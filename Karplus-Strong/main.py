'''
Main function

Original author: Mahesh Venkitachalam

Slight modifications by me
'''

import os
import argparse
import time
import ks
import musicer
import pygame
import matplotlib.pyplot as plt
import numpy as np

def main():
    '''The main program'''

    parser = argparse.ArgumentParser(
        description="Generating sounds with Karplus Strong Algorithm"
        )
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    parser.add_argument("--music", action='store_true', required=False)
    args = parser.parse_args()

    #Create note player
    def_notes = {'C4': 262, 'Eb': 311, 'F': 349, 'G':391, 'Bb':466}

    note_player = ks.NotePlayer()
    print("Creating notes...")
    for name, freq in def_notes.items():
        filename = name + ".wav"
        if not os.path.exists(filename):
            data = ks.generate_note(freq)
            print(f"Creating {filename}...")
            ks.write_wave(filename, data)
        else:
            print(f"{filename} already exists, skipping...")

        note_player.add_note(name + ".wav")

    if args.play:
        while True:
            try:
                note_player.play_random()
                #rest = np.random.choice([1, 2, 4, 8], 1,
                #                        p=[0.15, 0.7, 0.1, 0.05])
                #time.sleep(0.25*rest[0])
                rest = np.random.choice([0.25, 0.5], 1,
                                        p=[0.66, 0.34])                                        
                time.sleep(rest[0])
            except KeyboardInterrupt:
                exit()

    if args.piano:
        #TODO: Fix this, doesn't work...
        mp_test = musicer.Musicer(channels=1, buffer=2048)
        mp_test.load_notes("notes5.txt")
        mp_test.load_notes("notes4.txt")
        mp_test.load_notes("notes3.txt")
        mp_test.load_notes("notes2.txt")
        #pygame.init()
        musicer.piano(4, 5, mp_test.note_dict)

    if args.music:
        #TODO: Add mutliproc to stop playing music
        mp_test = musicer.Musicer(channels=1, buffer=2048)
        mp_test.load_notes("notes5.txt")
        mp_test.load_notes("notes4.txt")
        mp_test.load_notes("notes3.txt")
        mp_test.load_notes("notes2.txt")

        mp_test.load_musics(mp_test.music_path)

        while True:
            print("\nSaved songs:")
            print("\n".join([f"{str(key)}- {val[0]}" for key, val in mp_test.song_dict.items()]))
            song_ind = int(input("Enter the number of the song (0 to leave): "))
            if song_ind is 0:
                break
            else:
                mp_test.play_music(mp_test.song_dict[song_ind][1])

if __name__ == "__main__":
    main()
