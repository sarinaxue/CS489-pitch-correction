# CS489-pitch-correction

A Python implementation of pitch correction using the pYIN Pitch Detection Algorithm and Time-Domain Pitch-Synchronous Overlap-Add (TD-PSOLA) for WAV files.

`python pitch_correct.py [wav_filename]` will produce a plot of the original and target frequencies of the wav and produce a pitch corrected wav file.

Currently, pitch correcting to the closest frequency belonging to the equal temepered scale. This produces wrong estimations for notes and metallic sound. Will need to consider how to produce a more natural sound, whether that is writing our own PSOLA or using something like a phase vocoder instead.

# TDPSOLA Code from KAIST-MACLab
https://github.com/KAIST-MACLab/PyTSMod/blob/main/pytsmod/tdpsolatsm.py

# Misc
* If you're getting weird errors make sure you update numpy :)
