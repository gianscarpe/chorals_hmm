import os
import math
import music21
import pickle
import numpy
import random
import argparse
import itertools
import statistics
import pomegranate
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

def test(model, testset, framework):
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

def train(n_components, n_iter, n_features, trainset, trainset_lengths, size, framework):
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

def generate_sample(model, model_name, framework):
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
