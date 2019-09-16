import os
import itertools

BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, 'dataset'))
MODELS_DIR = os.path.abspath(os.path.join(BASE_DIR, 'models'))
MIDI_DIR = os.path.abspath(os.path.join(BASE_DIR, 'midi'))

# Bach chorales (our dataset) state space: pitch x duration
MIN_PITCH_CHORALES = 60
MAX_PITCH_CHORALES = 79
MIN_DUR_CHORALES = 1
MAX_DUR_CHORALES = 16

# Bach chorales (our dataset parsed by music21) state space: pitch x duration
MIN_PITCH_CHORALES_M21 = 52
MAX_PITCH_CHORALES_M21 = 77
DURATIONS_CHORALES_M21 = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]

# Music21 Bach chorales state space: pitch x duration
MIN_PITCH_M21 = 51
MAX_PITCH_M21 = 81
DURATIONS_M21 = [0.0, 0.125, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]

# Music21 and our dataset state space: pitch x duration
MIN_PITCH_COMBINED = 51
MAX_PITCH_COMBINED = 81
DURATIONS_COMBINED = [0.0, 0.125, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]