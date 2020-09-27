#!/usr/bin/env python

from scipy.io import wavfile
import os
import numpy as np
import argparse
from tqdm import tqdm
import matplotlib.pyplot as plt
import math
# Utility functions

def windows(signal, window_size, step_size):
    if type(window_size) is not int:
        raise AttributeError("Window size must be an integer.")
    if type(step_size) is not int:
        raise AttributeError("Step size must be an integer.")
    for i_start in range(0, len(signal), step_size):
        i_end = i_start + window_size
        if i_end >= len(signal):
            break
        yield signal[i_start:i_end]

def energy(samples):
    return np.sum(np.power(samples, 2.)) / float(len(samples))

def db(samples):
    db = float('-inf')
    for sample in samples:
        amplitude = abs(sample)/ max_amplitude
        print(amplitude)
        db = max(db,20 * math.log10(amplitude + math.pow(10,-8)))
        print(db)
    return db

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)
    
def rising_edges(binary_signal):
    previous_value = 0
    index = 0
    for x in binary_signal:
        if x and not previous_value:
            yield index
        previous_value = x
        index += 1

# Process command line arguments
#outdoor silence threshold = 5e-6
#indoor silence threshold 5e-5

#######  split audio based on energy in frequency window
parser = argparse.ArgumentParser('split teeth bite sample based on sound energy')
parser.add_argument('input_file', type=str, help='The WAV file to split.')
parser.add_argument('--output-dir', '-o', type=str, default='.', help='The output folder. Defaults to the current folder.')
parser.add_argument('--min-silence-length', '-m', type=float, default=0.2, help='The minimum length of silence at which a split may occur [seconds]. Defaults to 3 seconds.')
parser.add_argument('--silence-threshold', '-t', type=float, default=2e-5, help='The energy level (between 0.0 and 1.0) below which the signal is regarded as silent. Defaults to 1e-6 == 0.0001%.')
parser.add_argument('--step-duration', '-s', type=float, default=None, help='The amount of time to step forward in the input file after calculating energy. Smaller value = slower, but more accurate silence detection. Larger value = faster, but might miss some split opportunities. Defaults to (min-silence-length / 10.).')
parser.add_argument('--dry-run', '-n', action='store_true', help='Don\'t actually write any output files.')

args = parser.parse_args()

input_filename = args.input_file
window_duration = args.min_silence_length

if args.step_duration is None:
    step_duration = window_duration
else:
    step_duration = args.step_duration
silence_threshold = args.silence_threshold
output_dir = args.output_dir
output_filename_prefix = os.path.splitext(os.path.basename(input_filename))[0]
dry_run = args.dry_run
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Read and split the file

sample_rate, samples = input_data=wavfile.read(filename=input_filename, mmap=True)

max_amplitude = np.iinfo(samples.dtype).max
max_energy = energy([max_amplitude])

window_size = int(window_duration * sample_rate)
step_size = int(step_duration * sample_rate)

signal_windows = windows(
    signal=samples,
    window_size=window_size,
    step_size=step_size
)

# window_energy = (energy(w) / max_energy for w in tqdm(
#     signal_windows,
#     total=int(len(samples) / float(step_size))
# ))

window_energy = (energy(w) / max_energy for w in signal_windows)
energy_list = []
for w in window_energy:
    # print(w,w < silence_threshold)
    energy_list.append(w)

thres_list = [silence_threshold]*len(energy_list)
plt.plot(energy_list)
plt.plot(thres_list)
axes = plt.gca()
axes.set_ylim([0,10e-5])
plt.show()

signal_windows = windows(
    signal=samples,
    window_size=window_size,
    step_size=step_size
)

window_energy = (energy(w) / max_energy for w in signal_windows)
window_silence = (e < silence_threshold for e in window_energy)

cut_times = (r * step_duration for r in rising_edges(window_silence))

# This is the step that takes long, since we force the generators to run.
cut_samples = [int(t * sample_rate) for t in cut_times]
cut_samples.append(-1)
# print("Cut samples: ",cut_samples)
for i in cut_samples:
    print(i/48000)
cut_ranges = [(i, cut_samples[i]-1*window_size, cut_samples[i]+1*window_size) for i in range(len(cut_samples) - 1)]

for i, start, stop in tqdm(cut_ranges):
    output_file_path = "{}_{:.02f}.wav".format(
        os.path.join(output_dir, output_filename_prefix),
        start/48000,
    )
    if not dry_run:
        # print ("Writing file {}".format(output_file_path))
        wavfile.write(
            filename=output_file_path,
            rate=sample_rate,
            data=samples[start:stop]
        )
    else:
        print ("Not writing file {}".format(output_file_path))