from mido import Message, MidiFile, MetaMessage, MidiTrack
import mido
import time


# input: denominator of note length (8 is 8th note, 1 is whole note, 1/2 is 2 measures)
# output: time argument for message
def note_duration_to_time_delta(duration):
    ticks_per_beat = 480
    return int(ticks_per_beat / (duration / 4))


def velocity_scale_chord(chord, min_vel, max_vel, num_notes):
    new_chord = []
    chord.sort(key=lambda x: x.note)
    vel_delta = int((max_vel - min_vel) / (num_notes - 1))
    for i in range(num_notes):
        new_chord.append(chord[i].copy(velocity=min_vel+(i*vel_delta)))
    return new_chord


# input: track of quantinized chords
# output: track of same chords, with higher notes having higher velocities
def velocity_scaling(track, min_vel=80, max_vel=127, single_vel=100):
    new_track = MidiTrack()
    chord = []
    num_notes = 0
    for msg in track:
        if msg.type == "note_on":
            chord.append(msg)
            num_notes += 1
        elif chord and msg.type == "note_off":
            if num_notes == 1:
                new_track.append(chord[0].copy(velocity=single_vel))
            else:
                [new_track.append(x) for x in velocity_scale_chord(chord, min_vel, max_vel, num_notes)]
            chord = []
            num_notes = 0
            new_track.append(msg)
        else:
            new_track.append(msg)
    return new_track


# input: track of quantinized chords
# output: track of glissando chords
def glissando(track, delta=64):
    new_track = MidiTrack()
    delta = note_duration_to_time_delta(delta)
    bottom_note_on = True
    num_notes = 0
    for msg in track:
        if msg.type == "note_on":
            if not bottom_note_on:
                msg = msg.copy(time=delta)
                num_notes += 1
            else:
                bottom_note_on = False
        elif not bottom_note_on and msg.type == "note_off":
            bottom_note_on = True
            new_time = msg.time - num_notes * delta
            msg = msg.copy(time=new_time)
            num_notes = 0
        new_track.append(msg)
    return new_track


# input: track of quantinized chords
# output: track of glissando chords
def transpose(track, factor):
    new_track = MidiTrack()
    for msg in track:
        if msg.type == "note_on" or msg.type == "note_off":
            msg = msg.copy(note=msg.note+factor)
        new_track.append(msg)
    return new_track


def transpose_octave_and_save(track, file_prefix):
    for i in range(-6, 6):
        if not i == 0:
            save_midi([transpose(track, i)], file_prefix + str(i) + ".mid")
        else:
            save_midi([track], file_prefix + str(i) + ".mid")


# records from input port
# returns list of lists of midi messages, inner list correspond to messages that are chords
def record_midi_chords(chord_time=1.5, end_time=4.0):
    with mido.open_input() as port:
        last_time = time.time()
        current_chord = []
        chords = []
        for msg in port:
            if msg.type == "note_on" and msg.velocity == 80:
                new_time = time.time()
                delta = new_time - last_time
                if delta > chord_time:
                    last_time = new_time
                    if current_chord:
                        chords.append(sorted(current_chord, key=lambda x: x.note))
                    current_chord = [msg]
                else:
                    current_chord.append(msg)
            if time.time() - last_time > end_time:
                break
        if current_chord:
            chords.append(sorted(current_chord, key=lambda x: x.note))
        return chords


# build midi track from list of chords
def build_track(chords, duration=8, name="", bpm=120):
    duration = note_duration_to_time_delta(duration)
    track = MidiTrack(name)
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
    track.append(MetaMessage('time_signature', numerator=4, denominator=4))
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


def record_song(prefix_path, min_time_next_chord=0.5, end_time=6.0):
    for i in range(1,4):
        print("version {}".format(i))
        chords = record_midi_chords(min_time_next_chord, end_time)
        track = build_track(chords, 1)
        transpose_octave_and_save(track, prefix_path + "{}_".format(i))

if __name__ == "__main__":
    mido.set_backend('mido.backends.pygame')
    # test = MidiFile('midi_files/aguadebeber_samplehighs.mid')
    name = "armageddon"
    record_song("midi_files/" + name)
    """
    chords = record_midi_chords(0.5, 6.0)
    track = build_track(chords, 1)
    transpose_octave_and_save(track,  "midi_files/chords" + str(time.time()))
    track = velocity_scaling(track)
    track = glissando(track, 48)
    save_midi([track], "chords.mid")
"""
