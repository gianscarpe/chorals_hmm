import os
import pickle
import numpy
import itertools
from src import BASE_DIR, DATA_DIR
from src.helpers import save_pickle, load_pickle

def tokenize(chars):
    if type(chars) == bytes:
        chars = chars.decode("utf-8")
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def tokens2notes(tokens):
    i = 0
    note = []
    notes = []
    while i < len(tokens) - 1:
        if tokens[i] != '(' and tokens[i] != ')' and (tokens[i] == 'pitch' or tokens[i] == 'dur'):
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

vocab_path = os.path.join(DATA_DIR, 'bach_chorales', 'vocab.pkl')
data_path = os.path.join(DATA_DIR, 'bach_chorales', 'dataset.dt')
parsed_data_path = os.path.join(DATA_DIR, 'bach_chorales', 'parsed_dataset.pkl')

unique_notes = notes2unique(data_path)
save_pickle(unique_notes, vocab_path)
vocab = load_pickle(vocab_path)
parsed_dataset = dataset2states(data_path, vocab_path)
save_pickle(parsed_dataset, parsed_data_path)