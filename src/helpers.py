import pickle
import music21
import itertools
from src import MIN_PITCH_CHORALES, MAX_PITCH_CHORALES,\
                MIN_DUR_CHORALES, MAX_DUR_CHORALES,\
                PITCHES_CHORALES_M21, PITCHES_COMBINED_M21,\
                PITCHES_ALL_M21, DURATIONS_CHORALES_M21,\
                DURATIONS_COMBINED_M21, DURATIONS_ALL_M21

def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def get_pitches(dataset='chorales'):
    if dataset == 'chorales':
        return [i for i in range(MIN_PITCH_CHORALES, MAX_PITCH_CHORALES + 1)]
    elif dataset == 'chorales_m21':
        return PITCHES_CHORALES_M21
    elif dataset == 'm21':
        return PITCHES_COMBINED_M21
    elif dataset == 'all':
        return PITCHES_ALL_M21

def get_durations(dataset='chorales'):
    if dataset == 'chorales':
        return [i for i in range(MIN_DUR_CHORALES, MAX_DUR_CHORALES + 1)]
    elif dataset == 'chorales_m21':
        return DURATIONS_CHORALES_M21
    elif dataset == 'm21':
        return DURATIONS_COMBINED_M21
    elif dataset == 'all':
        return DURATIONS_ALL_M21

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

def get_datasets_equality_ratio(
    our_bach_music21_datasets: list, 
    bach_music21_datasets: list,
    thr=.9):

    equals_datasets = []
    for i_our, our_dataset in enumerate(our_bach_music21_datasets):
        for i_m21, m21_dataset in enumerate(bach_music21_datasets):
            equals = 0
            k = 0
            if len(our_dataset) <= len(m21_dataset):
                for our_elem in our_dataset:
                    while k < len(m21_dataset) and m21_dataset[k] != our_elem:
                        k += 1
                    if k < len(m21_dataset):
                        equals += 1
                        k += 1
            else:
                for m21_elem in m21_dataset:
                    while k < len(our_dataset) and m21_elem != our_dataset[k]:
                        k += 1
                    if k < len(our_dataset):
                        equals += 1  
                        k += 1 
            if equals / min(len(m21_dataset), len(our_dataset)) > thr:
                equals_datasets.append((i_our, i_m21, equals, min(len(m21_dataset), len(our_dataset))))
    return equals_datasets

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