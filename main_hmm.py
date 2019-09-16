import os
import math
import music21
import pickle
import numpy
import random
import itertools
from src import BASE_DIR, DATA_DIR, MODELS_DIR, MIDI_DIR
from src.parser.parser import states2notes, states2music21_stream
from src.helpers import load_pickle, save_pickle, stream2midi
from hmmlearn import hmm
from functools import reduce

music21.environment.set('musicxmlPath', '/usr/bin/musescore')
music21.environment.set('graphicsPath', '/usr/bin/musescore')
music21.environment.set('musescoreDirectPNGPath', '/usr/bin/musescore')

vocabs = load_pickle(os.path.join(DATA_DIR, 'music21', 'bach_vocab.pkl'))
parsed_dataset = load_pickle(os.path.join(DATA_DIR, 'music21', 'bach_states_dataset.pkl'))

# Parameters
train_ratio = .6
training_size = round(len(parsed_dataset) * train_ratio)
n_components = 10
n_iter = 200
train = True
hmm_generate = True
generate_original = False

training_set = parsed_dataset[:training_size]
test_set = parsed_dataset[training_size:]

obs_train = [numpy.array([state for state in chorale]) for chorale in training_set]
obs_train = [state.reshape(-1, 1) for state in obs_train]
train_lengths = [len(seq) for seq in obs_train]

obs_test = [numpy.array([state for state in chorale]) for chorale in test_set]
obs_test = [state.reshape(-1, 1) for state in obs_test]
test_lengths = [len(seq) for seq in obs_test]

# Train the model.
hmm.MultinomialHMM._check_input_symbols = lambda *_: True
model_name = 'hmm_bach_m21' + '_' + str(int(train_ratio * 10)) + '_' + str(n_components) + '_' + str(n_iter)

if train:
    model = hmm.MultinomialHMM(n_components=n_components, n_iter=n_iter)
    model.monitor_.verbose = True
    model.n_features = len(vocabs)
    model.fit(numpy.concatenate(obs_train), train_lengths)
    # Print likelihoods
    likelihoods = [model.score(sequence) for i, sequence in enumerate(obs_test)]
    print(likelihoods)
    save_pickle(model, os.path.join(MODELS_DIR, 'hmm', model_name + '.pkl'))
else:
    model = load_pickle(os.path.join(MODELS_DIR, 'hmm', model_name + '.pkl'))
    likelihoods = [model.score(sequence) for i, sequence in enumerate(obs_test)]
    print(likelihoods)

# Generate song
if hmm_generate:
    sample, _ = model.sample(50)
    sample = list(itertools.chain(*sample))
    # notes = states2notes(sample, vocabs)
    # notes2midi(notes, os.path.join(MIDI_DIR, 'hmm', 'generated' + '_' + model_name + '.mid'))
    stream = states2music21_stream(sample, vocabs, our=False)
    #stream.show('lily')
    stream.write('musicxml.pdf', os.path.join(BASE_DIR, 'music_sheet', model_name + '.xml'))
    stream2midi(stream, os.path.join(MIDI_DIR, 'hmm', model_name + '.mid'))

if generate_original:
    chorale_num = random.randint(0, training_size - 1)
    sample = training_set[chorale_num]
    # notes = states2notes(sample, vocabs)
    # notes2midi(notes, os.path.join(MIDI_DIR, 'original', 'original' + '_' + str(chorale_num) + '.mid'))
    stream = states2music21_stream(sample, vocabs)
    stream2midi(stream, os.path.join(MIDI_DIR, 'hmm', 'generated' + '_' + str(chorale_num) + '.mid'))