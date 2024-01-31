# Python script extract-oki-msm6376.py
This Python script is able to extract sound samples from any rom file that is used in conjunction with the Oki MSM6376 speech synthesizer chip.
The MSM6376 is capable of playing audio samples that are stored in a 4 bit ADPCM audio format that is also known as the IMA/OKI ADPCM audio format. 
This specific audio chip is used quite a bit in gambling machines from the Maygay brand. It is also used in pinball machines from the Sleic brand. 
This chip is rather common in devices from the mid nineties. 
# Prerequisites
If you want this script to successfully convert the extracted OKI ADPCM audio files to wave files you need to install ffmpeg 
(https://ffmpeg.org/download.html). FFmpeg also needs to be added to the PATH environment variable. If these conditions 
are not met, the script will not be able to convert the extracted PCM files to the more common wave file format.
# Extract audio samples
The OKI ADPCM audio format does not contain any information about the audio sampling rate, so when converting it to a .wav file (or any other format) 
you need to supply the correct sampling rate in khz. If you don't know this information, you can get this value by trial and error. 
It is also good to know that it is not uncommon that there are multiple soundrom files for a single device. 
You typically need to combine the files into a single rom files to be able to extract all the available audio samples. 
This is for example the case when extracting the audio samples from the Sleic IO Moon and the Sleic Bike Race pinball machines.

Extract all sample files from soundrom.bin, assume that they have an audio sampling rate of 32khz.
This will create an output directory with 2 sub directories. One will be named pcm and it will contain the raw extracted OKI ADPCM audio stream. 
These files can be used with specialized audio editors. It also contains a wav folder, this will contain the same audio samples, but already converted
to the common wave file format that can be played in almost every common audio player.

`python extract-oki-msm6376.py --file "C:\roms\soundrom.bin" --khz 32`



