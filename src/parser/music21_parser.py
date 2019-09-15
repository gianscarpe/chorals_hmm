import os
import pickle
import numpy
import music21
import itertools
from src import BASE_DIR, DATA_DIR
from src.helpers import save_pickle, load_pickle

music21.environment.set('musicxmlPath', '/usr/bin/musescore')
scores = music21.corpus.search('bach', 'composer')
print(scores)
for score in scores:
    song = score.parse()
    song.show()
    

