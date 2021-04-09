import copy
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

# get closest fundamental frequencies that belongs to scale
f_target = copy.copy(f0)
f_target[np.isnan(f0)] = 1 # all elements must be integers and non-zero to prevent division by zero
f_target = librosa.note_to_hz(librosa.hz_to_note(f_target))

# plot the frequencies
fig, ax = plt.subplots()
img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
ax.set(title='['+sys.argv[1]+'] Original vs Pitch Corrected')
fig.colorbar(img, ax=ax, format="%+2.f dB")
ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
f_target[f_target < 1.03] = np.nan # removes the ftarget rise/drop at beginning/end
ax.plot(times, f_target, label='ftarget', color='blue', linewidth=1)
ax.legend(loc='upper right')
plt.show()

# use PSOLA to move to desired fundamental frequency
signal_length = signal.shape[-1]
f_target[np.isnan(f_target)] = 0 # prevents audio from getting cut off
signal_pitch_corrected = tsm.tdpsola(signal, fs, f0, tgt_f0=f_target, p_hop_size=512, p_win_size=1024)
sf.write('./wav/'+sys.argv[1]+'_pitch_corrected.wav', signal_pitch_corrected, fs)


