import os
import numpy as np
import mido
from vapory import *
from moviepy.editor import VideoClip, AudioFileClip
import time
from libs import fluidsynth

#MIDI_NAME = "./selec/lets_fall_in_love.mid"
#MP3_NAME = MIDI_NAME[:-3]+"mp3"
#VIDEO_NAME = MIDI_NAME[:-3]+"mp4"


fs = fluidsynth.Synth()
fs.start()

sfid = fs.sfload("example.sf2")
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
fs.noteon(0, 67, 30)
fs.noteon(0, 76, 30)

time.sleep(1.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(1.0)

fs.delete()