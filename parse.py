import os
import music21
from src import DATA_DIR
from src.parser.parser import dataset2music21_streams
from src.helpers import save_pickle, load_pickle, get_pitch_space

vocab_path = os.path.join(DATA_DIR, 'bach_chorales', 'vocab.pkl')
data_path = os.path.join(DATA_DIR, 'bach_chorales', 'dataset.dt')
parsed_data_path = os.path.join(DATA_DIR, 'bach_chorales', 'parsed_dataset.pkl')

# save_pickle(get_pitch_space(), vocab_path)
# vocab = load_pickle(vocab_path)
# parsed_dataset = dataset2states(data_path, vocab)
# save_pickle(parsed_dataset, parsed_data_path)

music21.environment.set('musicxmlPath', '/usr/bin/musescore')
streams = dataset2music21_streams(data_path)
chorale_num = 5
streams[chorale_num].show()
mf = music21.midi.translate.streamToMidiFile(streams[chorale_num])
mf.open('midi.mid', 'wb')
mf.write()
mf.close()

# scores = music21.corpus.search('bach', 'composer')
# music21_bach = scores[10].parse().parts['Soprano']
# music21_bach.show()
# mf = music21.midi.translate.streamToMidiFile(music21_bach)
# mf.open('music21_bach.mid', 'wb')
# mf.write()
# mf.close()