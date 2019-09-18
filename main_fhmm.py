from factorial_hmm import FullDiscreteFactorialHMM
import numpy as np
import itertools
import os
from src import BASE_DIR, DATA_DIR, MODELS_DIR, MIDI_DIR
from src.helpers import load_pickle, save_pickle, stream2midi
from src.parser.parser import states2notes, states2music21_stream
import argparse

# TODO: info from the paper

'''
EM steps: 30 +- 12
K: from 2 to 6
M: from 2 to 9

'''


def train(params, M, K, n_iterations, model_name, verbose, random_seed=1):
    print(" -- Training FHMM --\n")
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

    trained_hmm = hmm.EM(training_set, n_iterations=n_iterations,
                         verbose=verbose)

    return trained_hmm


def test(model, test_set):
    print(" -- Testing FHMM --\n")
    log_likelihoods = np.array(
        [model.Forward(np.array(test_set[i]))[2] for i, sequence in
         enumerate(test_set)])

    print(f"Test likelihood {np.mean(log_likelihoods)}")


if __name__ == "__main__":
    print(" -- main.py FHMM --\n")
    parser = argparse.ArgumentParser(description='Train and test FHMM')
    parser.add_argument('-K', type=int, default=2, help='value K')
    parser.add_argument('-M', type=int, default=2, help='value K')
    parser.add_argument('-N', type=int, default=15, help='Number of iterations')
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    parser.add_argument("-s", "--save_model", action="store_true",
                        help="Save the trained model")
    parser.add_argument("--generate", action="store_true",
                        help="Generate a midi file")
    parser.add_argument("--dataset", type=str,
                        default=os.path.join(DATA_DIR, 'chorales', 'music21'),
                        help="Dataset base dir")

    args = parser.parse_args()

    DIR = args.dataset
    vocabs = load_pickle(os.path.join(DIR, 'vocab.pkl'))
    parsed_dataset = load_pickle(os.path.join(DIR,
                                              'chorales_states_dataset.pkl'))

    dataset = np.array(list(map(np.array, parsed_dataset)))
    training_set = dataset[:60]  # parsed training set state
    test_set = dataset[60:]

    n_steps = len(training_set)

    K = args.K
    M = args.M
    D = len(vocabs)  # what is it? maybe number of different observation
    n_iterations = args.N
    hmm_generate = args.generate

    save = args.save_model
    verbose = args.verbose

    params = {'hidden_alphabet_size': K, 'n_hidden_chains': M,
              'observed_alphabet_size': D, 'n_observed_chains': 1,
              'initial_hidden_state': np.zeros((M, K)),
              'transition_matrices': np.zeros((M, K, K)),
              'obs_given_hidden': np.zeros([K] * M + [D])}

    model_name = f"K-{K}-M-{M}-nit-{n_iterations}"

    trained_hmm = train(params, M, K, n_iterations, model_name, verbose)
    test(trained_hmm, test_set)

    if save:
        save_pickle(trained_hmm,
                    os.path.join(MODELS_DIR, 'fhmm', model_name + ".pkl"))

    if hmm_generate:
        print(" -- Generating MIDI --\n")
        _, sample = trained_hmm.Simulate()
        sample = list(itertools.chain(*sample))
        # notes = states2notes(sample, vocabs)
        # notes2midi(notes, os.path.join(MIDI_DIR, 'hmm', 'generated' + '_' + model_name + '.mid'))
        stream = states2music21_stream(sample, vocabs, our=False)
        # stream.show('lily')
        stream.write('musicxml.pdf',
                     os.path.join(BASE_DIR, 'music_sheet', model_name + '.xml'))

        stream2midi(stream, os.path.join(MIDI_DIR, 'fhmm', model_name + '.mid'))
