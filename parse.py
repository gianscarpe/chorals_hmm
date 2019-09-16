import os
import math
import music21
from fractions import Fraction
from src import DATA_DIR
from src.parser.parser import dataset2states, dataset2music21_streams, parse_music21_dataset
from src.helpers import save_pickle, load_pickle, get_pitch_space, get_datasets_equality_ratio

vocab_path = os.path.join(DATA_DIR, 'music21', 'vocab.pkl')
data_path = os.path.join(DATA_DIR, 'music21', 'bach_dataset.pkl')
parsed_data_path = os.path.join(DATA_DIR, 'music21', 'bach_states_dataset.pkl')

save_pickle(get_pitch_space(dataset='m21'), vocab_path)
vocab = load_pickle(vocab_path)
print(len(vocab), '\n', vocab)
parsed_dataset = dataset2states(data_path, vocab, our=False)
print(parsed_dataset)
save_pickle(parsed_dataset, parsed_data_path)

pitches = []
durations = []
bach_music21_datasets = []
# bach_music21_datasets = parse_music21_dataset(author='beethoven', instrument='viola')
# bach_music21_datasets = load_pickle(os.path.join(DATA_DIR, 'music21', 'bach_dataset.pkl'))
# for dataset in bach_music21_datasets:
#     for elem in dataset:
#         if elem['pitch'] not in pitches:
#             pitches.append(elem['pitch'])
#         if elem['duration'] not in durations:
#             durations.append(elem['duration'])
# pitches.sort()
# durations.sort()
# print(pitches, durations)
# streams = dataset2music21_streams(data_path)
# our_bach_music21_datasets = parse_music21_dataset(our=True, streams=streams)
# bach_music21_datasets = load_pickle(os.path.join(DATA_DIR, 'music21', 'bach_dataset.pkl'))
# our_bach_music21_datasets = load_pickle(os.path.join(DATA_DIR, 'bach_chorales', 'music21', 'm21_dataset.pkl'))
# print(get_datasets_equality_ratio(our_bach_music21_datasets, bach_music21_datasets))
# combined = bach_music21_datasets + our_bach_music21_datasets
# print(combined)
# print(len(bach_music21_datasets))
# save_pickle(bach_music21_datasets, os.path.join(DATA_DIR, 'music21', 'beethoven_dataset.pkl'))