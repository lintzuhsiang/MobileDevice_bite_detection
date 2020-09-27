#Data PreProcessing Directory
This is the directory that deals with bite-related audio clips. We transfer the original bite clips into discrete bite samples. Also, filtering methods such as volume detection and Signal-to-Noise (SNR) detection are applied.

##Generate Bite Samples
###Original Data Structure:
- DataProProcessing_Folder
	- Scripts
	- Original Data 
		- UserName
			- 01_01_01
			- 01_02_01

###Bite Audio Naming: 
	Example: 01_02_03_04
		01: username (01-50)
		02: bite environment(01:indoor,02:outdoor,03:running)
		03: bite position(01:front teeth,02:back teeth,03:grind teeth)
		04: bite time(01:one-time,02:two-time,03:three-time)

##Script Usage
###split_audio_timestamp
python3 split_audio_timestamp input_file -s start_time -e end_time -d True/False

Version 1: audio samples length: 400ms
Cut original audio clips into audio samples, by setting -s -e parameter to cut the samples contain all valid bite signals.

Version 2: audio samples length: 50ms
Cut original audio clips into audio samples, by setting -s -e parameter to cut the samples contain all valid bite signal. In the samples, cut 50ms section that have maximum energy sum.



