import copy
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pytsmod as tsm
import soundfile as sf
import sys

def findClosestFreq(f0, freqs):
    left, right = 0, len(freqs) - 1
    index = left
    while left <= right:
        mid = left + (right - left) // 2
        if freqs[mid] < f0:
            left = mid + 1
        elif freqs[mid] > f0:
            right = mid - 1
        else:
            index = mid
            break
        if abs(freqs[mid] - f0) < abs(freqs[index] - f0):
            index = mid
    return freqs[index]


def estimateKey(signal, fs):
    chroma_cq = librosa.feature.chroma_cqt(y=signal,sr=fs,fmin=65.41,n_octaves=5) # C2=65.41Hz, 5 octaves to C7
    # plot the chromagram
    """
    fig, ax = plt.subplots()
    img = librosa.display.specshow(chroma_cq, y_axis='chroma', x_axis='time', ax=ax)
    ax.set(title=key+' chroma_cqt')
    fig.colorbar(img, ax=ax)
    plt.show()
    """
    keys = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    key_id = np.argmax(np.sum(chroma_cq, axis=1)) # estimate more frequent note as the root note
    key = keys[key_id] 
    # determine if major or minor
    min_third_id = (key_id+3)%12
    maj_third_id = (key_id+4)%12
    if np.sum(chroma_cq[min_third_id]) > np.sum(chroma_cq[maj_third_id]):
        key+=':min'
    else:
        key+=':maj' # most songs are major, so default to major if equal amount
    return key

# get all frequencies in the scale from C2 to C7
def getTargetFreqs(f0, key=None):
    f_target = copy.copy(f0)
    f_target[np.isnan(f0)] = 1 # all elements must be integers and non-zero to prevent division by zero
    try:
        octave_freqs = librosa.note_to_hz(map(lambda note: note + '2', librosa.key_to_notes(key))) 
    except:
        return librosa.note_to_hz(librosa.hz_to_note(f_target))
    octave_freqs[0] /= 2 # strangely, the first note is actually in the next octave, so bring it back down
    possible_freqs = []
    possible_freqs = copy.copy(octave_freqs)
    for _x in range(6):
        octave_freqs *= 2
        possible_freqs = np.concatenate((possible_freqs, octave_freqs), axis=None)
    for i, freq in enumerate(f_target):
        f_target[i] = findClosestFreq(freq, possible_freqs)
    return f_target


# CLI arguments:
# string - name of audio file
# string (optional) - key to correct to
# string (optional) - if 1, use hpss to remove transients before correcting
def main():
    y, fs = librosa.load('./wav/'+sys.argv[1]+'.wav')
    signal = y
    use_hpss = False
    if len(sys.argv) >= 4:
        if (sys.argv[3] == '1'):
            use_hpss = True
            signal_harmonic, _signal_percussive = librosa.effects.hpss(y, margin=(1,3), kernel_size=17)
            signal = signal_harmonic # use only harmonic component in key estimation /pitch detection/pitch correction
    
    # PITCH DETECTION: detect original fundamental frequencies with pYIN
    f0, _voiced_flag, _voiced_probs = librosa.pyin(signal, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

    # check if key was passed as an argument
    key = None
    if len(sys.argv) >= 3:
        if sys.argv[2] == 'estimate':
            key = estimateKey(signal, fs)
        else:
            key = sys.argv[2]
        print("Pitch correcting to: " + key + " key")
        f_target = getTargetFreqs(f0, key)
    else:
        f_target = getTargetFreqs(f0)
    # print(f_target)

    # plot the original and target frequencies
    fig, ax = plt.subplots()
    times = librosa.times_like(f0)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
    ax.set(title='['+sys.argv[1]+'] Original vs Target')
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
    f_target[f_target < 65.41] = np.nan # removes the ftarget rise/drop at beginning/end
    ax.plot(times, f_target, label='ftarget', color='blue', linewidth=1)
    ax.legend(loc='upper right')
    plt.show()
    
    # PITCH CORRECTION: use PSOLA to move to desired target frequency
    f_target[np.isnan(f_target)] = 0 # prevents audio from getting cut off
    signal_pitch_corrected = tsm.tdpsola(y, fs, f0, tgt_f0=f_target, p_hop_size=512, p_win_size=1024)

    filename = './wav/'+sys.argv[1]+'_pitch_corrected'
    if (key != None):
        filename += '_' + key.replace(':','')
    if (use_hpss == 1):
        filename += '_hpss'
    filename += '.wav'
    sf.write(filename, signal_pitch_corrected, fs)
    print('File saved to ' + filename)

if __name__ == "__main__":
    main()