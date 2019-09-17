import os
import itertools
from fractions import Fraction


BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, 'dataset'))
MODELS_DIR = os.path.abspath(os.path.join(BASE_DIR, 'models'))
MIDI_DIR = os.path.abspath(os.path.join(BASE_DIR, 'midi'))

# Authors and instruments
AUTHORS = ['bach', 'beethoven', 'mozart']
INSTRUMENTS = ['soprano', 'viola', 'viola']

# Bach chorales (our dataset) state space: pitch x duration
MIN_PITCH_CHORALES = 60
MAX_PITCH_CHORALES = 79
MIN_DUR_CHORALES = 1
MAX_DUR_CHORALES = 16

# Bach chorales (our dataset parsed by music21) state space: pitch x duration
PITCHES_CHORALES_M21 = [52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 74.0, 75.0, 76.0, 77.0]
DURATIONS_CHORALES_M21 = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]

# Music21 state space: pitch x duration
BACH_PITCHES_M21 = [51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 79.0, 81.0]
BACH_DURATIONS_M21 = [0.0, 0.125, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
MOZART_PITCHES_M21 = [41.0, 43.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0]
MOZART_DURATIONS_M21 = [0.0, 0.0625, Fraction(1, 12), 0.125, Fraction(1, 6), 0.25, Fraction(1, 3), 0.375, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]
BEETHOVEN_PITCHES_M21 = [39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0]
BEETHOVEN_DURATIONS_M21 = [0.0, 0.00390625, 0.02734375, 0.05859375, Fraction(1, 12), Fraction(1, 10), 0.125, Fraction(1, 6), 0.19921875, 0.25, Fraction(1, 3), 0.375, 0.5, Fraction(2, 3), 0.75, 0.875, 1.0, 1.5, 1.75, 2.0, 3.0, 4.0]

# Music21 combined state space: pitch x duration
PITCHES_COMBINED_M21 = list(set(BACH_PITCHES_M21 + MOZART_PITCHES_M21 + BEETHOVEN_PITCHES_M21))
DURATIONS_COMBINED_M21 = list(set(BACH_DURATIONS_M21 + MOZART_DURATIONS_M21 + BEETHOVEN_DURATIONS_M21))

# Music21 combined and our dataset (parsed with music21) state space: pitch x duration
PITCHES_ALL_M21 = list(set(PITCHES_COMBINED_M21 + PITCHES_CHORALES_M21))
DURATIONS_ALL_M21 = list(set(DURATIONS_COMBINED_M21 + DURATIONS_CHORALES_M21))