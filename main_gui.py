import os
import math
import music21
import numpy
import itertools
import pomegranate
from factorial_hmm import FullDiscreteFactorialHMM
from src import BASE_DIR, DATA_DIR, MODELS_DIR, MIDI_DIR
from src.parser.parser import states2notes, states2music21_stream
from src.helpers import load_pickle, save_pickle, stream2midi
from hmmlearn import hmm


def init(data_path, size, type):
    vocabs = load_pickle(os.path.join(DATA_DIR, 'music21', 'vocabs.pkl'))
    dataset = load_pickle(data_path)

    if type == "fhmm":
        dataset = numpy.array(list(map(numpy.array, dataset)))

    if size == 'all':
        trainset = dataset
        testset = None
    else:
        trainset_size = int(size)
        trainset = dataset[:trainset_size]
        testset = None
        if trainset_size < len(dataset):
            testset = dataset[trainset_size:]
        else:
            print('Not enough data for the test size')
            exit(1)
    return trainset, testset, vocabs

def prepare_dataset(dataset):
    dataset = [numpy.array([state for state in song]).reshape(-1, 1) for song in dataset]
    lengths = [len(song) for song in dataset]
    return dataset, lengths

def test_hmm(model, testset, framework):
    if framework == "hmml":
        print("Using hmml")
        likelihoods = numpy.array([model.score(song) for song in testset], dtype=numpy.float64)
    else:
        print("Using pomegranate")
        likelihoods = numpy.array([model.log_probability(numpy.array(song), check_input=False) for song in testset],
                                  dtype=numpy.float64)
    infs = sum(1 if math.isinf(ll) else 0 for ll in likelihoods)
    result = numpy.mean(likelihoods)
    print(infs, result)
    result_string = "AVG: {}".format(result)
    infs_string = '#infs {} on {}-length'.format(infs, len(likelihoods))
    return infs_string, result_string

def train_hmm(n_components, n_iter, n_features, trainset, trainset_lengths, size, framework):
    if framework == "hmml":
        print("Using hmml")
        model = hmm.MultinomialHMM(n_components=n_components, n_iter=n_iter)
        model.n_features = n_features
        model.fit(numpy.concatenate(trainset), trainset_lengths)
        fw = "hmml"
    else:
        print("Using pomegranate")
        model = pomegranate.HiddenMarkovModel.from_samples(
            pomegranate.DiscreteDistribution,
            n_components=n_components,
            X=trainset,
            algorithm='baum-welch',
            min_iterations=0,
            max_iterations=n_iter)
        model.bake()
        fw = "pom"
    model_name = 'M-' + str(n_components) + '-ts-' + str(size) + '-nit-' + str(n_iter) + '-fw-' + fw
    save_pickle(model, os.path.join(MODELS_DIR, 'hmm', model_name + '.pkl'))
    return model, model_name

def generate_sample_hmm(model, model_name, framework):
    vocabs = load_pickle(os.path.join(DATA_DIR, 'music21', 'vocabs.pkl'))
    if framework == "hmml":
        print("Using hmml")
        sample, _ = model.sample(50)
        sample = list(itertools.chain(*sample))
    else:
        print("Using pomegranate")
        sample = model.sample(length=50)
    stream = states2music21_stream(sample, vocabs, our=False)
    if not os.path.exists(os.path.join(BASE_DIR, 'music_sheet')):
        os.makedirs(os.path.join(BASE_DIR, 'music_sheet'))
    conv = music21.converter.subConverters.ConverterLilypond()
    conv.write(stream, fmt='lilypond', fp=os.path.join(BASE_DIR, 'static', 'scores', 'hmm', model_name), subformats=['png'])
    image = os.path.join('static', 'scores', 'hmm', model_name) + ".png"
    files = os.listdir(os.path.join(BASE_DIR, 'static', 'scores'))
    for item in files:
        if item.endswith(".eps") or item.endswith(".count") or item.endswith(".tex") or item.endswith(".texi") or item.endswith(".pkl"):
            os.remove(os.path.join(BASE_DIR, 'static', 'scores', 'hmm', item))
    if not os.path.exists(os.path.join(MIDI_DIR, 'hmm')):
        os.makedirs(os.path.join(MIDI_DIR, 'hmm'))
    stream2midi(stream, os.path.join(BASE_DIR, 'static', 'midi', 'hmm', model_name + '.mid'))
    midi = os.path.join('static' ,'midi', 'hmm', model_name + '.mid')
    return image, midi

def train_fhmm(D, M, K, n_iterations, size, trainset, random_seed=42):
    print(" -- Training FHMM --\n")

    params = {'hidden_alphabet_size': K, 'n_hidden_chains': M,
              'observed_alphabet_size': D, 'n_observed_chains': 1,
              'initial_hidden_state': numpy.zeros((M, K)),
              'transition_matrices': numpy.zeros((M, K, K)),
              'obs_given_hidden': numpy.zeros([K] * M + [D])}

    random_state = numpy.random.RandomState(random_seed)
    for i in range(M):
        params['transition_matrices'][i][:][:] = [[1 / K] * K] * K
        params['initial_hidden_state'][i, :] = [1 / K] * K

    for st in itertools.product(*[range(K)] * M):
        R = random_state.rand(D)
        R /= R.sum()
        params['obs_given_hidden'][list(st) + [Ellipsis]] = R

    hmm = FullDiscreteFactorialHMM(params=params, n_steps=100, calculate_on_init=True)
    hmm = hmm.EM(trainset, n_iterations=n_iterations)

    model_name = f"K-{K}-M-{M}-ts-{size}-nit-{n_iterations}"
    save_pickle(hmm, os.path.join(MODELS_DIR, 'fhmm', model_name + ".pkl"))

    return hmm, model_name

def test_fhmm(model, testset):
    print(" -- Testing FHMM --\n")
    log_likelihoods = numpy.array(
        [model.Forward(numpy.array(testset[i]))[2] for i, sequence in
         enumerate(testset)])
    result = f"Test likelihood {numpy.mean(log_likelihoods)}"

    return result

def generate_sample_fhmm(model, model_name):
    print(" -- Generating MIDI --\n")
    vocabs = load_pickle(os.path.join(DATA_DIR, 'chorales', 'music21', 'vocabs.pkl'))
    _, sample = model.Simulate()
    sample = list(itertools.chain(*sample))[:50]
    stream = states2music21_stream(sample, vocabs, our=False)
    # stream.show('lily')
    if not os.path.exists(os.path.join(BASE_DIR, 'music_sheet')):
        os.makedirs(os.path.join(BASE_DIR, 'music_sheet'))
    conv = music21.converter.subConverters.ConverterLilypond()
    conv.write(stream, fmt='lilypond', fp=os.path.join(BASE_DIR, 'static', 'scores', 'fhmm', model_name), subformats=['png'])
    image = os.path.join('static', 'scores', 'fhmm',  model_name) + ".png"
    files = os.listdir(os.path.join(BASE_DIR, 'static', 'scores', 'fhmm'))
    for item in files:
        if item.endswith(".eps") or item.endswith(".count") or item.endswith(".tex") or item.endswith(
                ".texi") or item.endswith(".pkl"):
            os.remove(os.path.join(BASE_DIR, 'static', 'scores', 'fhmm', item))
    if not os.path.exists(os.path.join(MIDI_DIR, 'fhmm')):
        os.makedirs(os.path.join(MIDI_DIR, 'fhmm'))
    stream2midi(stream, os.path.join(BASE_DIR, 'static', 'midi', 'fhmm', model_name + '.mid'))
    midi = os.path.join('static', 'midi', 'fhmm', model_name + '.mid')
    return image, midi