import os
import math
import music21
import pickle
import numpy
import random
import argparse
import itertools
import statistics
from src import BASE_DIR, DATA_DIR, MODELS_DIR, MIDI_DIR
from src.parser.parser import states2notes, states2music21_stream
from src.helpers import load_pickle, save_pickle, stream2midi
from hmmlearn import hmm

def prepare_dataset(dataset):
    dataset = [numpy.array([state for state in song]).reshape(-1, 1) for song in dataset]
    lengths = [len(song) for song in dataset]
    return dataset, lengths

def test(model, testset, test_lengths):
    likelihoods = [model.score(song) for song in testset]
    infs = sum(1 if math.isinf(ll) else 0 for ll in likelihoods)
    print('#infs {} on {}-length'.format(infs, len(likelihoods)))
    likelihoods = [ll for ll in likelihoods if not math.isinf(ll)]
    if likelihoods != []:
        print("AVG: {}".format(statistics.mean(likelihoods)))
    else:
        print("AVG: 0")

def train(n_components, n_iter, n_features, trainset, trainset_lengths):
    model = hmm.MultinomialHMM(n_components=n_components, n_iter=n_iter)
#    model.monitor_.verbose = args.verbose
    model.n_features = n_features
    model.fit(numpy.concatenate(trainset), trainset_lengths)
    return model


#music21.environment.set('musicxmlPath', '/usr/bin/musescore')
#music21.environment.set('graphicsPath', '/usr/bin/musescore')
#music21.environment.set('musescoreDirectPNGPath', '/usr/bin/musescore')

if __name__ == "__main__":
    print(" -- main.py HMM --\n")
    parser = argparse.ArgumentParser(description='Train and test HMM')
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
    vocabs = load_pickle(os.path.join(args.dataset_dir, 'vocabs.pkl'))
    dataset = load_pickle(fullname)

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

    # Parameters
    trainset_size = args.trainset_size
    n_components = args.M
    n_iter = args.N
    hmm_generate = args.generate
    generate_original = False

    obs_train, train_lengths = prepare_dataset(trainset)
    obs_test, test_lengths = prepare_dataset(testset)

    model_name = 'M-' + str(n_components) + '-ts-' + str(trainset_size) + '-nit-' + str(n_iter)

    if not args.skip_training:
        hmm.MultinomialHMM._check_input_symbols = lambda *_: True
        model = train(n_components, n_iter, len(vocabs), obs_train, train_lengths)
        if args.save_model:
            save_pickle(model, os.path.join(MODELS_DIR, 'hmm', model_name + '.pkl'))
    else:
        if args.model_path is None:
            print('SPecify the model path running this command with --model-path PATH-TO-MODEL')
            exit(1)
        model = load_pickle(os.path.abspath(args.model_path))

    # Print likelihoods
    test(model, obs_test, test_lengths)

    # Generate song
    if hmm_generate:
        sample, _ = model.sample(50)
        sample = list(itertools.chain(*sample))
        stream = states2music21_stream(sample, vocabs, our=False)
        if not os.path.exists(os.path.join(BASE_DIR, 'music_sheet')):
            os.makedirs(os.path.join(BASE_DIR, 'music_sheet'))
        stream.write('musicxml.pdf',
                     os.path.join(BASE_DIR, 'music_sheet', model_name + '.xml'))
        if not os.path.exists(os.path.join(MIDI_DIR, 'hmm')):
            os.makedirs(os.path.join(MIDI_DIR, 'hmm'))
        stream2midi(stream, os.path.join(MIDI_DIR, 'hmm', model_name + '.mid'))

    if generate_original:
        chorale_num = random.randint(0, trainset_size - 1)
        sample = trainset[chorale_num]
        stream = states2music21_stream(sample, vocabs)
        stream2midi(stream, os.path.join(MIDI_DIR, 'hmm', 'generated' + '_' + str(chorale_num) + '.mid'))