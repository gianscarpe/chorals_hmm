import os
import math
import music21
from src import DATA_DIR
from src.parser.parser import dataset2states, dataset2music21_streams, parse_music21_dataset
from src.helpers import save_pickle, load_pickle, get_pitch_space

vocab_path = os.path.join(DATA_DIR, 'bach_chorales', 'm21_vocab.pkl')
data_path = os.path.join(DATA_DIR, 'bach_chorales', 'm21_dataset.pkl')
parsed_data_path = os.path.join(DATA_DIR, 'bach_chorales', 'm21_states_dataset.pkl')

save_pickle(get_pitch_space(dataset='chorales_m21'), vocab_path)
vocab = load_pickle(vocab_path)
parsed_dataset = dataset2states(data_path, vocab, our=False)
print(parsed_dataset)
save_pickle(parsed_dataset, parsed_data_path)

# music21.environment.set('musicxmlPath', '/usr/bin/musescore')
# streams = dataset2music21_streams(data_path)
# chorale_num = 5
# streams[chorale_num].show()
# mf = music21.midi.translate.streamToMidiFile(streams[chorale_num])
# mf.open('midi.mid', 'wb')
# mf.write()
# mf.close()

# pitches = []
# durations = []
# bach_music21_datasets = []
# # bach_music21_datasets = parse_music21_dataset()
# streams = dataset2music21_streams(data_path)
# bach_music21_datasets.extend(parse_music21_dataset(our=True, streams=streams))
# for dataset in bach_music21_datasets:
#     for elem in dataset:
#         if elem['pitch'] not in pitches:
#             pitches.append(elem['pitch'])
#         if elem['duration'] not in durations:
#             durations.append(elem['duration'])
# print(durations, pitches)
# save_pickle(bach_music21_datasets, os.path.join(DATA_DIR, 'bach_chorales', 'm21_parsed_dataset.pkl'))