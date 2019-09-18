from factorial_hmm import FullDiscreteFactorialHMM
import numpy as np
import itertools
import os
from src import BASE_DIR, DATA_DIR, MODELS_DIR, MIDI_DIR
from src.helpers import load_pickle, save_pickle, stream2midi
from src.parser.parser import states2notes, states2music21_stream

# TODO: info from the paper
'''
EM steps: 30 +- 12
K: from 2 to 6
M: from 2 to 9

'''

vocabs = load_pickle(os.path.join(DATA_DIR, 'chorales', 'music21', 'vocab.pkl'))
parsed_dataset = load_pickle(os.path.join(DATA_DIR, 'chorales', 'music21',
                                          'chorales_states_dataset.pkl'))

dataset = np.array(list(map(np.array, parsed_dataset)))
training_set = dataset[:60]  # parsed training set state

test_set = dataset[60:]

n_steps = len(training_set)

save = True
K = 2
M = 2
D = len(vocabs)  # what is it? maybe number of different observation
random_seed = 1
n_iterations = 15
hmm_generate = False

params = {'hidden_alphabet_size': K, 'n_hidden_chains': M,
          'observed_alphabet_size': D, 'n_observed_chains': 1,
          'initial_hidden_state': np.zeros((M, K)),
          'transition_matrices': np.zeros((M, K, K)),
          'obs_given_hidden': np.zeros([K] * M + [D])}

model_name = f"K-{K}-M-{M}-nit-{n_iterations}"

random_state = np.random.RandomState(random_seed)
for i in range(M):
    # matrix = random_state.random_sample((K, K))
    # matrix /= matrix.sum(axis=0)[np.newaxis, :]
    params['transition_matrices'][i][:][:] = [[1 / K] * K] * K

    # params['transition_matrices'][i][:][:] = [ [1 - ps[0], ps[1]], [ps[0], 1 - ps[1]]]
    params['initial_hidden_state'][i, :] = [1 / K] * K

for st in itertools.product(*[range(K)] * M):
    R = random_state.rand(D)
    R /= R.sum()
    params['obs_given_hidden'][list(st) + [Ellipsis]] = R

hmm = FullDiscreteFactorialHMM(params=params, n_steps=1000,
                               calculate_on_init=True)

trained_hmm = hmm.EM(training_set, n_iterations=n_iterations, verbose=True)

if (save == False):
    save_pickle(trained_hmm, os.path.join(MODELS_DIR, 'fhmm', model_name + ".pkl"))

log_likelihoods = np.array(
    [trained_hmm.Forward(np.array(test_set[i]))[2] for i, sequence in
     enumerate(test_set)])

print(f"Test likelihood {np.mean(log_likelihoods)}")


if hmm_generate:
    _, sample = trained_hmm.Simulate()
    sample = list(itertools.chain(*sample))
    # notes = states2notes(sample, vocabs)
    # notes2midi(notes, os.path.join(MIDI_DIR, 'hmm', 'generated' + '_' + model_name + '.mid'))
    stream = states2music21_stream(sample, vocabs, our=False)
    #stream.show('lily')
    stream.write('musicxml.pdf', os.path.join(BASE_DIR, 'music_sheet', model_name + '.xml'))
    stream2midi(stream, os.path.join(MIDI_DIR, 'fhmm', model_name + '.mid'))

