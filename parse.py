import os
import sys
import math
import music21
import argparse
import itertools
from os import path
from fractions import Fraction
from src import DATA_DIR
from src.parser.parser import dataset2states, chorales2music21_streams, parse_music21_dataset
from src.helpers import save_pickle, load_pickle, get_pitch_space, get_datasets_equality_ratio


class CommandParser(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Pretends to be git',
            usage='''parse.py <command> [<args>]

            The most commonly commands are:
            music21     Search songs by author and instrument from music21 corpuses, 
                        or parse our dataset
            fetch       Download objects and refs from another repository
            '''
        )
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def music21(self):
        parser = argparse.ArgumentParser(
            description='Search artists from music21 corpus or parse our dataset',
            usage='''parse.py music21 [<args>]'''
        )
        parser.add_argument(
            '--path',
            default=DATA_DIR,
            action='store'
        )
        parser.add_argument(
            '--author', 
            default='bach',
            action='store'
        )
        parser.add_argument(
            '--instrument', 
            default='soprano',
            action='store'
        )
        parser.add_argument(
            '--transposing-key', 
            default='C',
            action='store'
        )
        parser.add_argument(
            '--to-states',
            action='store_true'
        )
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        args.path = path.abspath(args.path)
        m21_dataset = parse_music21_dataset(args.author, args.instrument, args.transposing_key)
        if args.author == 'our':
            name = 'chorales_dataset.pkl'
            dirname = path.join(args.path, 'chorales', 'music21')
        else:
            name = args.author + '_dataset.pkl'
            dirname = path.join(args.path, 'music21')
        if not path.exists(dirname):
            os.makedirs(dirname)
        filename = path.join(dirname, name)
        print('Saving parsed dataset to {}'.format(filename))
        save_pickle(m21_dataset, filename)
        if args.to_states:
            if path.exists(path.join(dirname, 'vocab.pkl')):
                vocab = load_pickle(path.join(dirname, 'vocab.pkl'))
            else:
                print('You have to create the vocabulary first!\nRun parse.py vocab -h to see options')
                exit(1)
            if args.author == 'our':
                m21_states_dataset = dataset2states(m21_dataset, vocab, our=True)
                name = 'chorales_states_dataset.pkl'
            else:
                m21_states_dataset = dataset2states(m21_dataset, vocab, our=False)
                name = args.author + '_states_dataset.pkl'
            filename = path.join(dirname, name)
            print('Saving states dataset to {}'.format(filename))
            save_pickle(m21_states_dataset, filename)

    def vocab(self):
        parser = argparse.ArgumentParser(
            description='Create vocabs needed to translate a song into a set of states',
            usage='''parse.py vocab [<args>]'''
        )
        parser.add_argument(
            'path',
            default=DATA_DIR,
            action='store'
        )
        parser.add_argument(
            '--to-states',
            action='store_true'
        )
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        args.path = path.abspath(args.path)
        datasets_in_dir = [
            filename for filename in os.listdir(args.path) 
            if filename.endswith('dataset.pkl') and not 'states' in filename
        ]
        if datasets_in_dir != []:
            pitches = []
            durations = []
            loaded_datasets = []
            for dataset in datasets_in_dir:
                dataset = load_pickle(path.join(args.path, dataset))
                loaded_datasets.append(dataset)
                for song in dataset:
                    for note in song:
                        if note['pitch'] not in pitches:
                            pitches.append(note['pitch'])
                        if note['duration'] not in durations:
                            durations.append(note['duration'])          
            pitches = list(set(pitches))
            durations = list(set(durations))
            vocab = list(itertools.product(pitches, durations))
            print('Vocab length: ', len(vocab))
            print('Saving vocabs to {}'.format(path.join(args.path, 'vocab.pkl')))
            save_pickle(vocab, path.join(args.path, 'vocab.pkl'))
        else:
            print('Specify a folder in which there\'s at least one dataset')
            exit(1)
        if args.to_states:
            if loaded_datasets != []:
                if 'chorales' in args.path:
                    states_dataset = dataset2states(loaded_datasets[0], vocab, our=False)
                    name = 'chorales_states_dataset.pkl'
                    filename = path.join(args.path, name)
                    print('Saving states dataset to {}'.format(filename))
                    save_pickle(states_dataset, filename)
                else:
                    for i, dataset in enumerate(loaded_datasets):
                        states_dataset = dataset2states(dataset, vocab, our=False)
                        name = datasets_in_dir[i].split('_')[0] + '_states_dataset.pkl'
                        filename = path.join(args.path, name)
                        print('Saving states dataset to {}'.format(filename))
                        save_pickle(states_dataset, filename)
            else:
                print('Get some dataset before! Run parse.py music21 -h to get info')
                exit(1)

if __name__ == '__main__':
    CommandParser()

# vocab_path = path.join(DATA_DIR, 'music21', 'vocab.pkl')
# data_path = path.join(DATA_DIR, 'music21', 'bach_dataset.pkl')
# parsed_data_path = path.join(DATA_DIR, 'music21', 'bach_states_dataset.pkl')

# save_pickle(get_pitch_space(dataset='m21'), vocab_path)
# vocab = load_pickle(vocab_path)
# print(len(vocab), '\n', vocab)
# parsed_dataset = dataset2states(data_path, vocab, our=False)
# print(parsed_dataset)
# save_pickle(parsed_dataset, parsed_data_path)

# pitches = []
# durations = []
# bach_music21_datasets = []
# bach_music21_datasets = parse_music21_dataset(author='bach', instrument='viola')
# bach_music21_datasets = load_pickle(path.join(DATA_DIR, 'music21', 'bach_dataset.pkl'))
# for dataset in bach_music21_datasets:
#     for elem in dataset:
#         if elem['pitch'] not in pitches:
#             pitches.append(elem['pitch'])
#         if elem['duration'] not in durations:
#             durations.append(elem['duration'])
# pitches.sort()
# durations.sort()
# print(pitches, durations)
# streams = chorales2music21_streams()
# our_bach_music21_datasets = parse_music21_dataset(our=True, streams=streams)
# bach_music21_datasets = load_pickle(path.join(DATA_DIR, 'music21', 'bach_dataset.pkl'))
# our_bach_music21_datasets = load_pickle(path.join(DATA_DIR, 'bach_chorales', 'music21', 'm21_dataset.pkl'))
# print(get_datasets_equality_ratio(our_bach_music21_datasets, bach_music21_datasets))
# combined = bach_music21_datasets + our_bach_music21_datasets
# print(combined)
# print(len(bach_music21_datasets))
# save_pickle(bach_music21_datasets, path.join(DATA_DIR, 'music21', 'beethoven_dataset.pkl'))