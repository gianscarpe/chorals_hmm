import os
import itertools

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'dataset'))

# Bach chorales state space: pitch x duration
MIN_PITCH = 60
MAX_PITCH = 79
MIN_DUR = 1
MAX_DUR = 16