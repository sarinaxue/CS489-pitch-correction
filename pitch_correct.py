import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pytsmod as tsm
import soundfile as sf
import sys

# detect original fundamental frequencies with pYIN
signal, fs = librosa.load('./wav/'+sys.argv[1]+'.wav')
f0, voiced_flag, voiced_probs = librosa.pyin(signal, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
times = librosa.times_like(f0)
D = librosa.amplitude_to_db(np.abs(librosa.stft(signal)), ref=np.max)
fig, ax = plt.subplots()
img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
ax.set(title='pYIN')
fig.colorbar(img, ax=ax, format="%+2.f dB")
ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
ax.legend(loc='upper right')
plt.show()

# get closest fundamental frequencies that belongs to scale
# TODO: change this to take in a scale and find closest frequency
f_target = f0

# use PSOLA to move to desired fundamental frequency
signal_length = signal.shape[-1]
signal_pitch_corrected = tsm.tdpsola(signal, fs, f0, f_target)
sf.write('./wav/'+sys.argv[1]+'_pitch_corrected.wav', signal_pitch_corrected, fs)


