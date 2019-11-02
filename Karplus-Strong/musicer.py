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

    def load_music(self, filename):
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
                except:
                	pass

                self.note_dict[cur_note].play()
                time.sleep(float(value) / rest)
