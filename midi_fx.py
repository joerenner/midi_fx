from mido import Message, MidiFile, MidiTrack
import mido

def glissando(note_on_message, note_off_message, length="constant", delta=1):

    new_messages = []


    return new_messages

def record_midi():
    with mido.open_input() as port:
        for msg in port:
            if msg.type == "note_on" and msg.velocity == 80:

                if msg.note == 36:
                    break


if __name__ == "__main__":
    mido.set_backend('mido.backends.pygame')
    record_midi()
    """for i, track in enumerate(mid.tracks):
        print(track.name)
        print(len(track))
        [print(msg) for msg in track]"""
