import os
import itertools

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'dataset'))
MODELS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'models'))
MIDI_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'midi'))

# Bach chorales state space: pitch x duration
MIN_PITCH_CHORALES = 60
MAX_PITCH_CHORALES = 79
MIN_DUR_CHORALES = 1
MAX_DUR_CHORALES = 16

# Music21 Bach chorales state space: pitch x duration
MIN_PITCH_MUSIC21 = 57
MAX_PITCH_MUSIC21 = 81
MIN_DUR_MUSIC21 = 0
MAX_DUR_MUSIC21 = 6