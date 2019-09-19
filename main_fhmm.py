from factorial_hmm import FullDiscreteFactorialHMM
import numpy
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

music21.environment.set('musicxmlPath', '/usr/bin/musescore')
music21.environment.set('graphicsPath', '/usr/bin/musescore')
music21.environment.set('musescoreDirectPNGPath', '/usr/bin/musescore')

def train(params, M, K, n_iterations, model_name, verbose, random_seed=42):
    print(" -- Training FHMM --\n")
    random_state = numpy.random.RandomState(random_seed)
    for i in range(M):
        # matrix = random_state.random_sample((K, K))
        # matrix /= matrix.sum(axis=0)[numpy.newaxis, :]
        params['transition_matrices'][i][:][:] = [[1 / K] * K] * K

        # params['transition_matrices'][i][:][:] = [ [1 - ps[0], ps[1]], [ps[0], 1 - ps[1]]]
        params['initial_hidden_state'][i, :] = [1 / K] * K

    for st in itertools.product(*[range(K)] * M):
        R = random_state.rand(D)
        R /= R.sum()
        params['obs_given_hidden'][list(st) + [Ellipsis]] = R

    hmm = FullDiscreteFactorialHMM(params=params, n_steps=1000,
                                   calculate_on_init=True)
    hmm = hmm.EM(trainset, n_iterations=n_iterations,
                                    verbose=verbose)
    return hmm

def test(model, testset):
    print(" -- Testing FHMM --\n")
    log_likelihoods = numpy.array(
        [model.Forward(numpy.array(testset[i]))[2] for i, sequence in
         enumerate(testset)])

    print(f"Test likelihood {numpy.mean(log_likelihoods)}")


if __name__ == "__main__":
    print(" -- main.py FHMM --\n")
    parser = argparse.ArgumentParser(description='Train and test FHMM')
    parser.add_argument('-K', type=int, default=2, help='value K')
    parser.add_argument('-M', type=int, default=2, help='value M of states')
    parser.add_argument('-N', type=int, default=15, help='Number of iterations')
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    parser.add_argument("-s", "--save-model", action="store_true",
                        help="Save the trained model")
    parser.add_argument('--trainset-size', type=str, action='store',
                        default='50',
                        help='Training set size')
    parser.add_argument('--skip-training', action='store_true')
    parser.add_argument('--model-path', type=str, action='store',
                        default=None,
                        help='Load model instead of training a new one')
    parser.add_argument("--generate", action="store_true",
                        help="Generate a midi file")
    parser.add_argument("--dataset-dir", type=str,
                        default=os.path.join(DATA_DIR, 'music21'),
                        help="Dataset base dir")
    parser.add_argument("--trainset-name", type=str,
                        default=os.path.join(DATA_DIR, 'music21', 'bach_states_dataset.pkl'),
                        help="Dataset base dir")
    parser.add_argument("--testset-name", type=str,
                        default=None,
                        help="Dataset base dir")

    args = parser.parse_args()

    fullname = os.path.join(args.dataset_dir, args.trainset_name)
    vocabs = load_pickle(os.path.join(args.dataset_dir, 'vocab.pkl'))
    parsed_dataset = load_pickle(fullname)

    dataset = numpy.array(list(map(numpy.array, parsed_dataset)))
    if args.trainset_size == 'all':
        trainset_size = len(dataset)
        trainset = dataset
    else:
        trainset_size = int(args.trainset_size)
        trainset = dataset[:trainset_size]
    if args.testset_name is not None:
        testset = load_pickle(os.path.join(args.dataset_dir, args.testset_name))
    else:
        if trainset_size < len(dataset):
            testset = dataset[trainset_size:]
        else:
            print('Not enough data for the test size')
            exit(1)

    n_steps = len(trainset)
    K = args.K
    M = args.M
    D = len(vocabs)  # what is it? maybe number of different observation
    n_iterations = args.N
    hmm_generate = args.generate
    save = args.save_model
    verbose = args.verbose

    params = {'hidden_alphabet_size': K, 'n_hidden_chains': M,
              'observed_alphabet_size': D, 'n_observed_chains': 1,
              'initial_hidden_state': numpy.zeros((M, K)),
              'transition_matrices': numpy.zeros((M, K, K)),
              'obs_given_hidden': numpy.zeros([K] * M + [D])}

    model_name = f"K-{K}-M-{M}-ts-{trainset_size}-nit-{n_iterations}"

    if args.skip_training:
        if args.model_path is None:
            print('SPecify the model path running this command with --model-path PATH-TO-MODEL')
            exit(1)
        trained_hmm = load_pickle(os.path.abspath(args.model_path))
    else:
        trained_hmm = train(params, M, K, n_iterations, model_name, verbose)
    test(trained_hmm, testset)

    if save:
        save_pickle(trained_hmm,
                    os.path.join(MODELS_DIR, 'fhmm', model_name + ".pkl"))

    if hmm_generate:
        print(" -- Generating MIDI --\n")
        _, sample = trained_hmm.Simulate()
        sample = list(itertools.chain(*sample))[:50]
        # notes = states2notes(sample, vocabs)
        # notes2midi(notes, os.path.join(MIDI_DIR, 'hmm', 'generated' + '_' + model_name + '.mid'))
        stream = states2music21_stream(sample, vocabs, our=False)
        # stream.show('lily')
        if not os.path.exists(os.path.join(BASE_DIR, 'music_sheet')):
            os.makedirs(os.path.join(BASE_DIR, 'music_sheet'))
        stream.write('musicxml.pdf',
                     os.path.join(BASE_DIR, 'music_sheet', model_name + '.xml'))
        if not os.path.exists(os.path.join(MIDI_DIR, 'fhmm')):
            os.makedirs(os.path.join(MIDI_DIR, 'fhmm'))
        stream2midi(stream, os.path.join(MIDI_DIR, 'fhmm', model_name + '.mid'))
