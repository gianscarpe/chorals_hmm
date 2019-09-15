import os
import math
import music21
from src import DATA_DIR
from src.parser.parser import dataset2states, dataset2music21_streams, create_music21_dataset
from src.helpers import save_pickle, load_pickle, get_pitch_space

vocab_path = os.path.join(DATA_DIR, 'bach_chorales', 'vocab.pkl')
data_path = os.path.join(DATA_DIR, 'bach_chorales', 'dataset.dt')
parsed_data_path = os.path.join(DATA_DIR, 'bach_chorales', 'parsed_dataset.pkl')

# save_pickle(get_pitch_space(), vocab_path)
# vocab = load_pickle(vocab_path)
# parsed_dataset = dataset2states(data_path, vocab)
# save_pickle(parsed_dataset, parsed_data_path)

# music21.environment.set('musicxmlPath', '/usr/bin/musescore')
# streams = dataset2music21_streams(data_path)
# chorale_num = 5
# streams[chorale_num].show()
# mf = music21.midi.translate.streamToMidiFile(streams[chorale_num])
# mf.open('midi.mid', 'wb')
# mf.write()
# mf.close()

max_pitch = 0
min_pitch = math.inf
max_dur = 0
min_dur = math.inf
bach_music21_datasets = create_music21_dataset()
for dataset in bach_music21_datasets:
    for elem in dataset:
        max_pitch = max(max_pitch, elem['pitch'])
        min_pitch = min(min_pitch, elem['pitch'])
        max_dur = max(max_dur, elem['duration'])
        min_dur = min(min_dur, elem['duration'])
print(min_dur, max_dur, min_pitch, max_pitch)
save_pickle(bach_music21_datasets, os.path.join(DATA_DIR, 'music21', 'bach.pkl'))