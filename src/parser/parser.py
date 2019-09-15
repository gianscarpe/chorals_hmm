import os
import pickle
import numpy
import music21
import itertools
from src import DATA_DIR
from src.helpers import save_pickle, load_pickle, get_pitch_space

def tokenize(chars):
    if type(chars) == bytes:
        chars = chars.decode("utf-8")
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def tokens2notes(tokens):
    i = 0
    note = []
    notes = []
    while i < len(tokens) - 1:
        if tokens[i] != '(' and tokens[i] != ')' and (tokens[i] == 'pitch' or tokens[i] == 'dur'):
            note.extend([int(tokens[i+1])])
            i += 2
        elif tokens[i] == tokens[i+1] == ')':
            notes.append(tuple(note))
            note = []
            i += 1
        else:
            i += 1
    return notes

def parse_dataset(data_path):
    with open(data_path, 'rb') as f:
        chorales = []
        for line in f.readlines():
            tokens = tokenize(line)
            if tokens != []:
                tokens.pop(0) # remove first '('
                tokens.pop(0) # remove chorales number
                tokens.pop()  # remove last ')'
                chorale_notes = tokens2notes(tokens)
                chorales.append(chorale_notes)
        return chorales

def tokens2music21(tokens):
    i = 0
    offset = 0
    keysig = None
    timesig = None
    notes = []
    while i < len(tokens) - 1:
        if tokens[i] != '(' and tokens[i] != ')':
            if tokens[i] == 'st':
                offset += int(tokens[i+1]) / 4
            elif tokens[i] == 'pitch':
                pitch = music21.pitch.Pitch()
                pitch.midi = int(tokens[i+1])
            elif tokens[i] == 'dur':
                duration = music21.duration.Duration(type='quarter')
                duration.quarterLength = int(tokens[i+1]) / 4
            elif tokens[i] == 'keysig':
                if keysig is None:
                    keysig = music21.key.KeySignature()
                    keysig.sharps = int(tokens[i+1])
            elif tokens[i] == 'timesig':
                if timesig is None:
                    timesig = music21.meter.TimeSignature()
                    timesig.numerator = int(int(tokens[i+1]) / 4)
                    timesig.denominator = 4
            i += 2
        elif tokens[i] == tokens[i+1] == ')':
            note = music21.note.Note()
            note.pitch = pitch
            note.duration = duration
            note.offset = offset
            notes.append(note)
            i += 1
        else:
            i += 1
    return keysig, timesig, notes

def dataset2music21(data_path):
    with open(data_path, 'rb') as f:
        streams = []
        for line in f.readlines():
            tokens = tokenize(line)
            if tokens != []:
                tokens.pop(0) # remove first '('
                tokens.pop(0) # remove chorales number
                tokens.pop()  # remove last ')'
                keysig, timesig, notes = tokens2music21(tokens)
                stream = music21.stream.Stream()
                stream.keySignature = keysig
                stream.timeSignature = timesig
                stream.append(notes)
                streams.append(stream.makeMeasures())
        return streams

def states2stream(states, vocab):
    stream = music21.stream.Stream()
    notes = []
    for state in states:
        (ps, dur) = vocab[state]
        # Set duration
        duration = music21.duration.Duration(type='quarter')
        duration.quarterLength = dur / 4
        # Set pitch
        pitch = music21.pitch.Pitch()
        pitch.midi = ps
        # Create note
        note = music21.note.Note()
        note.pitch = pitch
        note.duration = duration
        notes.append(note)
    stream.append(notes)
    return stream.makeMeasures()

def states2notes(states, vocab):
    return [vocab[state] for state in states]

def dataset2states(data_path, vocab):
    dataset = parse_dataset(data_path)
    parsed_dataset = []
    for chorale in dataset:
        parsed_dataset.append([vocab.index(note) for note in chorale])
    return parsed_dataset

if __name__ == 'main':
    vocab_path = os.path.join(DATA_DIR, 'bach_chorales', 'vocab.pkl')
    data_path = os.path.join(DATA_DIR, 'bach_chorales', 'dataset.dt')
    parsed_data_path = os.path.join(DATA_DIR, 'bach_chorales', 'parsed_dataset.pkl')

    # save_pickle(get_pitch_space(), vocab_path)
    # vocab = load_pickle(vocab_path)
    # parsed_dataset = dataset2states(data_path, vocab)
    # save_pickle(parsed_dataset, parsed_data_path)

    music21.environment.set('musicxmlPath', '/usr/bin/musescore')
    streams = dataset2music21(data_path)
    chorale_num = 5
    streams[chorale_num].show()
    mf = music21.midi.translate.streamToMidiFile(streams[chorale_num])
    mf.open('midi.mid', 'wb')
    mf.write()
    mf.close()

    # scores = music21.corpus.search('bach', 'composer')
    # music21_bach = scores[5].parse().parts['Soprano']
    # music21_bach.show()
    # mf = music21.midi.translate.streamToMidiFile(music21_bach)
    # mf.open('music21_bach.mid', 'wb')
    # mf.write()
    # mf.close()