#!/usr/bin/env python

from scipy.io import wavfile
import os
import numpy as np
import argparse
from tqdm import tqdm
import matplotlib.pyplot as plt
import json


# run the script: python3 split_audio_timestamp.py wavfile_path -s start_time -e end_time 
###### split audio based on json file
parser = argparse.ArgumentParser(description='split teeth bite sample based on json timestamps')
parser.add_argument('input_file', type=str, help='The WAV file to split.')
parser.add_argument('--start-time','-s',type=float,default=600,help='start time of an audio clip')
parser.add_argument('--end-time','-e',type=float,default=300,help='end time of an audio clip')
parser.add_argument('--sample-length','-l',type=float,default=50,help='length of bite audio clip in ms')
parser.add_argument('--window-step','-w',type=float,default=2,help='stride step across audio clip')
parser.add_argument('--dry_run','-d',type=bool,default=False,help='whether run to see less than two bites inside an audio clip')
args = parser.parse_args()

input_filename = args.input_file
basename = input_filename.split('.')[0]
print(basename)

json_file = basename + '.json'
output_dir = basename 
start_time = args.start_time
end_time = args.end_time
window_step = args.window_step
sample_length = args.sample_length
dry_run = args.dry_run

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_filename_prefix = os.path.splitext(os.path.basename(input_filename))[0]

print ("Splitting %s where start time is %d and end time is %d." %(
    input_filename,
    start_time,
    end_time
))

# Read and split the file


sample_rate, samples = input_data=wavfile.read(filename=input_filename, mmap=True)
max_amplitude = np.iinfo(samples.dtype).max



start_window_size = int(start_time * sample_rate / 1000)
end_window_size = int(end_time * sample_rate / 1000)
window_length = int(sample_length/1000 * sample_rate)

with open(json_file) as json_f:
    timestamp = json.load(json_f)
timestamp = [x/1000 for x in timestamp]
cut_ranges = [(i,timestamp[i],int(timestamp[i]*sample_rate-start_window_size),int(timestamp[i]*sample_rate+end_window_size) ) for i in range(len(timestamp))]

def detect_energy(clip_start,clip_end,window_step,total_energy):
    max_value = 0
    index = 0
    print("clip start end",clip_start,clip_end,window_step)
    for i in range(clip_start,clip_end,window_step):
        energy_result = energy(samples[i:i + window_length])
        print(energy_result,window_length, i,i/sample_rate)

        if energy_result >= max_value:
            max_value = energy_result
            index = i
    
    print("max value",   max_value, index, index/sample_rate)
   
    return samples[index - int(window_length * 1/8) :index + int(window_length * 7/8)]
    

def energy(samples):
    # return np.sum(np.power(samples,2))
    return np.sum(abs(samples))
    # return np.sum(samples)


for index, i, start, stop in cut_ranges:
    # print(index,i,start/48000,stop/48000)
    print()
    print()
    print("start middel stop", start/sample_rate,i,stop/sample_rate)
    # print("energy sample",energy(samples[start:stop]))
    output_file_path = "{}_{:.3f}.wav".format(
                os.path.join(output_dir, output_filename_prefix),
                i
            )

    if not dry_run:
        audio_clip = detect_energy(start,stop,int(window_step/1000 * sample_rate),energy(samples[start:stop]))

        # if isinstance(audio_clip,float):
            # print(audio_clip)
        wavfile.write(
            filename=output_file_path,
            rate=sample_rate,
            data=audio_clip
        )

    else:
         wavfile.write(
            filename=output_file_path,
            rate=sample_rate,
            data=samples[start:stop]
         )
        