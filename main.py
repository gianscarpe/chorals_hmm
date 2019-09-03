from factorial_hmm import FullDiscreteFactorialHMM
import numpy as np
import itertools

# TODO: info from the paper
'''
EM steps: 30 +- 12
K: from 2 to 6
M: from 2 to 9

'''

K = 2
M = 2
D = 3  # what is it? maybe number of different observation
n_steps = 30
random_seed = 1

params = {
    'hidden_alphabet_size': K,
    'n_hidden_chains': M,
    'observed_alphabet_size': D,
    'n_observed_chains': 1,
}

params['initial_hidden_state'] = np.zeros((M, K))
params['transition_matrices'] = np.zeros((M, K, K))
params['obs_given_hidden'] = np.zeros([K] * M + [D])

random_state = np.random.RandomState(random_seed)
for i in range(M):
    p1, p2 = random_state.rand(2)
    params['transition_matrices'][i, :, :] = [[1 - p1, p2], [p1, 1 - p2]]
    params['initial_hidden_state'][i, :] = [1 / K] * K

for st in itertools.product(*[range(K)] * M):
    R = random_state.rand(D)
    R /= R.sum()
    params['obs_given_hidden'][list(st) + [Ellipsis]] = R

hmm = FullDiscreteFactorialHMM(params=params, n_steps=n_steps,
                               calculate_on_init=True)

training_set = np.array([1, 0, 1]) # parsed training set state

hmm.EM(training_set,n_iterations=30)