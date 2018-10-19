#import os
#import numpy as np
#import mido
#from vapory import *
#from moviepy.editor import VideoClip, AudioFileClip
import time
#from lib import fluidsynth
import os
from vapory import *

CWD = os.getcwd()
ImageDir = CWD+"\\img\\"
# Pad the file names with zeros {:02} MUST match the length (Number of Digits) of the MAX_FRAMES number below
ImageName = "{}-{:03}.png"
MAX_FRAMES = 100
# starting frame for animations this MUST satisfy 0 < FRAMENUMBER < MAX_FRAMES
# As long as this is true any animation sequence (or subset) can be rendered
FRAMENUMBER = 1 

# SCENE GLOBALS #
ImgWidth = 1920
ImgHeight = 1080
CAM_TYPE = 2 # see CamType() for a list of camera definitions

#
# Soundfont files downloaded from: https://giantsoundfont.hpage.com/downloads.html
# Giant Soundfont V6.0
#
# Additonal soundfonts can be found at: http://www.synthfont.com/links_to_soundfonts.html
# and here: https://musescore.org/en/handbook/soundfonts-and-sfz-files#install
#
# MIDI_NAME = "./selec/lets_fall_in_love.mid"
# MP3_NAME = MIDI_NAME[:-3]+"mp3"
# VIDEO_NAME = MIDI_NAME[:-3]+"mp4"
#

#SoundFontFile = "soundfonts/6.0bank1.sf2"
"""
Kinematic Logo Animation
By: Andrew Malone
"""



def CamType(i):
    if i == 1:
        return Camera('angle', 45, 'location', [0.0 , 1.0,-2.0], 'look_at', [0 , 1.0 , 0.0])
    elif i == 2:
        return Camera('angle', 45, 'location', [-35.0 , 25.0 ,-30.0], 'look_at', [0 , 1.0 , 0.0])

# Generic sun object located at x,y,z
sun = LightSource([-900,2500,-3500], 'color', 'White')



# Colors and Textures #
CI_ColorMap = ColorMap([0.0,  'rgb', [0.0, 0.0, 0.0]],
                       [0.7,  'rgb', [0.0, 0.3, 0.0]],
                       [0.5,  'rgb', [0.0, 0.7, 0.0]],
                       [0.6,  'rgb', [0.0, 0.2, 0.0]],
                       [0.65, 'rgb', [0.0, 1.0, 1.0]],
                       [0.75, 'rgb', [0.0, 0.2, 0.0]],
                       [0.8,  'rgb', [0.0, 0.5, 0.0]],
                       [1.0,  'rgb', [0.0, 1.0, 0.0]])

CI_Plasma_Marble = Pigment('marble', 'turbulence', 2.75, CI_ColorMap, 'scale', 2.5, 'rotate', [0, 7.5 ,0])
# End of Colors and Textures #

# Define a Wheel Object #
WheelH = 1
WheelRadius = 2
SpokeW = (WheelRadius*2)+2
SpokeAngle = 360/3
Axel = Cylinder([0,-(WheelH/2),0], [0,(WheelH/2),0], WheelRadius)
# Start -x -y -z End x y z
Spoke = Box([-SpokeW/2,-(WheelH/2),0.5],[SpokeW/2,(WheelH/2),-0.5])

while FRAMENUMBER < MAX_FRAMES+1:
    Wheel = Object(Union(Axel,
                   Object(Spoke,'rotate',[0,SpokeAngle*1,0]),
                   Object(Spoke,'rotate',[0,SpokeAngle*2,0]),
                   Object(Spoke,'rotate',[0,SpokeAngle*3,0])
                   ), Texture(CI_Plasma_Marble), 'rotate', [0,(360/MAX_FRAMES)*FRAMENUMBER,0])


# End of Wheel Object #

    scene = Scene( CamType(CAM_TYPE),
               objects = [sun,Wheel],
               included = ["colors.inc", "textures.inc"],
               defaults = [Finish( 'ambient', 0.1, 'diffuse', 0.9)] )

    scene.render(ImageDir+ImageName.format("Test",FRAMENUMBER), antialiasing=0.001, remove_temp=False, height=ImgHeight, width=ImgWidth)
    FRAMENUMBER += 1
