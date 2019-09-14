import pickle
import itertools
from src import MIN_DUR, MAX_DUR, MIN_PITCH, MAX_PITCH

def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def get_pitches():
    return [i for i in range(MIN_PITCH, MAX_PITCH + 1)]

def get_durations():
    return [i for i in range(MIN_DUR, MAX_DUR + 1)]

def get_pitch_space():
    pitches = get_pitches()
    durations = get_durations()
    pitch_space = list(itertools.product(pitches, durations))
    return pitch_space