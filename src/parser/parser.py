import os
import pickle
import numpy
import itertools
from src import DATA_DIR
from src.helpers import save_pickle, load_pickle, get_pitch_space

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
            note.extend([int(tokens[i+1])])
            i += 2
        elif tokens[i] == tokens[i+1] == ')':
            notes.append(tuple(note))
            note = []
            i += 1
        else:
            i += 1
    return notes

def parse_dataset(dataset_name):
    with open(os.path.join(DATA_DIR, dataset_name), 'rb') as f:
        chorales = []
        for line in f.readlines():
            tokens = tokenize(line)
            if tokens != []:
                tokens.pop(0) # remove first '('
                tokens.pop(0) # remove chorales number
                tokens.pop()  # remove last ')'
                chorale_notes = tokens2notes(tokens)
                chorales.append(chorale_notes)
        return chorales

def dataset2states(dataset_name, vocab):
    dataset = parse_dataset(dataset_name)
    parsed_dataset = []
    for chorale in dataset:
        parsed_dataset.append([vocab.index(note) for note in chorale])
    return parsed_dataset

vocab_path = os.path.join(DATA_DIR, 'bach_chorales', 'vocab.pkl')
data_path = os.path.join(DATA_DIR, 'bach_chorales', 'dataset.dt')
parsed_data_path = os.path.join(DATA_DIR, 'bach_chorales', 'parsed_dataset.pkl')

save_pickle(get_pitch_space(), vocab_path)
vocab = load_pickle(vocab_path)
parsed_dataset = dataset2states(data_path, vocab)
save_pickle(parsed_dataset, parsed_data_path)
