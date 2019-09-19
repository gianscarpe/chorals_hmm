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


def init(data_path, size):
    vocabs = load_pickle(os.path.join(DATA_DIR, 'music21', 'vocabs.pkl'))
    dataset = load_pickle(data_path)

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

def test(model, testset):
    likelihoods = [model.score(song) for song in testset]
    infs = sum(1 if math.isinf(ll) else 0 for ll in likelihoods)
    infs_string = '#infs {} on {}-length'.format(infs, len(likelihoods))
    likelihoods = [ll for ll in likelihoods if not math.isinf(ll)]
    if likelihoods != []:
        likelihood_mean = statistics.mean(likelihoods)
        result = "AVG: " + str(likelihood_mean)
    else:
        result = "AVG: 0"
    return infs_string, result

def train(n_components, n_iter, n_features, trainset, trainset_lengths, size):
    hmm.MultinomialHMM._check_input_symbols = lambda *_: True
    model = hmm.MultinomialHMM(n_components=n_components, n_iter=n_iter)
    model.n_features = n_features
    model.fit(numpy.concatenate(trainset), trainset_lengths)
    model_name = 'M-' + str(n_components) + '-ts-' + str(size) + '-nit-' + str(n_iter)
    save_pickle(model, os.path.join(MODELS_DIR, 'hmm', model_name + '.pkl'))
    return model, model_name

def generate_sample(model, model_name):
    vocabs = load_pickle(os.path.join(DATA_DIR, 'music21', 'vocabs.pkl'))
    sample, _ = model.sample(50)
    sample = list(itertools.chain(*sample))
    stream = states2music21_stream(sample, vocabs, our=False)
    if not os.path.exists(os.path.join(BASE_DIR, 'music_sheet')):
        os.makedirs(os.path.join(BASE_DIR, 'music_sheet'))
    conv = music21.converter.subConverters.ConverterLilypond()
    conv.write(stream, fmt='lilypond', fp=os.path.join(BASE_DIR, 'static', 'scores', model_name), subformats=['png'])
    image = os.path.join('static', 'scores', model_name) + ".png"
    files = os.listdir(os.path.join(BASE_DIR, 'static', 'scores'))
    for item in files:
        if item.endswith(".eps") or item.endswith(".count") or item.endswith(".tex") or item.endswith(".texi") or item.endswith(".pkl"):
            os.remove(os.path.join(BASE_DIR, 'static', 'scores', item))
    if not os.path.exists(os.path.join(MIDI_DIR, 'hmm')):
        os.makedirs(os.path.join(MIDI_DIR, 'hmm'))
    stream2midi(stream, os.path.join(BASE_DIR, 'static', 'midi', model_name + '.mid'))
    midi = os.path.join('static' ,'midi', model_name + '.mid')
    return image, midi
