import os
import math
import music21
import pickle
import numpy
import random
import itertools
import statistics
from src import BASE_DIR, DATA_DIR, MODELS_DIR, MIDI_DIR
from src.parser.parser import states2notes, states2music21_stream
from src.helpers import load_pickle, save_pickle, stream2midi
from hmmlearn import hmm

music21.environment.set('musicxmlPath', '/usr/bin/musescore')
music21.environment.set('graphicsPath', '/usr/bin/musescore')
music21.environment.set('musescoreDirectPNGPath', '/usr/bin/musescore')

vocab = load_pickle(os.path.join(DATA_DIR, 'music21', 'vocab.pkl'))
parsed_dataset = load_pickle(os.path.join(DATA_DIR, 'combined', 'chorales_states_dataset.pkl'))
test_dataset = load_pickle(os.path.join(DATA_DIR, 'combined', 'beethoven_states_dataset.pkl'))

# Parameters
train_ratio = .6
training_size = 30
n_components = 20
n_iter = 100
train = False
hmm_generate = True
generate_original = False

training_set = parsed_dataset
test_set = test_dataset

obs_train = [numpy.array([state for state in chorale]) for chorale in training_set]
obs_train = [state.reshape(-1, 1) for state in obs_train]
train_lengths = [len(seq) for seq in obs_train]

obs_test = [numpy.array([state for state in chorale]) for chorale in test_set]
obs_test = [state.reshape(-1, 1) for state in obs_test]
test_lengths = [len(seq) for seq in obs_test]

# Train the model.
hmm.MultinomialHMM._check_input_symbols = lambda *_: True
model_name = 'hmm_m21' + '_' + str(training_size) + '_' + str(n_components) + '_' + str(n_iter)

if train:
    model = hmm.MultinomialHMM(n_components=n_components, n_iter=n_iter)
    model.monitor_.verbose = True
    model.n_features = len(vocab)
    model.fit(numpy.concatenate(obs_train), train_lengths)
    save_pickle(model, os.path.join(MODELS_DIR, 'hmm', model_name + '.pkl'))
else:
    model = load_pickle(os.path.join(MODELS_DIR, 'hmm', model_name + '.pkl'))

# Print likelihoods
likelihoods = [model.score(song) for song in obs_test]
infs = sum(1 if math.isinf(ll) else 0 for ll in likelihoods)
print('#infs {} on {}-length'.format(infs, len(likelihoods)))
likelihoods = [ll if not math.isinf(ll) else 0 for ll in likelihoods]
print("AVG: {}".format(statistics.mean(likelihoods)))

# Generate song
if hmm_generate:
    sample, _ = model.sample(50)
    sample = list(itertools.chain(*sample))
    stream = states2music21_stream(sample, vocab, our=False)
    stream.write('musicxml.pdf', os.path.join(BASE_DIR, 'music_sheet', model_name + '.xml'))
    stream2midi(stream, os.path.join(MIDI_DIR, 'hmm', model_name + '.mid'))

if generate_original:
    chorale_num = random.randint(0, training_size - 1)
    sample = training_set[chorale_num]
    stream = states2music21_stream(sample, vocab)
    stream2midi(stream, os.path.join(MIDI_DIR, 'hmm', 'generated' + '_' + str(chorale_num) + '.mid'))