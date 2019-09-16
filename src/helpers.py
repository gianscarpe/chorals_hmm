import pickle
import music21
import itertools
from src import MIN_DUR_CHORALES, MAX_DUR_CHORALES, MIN_PITCH_CHORALES, MAX_PITCH_CHORALES

def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def get_pitches(dataset='chorales'):
    if dataset == 'chorales':
        return [i for i in range(MIN_PITCH_CHORALES, MAX_PITCH_CHORALES + 1)]

def get_durations(dataset='chorales'):
    if dataset == 'chorales':
        return [i for i in range(MIN_DUR_CHORALES, MAX_DUR_CHORALES + 1)]

def get_pitch_space(dataset='chorales'):
    pitches = get_pitches(dataset=dataset)
    durations = get_durations(dataset=dataset)
    pitch_space = list(itertools.product(pitches, durations))
    return pitch_space

def stream2midi(stream, midi_path):
    mf = music21.midi.translate.streamToMidiFile(stream)
    mf.open(midi_path, 'wb')
    mf.write()
    mf.close()

# To use this method install first MIDIUtil: pip install MIDIUtil

# def notes2midi(notes, midi_path, track=0, channel=0, time=0, tempo=120, volume=100):
#     """ 
#     track    = 0
#     channel  = 0
#     time     = 0    # In beats
#     tempo    = 180   # In BPM
#     volume   = 127  # 0-127, as per the MIDI standard 
#     """

#     MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
#                         # automatically)
#     MyMIDI.addTempo(track, time, tempo)

#     for i, (pitch, duration) in enumerate(notes):
#         MyMIDI.addNote(track, channel, pitch, time + i, duration / 16, volume)

#     with open(midi_path, "wb") as output_file:
#         MyMIDI.writeFile(output_file)