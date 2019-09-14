import os
import pickle
import numpy
import music21
import itertools
from src import BASE_DIR, DATA_DIR
from src.helpers import save_pickle, load_pickle

scores = music21.corpus.search('mozart', 'composer')
print(scores)
for score in scores:
    song = score.parse()
    print(music21.instrument.partitionByInstrument(song))
    

