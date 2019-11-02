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
import matplotlib.pyplot as plt
import numpy as np

def main():
    '''The main program'''

    parser = argparse.ArgumentParser(
        description="Generating sounds with Karplus Strong Algorithm"
        )
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    parser.add_argument("--music", action='store_true', required=False)
    args = parser.parse_args()

    #Show plot if flag is set
    #if args.display:
    #    show_plot = True
    #    plt.ion()
    #else:
    #    show_plot = False

    #Create note player
    def_notes = {'C4': 262, 'Eb': 311, 'F': 349, 'G':391, 'Bb':466}

    note_player = ks.NotePlayer()
    print("Creating notes...")
    for name, freq in def_notes.items():
        filename = name + ".wav"
        if not os.path.exists(filename): #or args.display:
            data = ks.generate_note(freq)
            print(f"Creating {filename}...")
            ks.write_wave(filename, data)
        else:
            print(f"{filename} already exists, skipping...")

        note_player.add_note(name + ".wav")

        if args.display:
            note_player.play_note(name + ".wav")
            time.sleep(0.5)

    if args.play:
        while True:
            try:
                note_player.play_random()
                #rest = np.random.choice([1, 2, 4, 8], 1,
                #                        p=[0.15, 0.7, 0.1, 0.05])
                rest = np.random.choice([0.25, 0.5], 1,
                                        p=[0.66, 0.34])                                        
                #time.sleep(0.25*rest[0])
                time.sleep(rest[0])
            except KeyboardInterrupt:
                exit()

    if args.music:
        #TODO: Add a menu, I don't want to type the filename everytime
        mp_test = musicer.Musicer(channels=1, buffer=2048)
        mp_test.load_notes("notes5.txt")
        mp_test.load_notes("notes4.txt")
        mp_test.load_notes("notes3.txt")
        mp_test.load_notes("notes2.txt")

        while True:
            filename = input("Enter name of song file: ")
            if filename is "0":
                break
            mp_test.load_music(filename)

if __name__ == "__main__":
    main()
