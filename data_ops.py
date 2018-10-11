from mido import MidiFile
import os


# input: path to midi file
# output: list of chords (list of pitches)
def load_midifile_chords(path):
    midi = MidiFile(path)
    chords = []
    chord = []
    for msg in midi:
        if msg.type == "note_on":
            chord.append(msg.note)
        elif msg.type == "note_off" and msg.time > 0:
            chords.append(chord)
            chord = []
    return chords



def load_corpus(dir_path):
    corpus = []
    for filename in os.listdir(dir_path):
        print(filename)
        corpus.append(load_midifile_chords(dir_path + "//" + filename))
    return corpus

if __name__ == "__main__":
    corpus = load_corpus("midi_files")
    num_notes = 0
    num_chords = 0
    num_files = len(corpus)
    for file in corpus:
        num_chords += len(file)
        for chord in file:
            num_notes += len(chord)
    print(num_notes)
    print(num_chords)
    print(num_files)

"""
    8/14/2018: 495 midi files, 19125 chords, 97669 notes
    8/15/2018: 674, 27592, 140409
    8/25/18: 782, 32164, 164949
    8/29/18: 962, 38872, 198285

"""