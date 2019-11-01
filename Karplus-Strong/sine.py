import wave
import math
import numpy as np

samp_rate = 44100
samples = samp_rate * 5

x = np.arange(samples) / float(samp_rate)
vals = np.sin(2.0*math.pi*220*x)

#32767 because it is max int16 value or something...
data = np.array(vals*32767, 'int16').tostring()

file = wave.open('sine.wav', 'wb')
file.setparams((1, 2, samp_rate, samples, 'NONE', 'uncompressed'))
file.writeframes(data)
file.close
