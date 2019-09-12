import os
import pickle
import numpy
import itertools
from src import BASE_DIR, DATA_DIR
from src.helpers import *
from hmmlearn import hmm
from functools import reduce

vocabs = load_pickle(os.path.join(DATA_DIR, 'vocab.pkl'))
parsed_dataset = load_pickle(os.path.join(DATA_DIR, 'parsed_dataset.pkl'))

training_set = parsed_dataset[:30]
test_set = parsed_dataset[30:66]

obs_train = [numpy.array([state for state in chorale]) for chorale in training_set]
obs_train = [state.reshape(-1, 1) for state in obs_train]
train_lengths = [len(seq) for seq in obs_train]

obs_test = [numpy.array([state for state in chorale]) for chorale in test_set]
obs_test = [state.reshape(-1, 1) for state in obs_test]
test_lengths = [len(seq) for seq in obs_test]

# Train the model.
hmm.MultinomialHMM._check_input_symbols = lambda *_: True
model = hmm.MultinomialHMM(n_components=25, n_iter=100)
model.monitor_.verbose = True
model.n_features = len(vocabs)
model.fit(numpy.concatenate(obs_train), train_lengths)
print(model.score(numpy.concatenate(obs_test), test_lengths))
# Z2 = model.predict(obs_states)
# print(Z2)