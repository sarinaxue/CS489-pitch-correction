import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import pytsmod as tsm
import sys

y, sr = librosa.load(sys.argv[1]+'.wav')
f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
times = librosa.times_like(f0)
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
fig, ax = plt.subplots()
img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
ax.set(title='pYIN')
fig.colorbar(img, ax=ax, format="%+2.f dB")
ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
ax.legend(loc='upper right')
plt.show()
x = y.T
x_length = x.shape[-1]  # length of the audio sequence x.
x_pitch_corrected = tsm.tdpsola(x, sr, f0)
sf.write(sys.argv[1]+'_autocorrected.wav', x_pitch_corrected, sr)


