# CS489-pitch-correction

A Python implementation of pitch correction using the pYIN Pitch Detection Algorithm and Time-Domain Pitch-Synchronous Overlap-Add (TD-PSOLA) for WAV files.

`python pitch_correct.py [wav_filename] [key]` will produce a plot of the original and target frequencies of the wav and produce a pitch corrected wav file. Note, the wav file should be located in the /wav folder. Key is an optional argument. By default, the original frequencies will be compared against all possible musical frequencies. Specifying "estimate" for the key param will give a best guess on the key the song is in based on the most frequent note (assumption that it is the root) and limit the target frequencies to notes in the estimated key. Specifying something along the lines of "A#:maj" or "C:min" will limit the target frequencies to the specified key.

# TDPSOLA Code from KAIST-MACLab
https://github.com/KAIST-MACLab/PyTSMod/blob/main/pytsmod/tdpsolatsm.py

# Misc
* If you're getting weird errors make sure you update numpy :)
