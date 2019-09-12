import os
import pickle
import numpy
import itertools
from . import BASE_DIR, DATA_DIR
from hmmlearn import hmm
from functools import reduce


def tokenize(chars):
    if type(chars) == bytes:
        chars = chars.decode("utf-8")
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def tokens2notes(tokens):
    i = 0
    note = []
    notes = []
    while i < len(tokens) - 1:
        if tokens[i] != '(' and tokens[i] != ')':
            note.extend([tokens[i], int(tokens[i+1])])
            i += 2
        elif tokens[i] == tokens[i+1] == ')':
            notes.append(tuple(note))
            note = []
            i += 1
        else:
            i += 1
    return notes

def parse_dataset(dataset_name, unique=False):
    with open(os.path.join(DATA_DIR, dataset_name), 'rb') as f:
        if unique:
            notes = []
        chorales = []
        for line in f.readlines():
            tokens = tokenize(line)
            if tokens != []:
                tokens.pop(0) # remove first '('
                tokens.pop(0) # remove chorales number
                tokens.pop()  # remove last ')'
                chorale_notes = tokens2notes(tokens)
                if unique:
                    notes.extend(chorale_notes)
                chorales.append(chorale_notes)
        if unique:
            return chorales, notes
        return chorales

def notes2unique(dataset_name):
    _, notes = parse_dataset(dataset_name, unique=True)
    return list(set(notes))

def dataset2states(dataset_name, vocab_name):
    vocab = load_pickle(os.path.join(DATA_DIR, vocab_name))
    dataset = parse_dataset(dataset_name)
    parsed_dataset = []
    for chorale in dataset:
        parsed_dataset.append([vocab.index(note) for note in chorale])
    return parsed_dataset

def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# unique_notes = notes2unique('../dataset/dataset.dt')
# save_pickle(unique_notes, '../dataset/vocab.pkl')
# vocab = load_pickle('../dataset/vocab.pkl')
# parsed_dataset = dataset2states('../dataset/dataset.dt', '../dataset/vocab.pkl')
# save_pickle(parsed_dataset, '../dataset/parsed_dataset.pkl')
vocabs = load_pickle(os.path.join(DATA_DIR, 'vocab.pkl'))
parsed_dataset = load_pickle(os.path.join(DATA_DIR, 'parsed_dataset.pkl'))
obs_states = [numpy.array([state for state in chorale]) for chorale in parsed_dataset]
obs_states = [state.reshape(-1, 1) for state in obs_states]
lengths = [len(seq) for seq in obs_states]
# Train the model.
model = hmm.MultinomialHMM(n_components=3, n_iter=100)
model.monitor_.verbose = True
# model.n_features = len(vocabs)
model.fit(numpy.concatenate(obs_states), lengths)
# Z2 = model.predict(obs_states)
# print(Z2)