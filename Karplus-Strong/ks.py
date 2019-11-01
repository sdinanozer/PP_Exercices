'''
Uses the Karplus-Strong algorithm to generate musical notes.

Original author: Mahesh Venkitachalam
'''

import random
import wave
import pygame
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def generate_note(freq):
    samp_rate = 44100
    samples_num = 44100
    N = int(samp_rate/freq)

    #Initialize ring buffer.
    ring_buf = deque([random.random() - 0.5 for d in range(N)])

    #Initialize samples buffer.
    samples = np.array([0]*samples_num, 'float32')

    #Apply the Karplus-Strong algorithm
    #Or low pass filter I dont know
    for d in range(samples_num):
        samples[d] = ring_buf[0]
        average = 0.995*(ring_buf[0]+ring_buf[1])/2
        ring_buf.append(average)
        ring_buf.popleft()

    #Convert samples to 16-bit and then to a string
    #Max value for 16-bit is 32767
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()

def write_wave(fname, data):
    #Opening the file
    file = wave.open(fname, 'wb')
    channels = 1
    sample_width = 2
    frame_rate = 44100
    frames = 44100
    #Setting parameters
    file.setparams((channels, sample_width, frame_rate,
                    frames, 'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()

#Plays a WAV file
class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        self.notes = {}

    def add_note(self, filename):
        self.notes[filename] = pygame.mixer.Sound(filename)

    def play_note(self, filename):
        try:
            self.notes[filename].play()
        except:
            print(f"{filename} not found!")

    def play_random(self):
        index = random.randint(0, len(self.notes) - 1)
        note = list(self.notes.values())[index]
        note.play()
