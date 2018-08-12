from mido import Message, MidiFile, MetaMessage, MidiTrack
import mido
import time

def glissando(note_on_message, note_off_message, length="constant", delta=1):

    new_messages = []


    return new_messages


# records from input port
# returns list of lists of midi messages, inner list correspond to messages that are chords
def record_midi():
    with mido.open_input() as port:
        last_time = time.time()
        current_chord = []
        chords = []
        for msg in port:
            if msg.type == "note_on" and msg.velocity == 80:
                new_time = time.time()
                delta = new_time - last_time
                if delta > 1.5:
                    last_time = new_time
                    if current_chord:
                        chords.append(sorted(current_chord, key=lambda x: x.note))
                    current_chord = [msg]
                else:
                    current_chord.append(msg)
            if time.time() - last_time > 4.0:
                break
        if current_chord:
            chords.append(sorted(current_chord, key=lambda x: x.note))
        return chords

# build midi track from list of chords
def build_track(chords, duration=8, name="", bpm=120):
    ticks_per_beat = 480
    duration = int(ticks_per_beat / (duration / 4))
    track = MidiTrack(name)
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
    track.append(MetaMessage('time_signature', numerator = 4, denominator = 4))
    for chord in chords:
        for i in range(len(chord)):
            track.append(Message('note_on', note=chord[i].note, velocity=100, time=0))
        for i in range(len(chord)):
            track.append(Message('note_off', note=chord[i].note, velocity=0, time=duration if i == 0 else 0))
    track.append(MetaMessage('end_of_track'))
    return track

def save_midi(tracks, file_name="test.mid"):
    outfile = MidiFile()
    for track in tracks:
        outfile.tracks.append(track)
    outfile.save(file_name)

if __name__ == "__main__":
    mido.set_backend('mido.backends.pygame')
    #test = MidiFile('test.mid')
    chords = record_midi()
    track = build_track(chords, 1)
    save_midi([track], "test2.mid")

