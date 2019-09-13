import os
import math
import pickle
import numpy
import itertools
from src import BASE_DIR, DATA_DIR
from src.helpers import *
from hmmlearn import hmm
from functools import reduce

vocabs = load_pickle(os.path.join(DATA_DIR, 'bach_chorales', 'vocab.pkl'))
parsed_dataset = load_pickle(os.path.join(DATA_DIR, 'bach_chorales', 'parsed_dataset.pkl'))

training_set = parsed_dataset[:60]
test_set = parsed_dataset[60:]

obs_train = [numpy.array([state for state in chorale]) for chorale in training_set]
obs_train = [state.reshape(-1, 1) for state in obs_train]
train_lengths = [len(seq) for seq in obs_train]

obs_test = [numpy.array([state for state in chorale]) for chorale in test_set]
obs_test = [state.reshape(-1, 1) for state in obs_test]
test_lengths = [len(seq) for seq in obs_test]

# Train the model.
hmm.MultinomialHMM._check_input_symbols = lambda *_: True
model = hmm.MultinomialHMM(n_components=10, n_iter=100)
model.monitor_.verbose = True
model.n_features = len(vocabs)
model.fit(numpy.concatenate(obs_train), train_lengths)
likelihoods = [model.score(sequence[:10]) for i, sequence in enumerate(obs_test)]
print(likelihoods)
# print(model.score(numpy.concatenate(obs_test), test_lengths))
# Z2 = model.predict(obs_states)
# print(Z2)