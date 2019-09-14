import os
import math
import pickle
import numpy
import itertools
from src import BASE_DIR, DATA_DIR, MODELS_DIR, MIDI_DIR
from src.parser.parser import states2notes
from src.helpers import load_pickle, save_pickle, notes2midi
from hmmlearn import hmm
from functools import reduce

vocabs = load_pickle(os.path.join(DATA_DIR, 'bach_chorales', 'vocab.pkl'))
parsed_dataset = load_pickle(os.path.join(DATA_DIR, 'bach_chorales', 'parsed_dataset.pkl'))

training_set = parsed_dataset[:90]
test_set = parsed_dataset[90:]

obs_train = [numpy.array([state for state in chorale]) for chorale in training_set]
obs_train = [state.reshape(-1, 1) for state in obs_train]
train_lengths = [len(seq) for seq in obs_train]

obs_test = [numpy.array([state for state in chorale]) for chorale in test_set]
obs_test = [state.reshape(-1, 1) for state in obs_test]
test_lengths = [len(seq) for seq in obs_test]

# Train the model.
hmm.MultinomialHMM._check_input_symbols = lambda *_: True
n_components = 30
n_iter = 100
train = True
model_name = 'hmm_' + str(n_components) + '_' + str(n_iter) + '.pkl'

if train:
    model = hmm.MultinomialHMM(n_components=n_components, n_iter=n_iter)
    model.monitor_.verbose = True
    model.n_features = len(vocabs)
    model.fit(numpy.concatenate(obs_train), train_lengths)
    save_pickle(model, os.path.join(MODELS_DIR, 'hmm', model_name))
else:
    model = load_pickle(os.path.join(MODELS_DIR, 'hmm', model_name))

# Print likelihoods
likelihoods = [model.score(sequence) for i, sequence in enumerate(obs_test)]
print(likelihoods)

# Generate song
sample, _ = model.sample(50, 42)
sample = list(itertools.chain(*sample))
notes = states2notes(sample, vocabs)
notes2midi(notes, os.path.join(MIDI_DIR, 'generated.mid'))