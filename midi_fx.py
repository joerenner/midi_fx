from mido import Message, MidiFile, MidiTrack
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
def build_track(chords, duration=2, name=""):
    print(chords)
    track = MidiTrack(name)
    current_time = 0
    for chord in chords:
        for msg in chord:
            print(current_time)
            track.append(Message('note_on', note=msg.note, velocity=100, time=current_time))
        current_time += duration
        for msg in chord:
            track.append(Message('note_off', note=msg.note, velocity=100, time=current_time))
    return track

if __name__ == "__main__":
    mido.set_backend('mido.backends.pygame')
    chords = record_midi()
    track = build_track(chords)
    for msg in track:
        print(msg)
    print(track)

