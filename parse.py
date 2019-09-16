import os
import math
import music21
from src import DATA_DIR
from src.parser.parser import dataset2states, dataset2music21_streams, parse_music21_dataset
from src.helpers import save_pickle, load_pickle, get_pitch_space, get_datasets_equality_ratio

vocab_path = os.path.join(DATA_DIR, 'music21', 'bach_vocab.pkl')
data_path = os.path.join(DATA_DIR, 'music21', 'bach_dataset.pkl')
parsed_data_path = os.path.join(DATA_DIR, 'music21', 'bach_states_dataset.pkl')

save_pickle(get_pitch_space(dataset='m21'), vocab_path)
vocab = load_pickle(vocab_path)
print(vocab)
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

# # pitches = []
# # durations = []
# bach_music21_datasets = []
# bach_music21_datasets = parse_music21_dataset()
# # streams = dataset2music21_streams(data_path)
# # our_bach_music21_datasets = parse_music21_dataset(our=True, streams=streams)
# # # bach_music21_datasets = load_pickle(os.path.join(DATA_DIR, 'music21', 'bach_dataset.pkl'))
# # # our_bach_music21_datasets = load_pickle(os.path.join(DATA_DIR, 'bach_chorales', 'music21', 'm21_dataset.pkl'))
# # # print(get_datasets_equality_ratio(our_bach_music21_datasets, bach_music21_datasets))
# # print(our_bach_music21_datasets)
# save_pickle(bach_music21_datasets, os.path.join(DATA_DIR, 'music21', 'bach_dataset.pkl'))