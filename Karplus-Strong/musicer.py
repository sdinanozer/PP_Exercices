'''
File for class 'Musicer'.
Creates 3 octaves (for now) of notes from .txt 
files using Kasper-Strong algorithm and can play
music from .txt file.
'''

import os
import pygame
import time
import ks

class Musicer:
    '''Makes music obviously'''
    note_path = "./Notes"
    music_path = "./Musics"
    note_dict = {}
    octave_dict = {}
    song_dict = {}

    def __init__(self, sampling_freq=44100, size=-16,
                 channels=2, buffer=512):
        pygame.mixer.pre_init(sampling_freq, size, channels, buffer)
        pygame.init()
    
    def add_note(self, name):
        filename = ".".join((name, "wav"))
        filename = os.path.join(Musicer.note_path, filename)
        self.note_dict[name] = pygame.mixer.Sound(filename)

    def play_notes(self, note_arr):
        for note_name in note_arr:
            note = self.note_dict[note_name]
            note.play()

    def load_notes(self, filename):
        filename = os.path.join(Musicer.note_path, filename)

        with open(filename, 'r') as file:
            octave = file.readline().rstrip().split(",")
            self.octave_dict[int(octave[1])] = octave[0]

            for line in file:
                name, freq = line.rstrip().split(",")
                print(f"Loading {name} with {freq}Hz")
                #Name of the note.wav file
                wav_filename = name + octave[1] + ".wav"
                #Path to the note.wav file
                wav_filepath = os.path.join(Musicer.note_path, wav_filename)

                if not os.path.exists(wav_filepath):
                    print(f"Creating {wav_filename}...")
                    data = ks.generate_note(float(freq))
                    ks.write_wave(wav_filepath, data)
                else:
                    print(f"{wav_filename}4.wav already exists, skipping...")

                self.note_dict[name+octave[1]] = pygame.mixer.Sound(wav_filepath)

            print(f"Loaded {octave[0]} ({octave[1]}th octave).")

    def load_musics(self, path):
        directory = os.fsencode(path)
        for d, music_file in enumerate(os.listdir(directory), start=1):
            filename = os.fsdecode(music_file)
            filepath = os.path.join(path, filename)
            if filename.endswith(".txt"):
                with open(filepath, "r") as file:
                    self.song_dict[d] = (file.readline().rstrip(), filename)

    def play_music(self, filename):
        #TODO: Add multiprocessing to display timer & stop a playing song
        filename = os.path.join(Musicer.music_path, filename)

        with open(filename, 'r') as file:
            name = file.readline().rstrip()
            artist = file.readline().rstrip()
            print(f"Now playing {name} by {artist}...")

            bpm = int(file.readline().rstrip())
            rest = bpm / 60

            for line in file:
                #Value of a whole note being 4
               	try:
                	cur_note, value = line.split(",")
                	self.note_dict[cur_note].play()
                	time.sleep(float(value) / rest)
                except:
                	pass

#Don't know why it doesn't work
'''
def piano(oct1, oct2, notes):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    notes["C"+str(oct1)].play()
                if event.key == pygame.K_w:
                    notes["D"+str(oct1)].play()
                if event.key == pygame.K_e:
                    notes["E"+str(oct1)].play()
                if event.key == pygame.K_r:
                    notes["F"+str(oct1)].play()
                if event.key == pygame.K_t:
                    notes["G"+str(oct1)].play()
                if event.key == pygame.K_y:
                    notes["A"+str(oct1)].play()
                if event.key == pygame.K_u:
                    notes["B"+str(oct1)].play()
                if event.key == pygame.K_2:
                    notes["C#"+str(oct1)].play()
                if event.key == pygame.K_3:
                    notes["D#"+str(oct1)].play()
                if event.key == pygame.K_5:
                    notes["F#"+str(oct1)].play()
                if event.key == pygame.K_6:
                    notes["G#"+str(oct1)].play()
                if event.key == pygame.K_7:
                    notes["A#"+str(oct1)].play()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
'''
