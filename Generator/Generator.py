#import os
#import numpy as np
#import mido
#from vapory import *
#from moviepy.editor import VideoClip, AudioFileClip
import time
#from lib import fluidsynth
import os
from vapory import *
from moviepy.editor import *

## SETTINGS ##

SceneName = "GreenGear"
ImgWidth = 1920
ImgHeight = 1080
CAM_TYPE = 2 # see CamType() for a list of camera definitions

# starting frame for animations this MUST satisfy 0 < FRAMENUMBER < MAX_FRAMES
# As long as this is true any animation sequence (or subset) can be rendered
FRAMENUMBER = 0
MAX_FRAMES = 500
FPS = 120

# SCENE GLOBALS #
CWD = os.getcwd()

## Internal Variables ##
OutputFileName = "{}_{}-frames_{}-FPS".format(SceneName,MAX_FRAMES,FPS)
ImageFrmtStr = "{}-{:03}.png"
ImageDir = CWD+"\\img\\"
Mp4Dir = CWD+"\\mp4\\"

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

## Static Objects ##
Axel = Cylinder([0,-(WheelH/2),0], [0,(WheelH/2),0], WheelRadius)
# Start -x -y -z End x y z
Spoke = Box([-SpokeW/2,-(WheelH/2),0.5],[SpokeW/2,(WheelH/2),-0.5])

Frames = []
## Scene Animation ##
while FRAMENUMBER < MAX_FRAMES:
    FRAMENUMBER += 1
    print("Rendering Frame: {} of {}".format(FRAMENUMBER,MAX_FRAMES))
    Wheel = Object(Union(Axel,
                   Object(Spoke,'rotate',[0,SpokeAngle*1,0]),
                   Object(Spoke,'rotate',[0,SpokeAngle*2,0]),
                   Object(Spoke,'rotate',[0,SpokeAngle*3,0])
                   ), Texture(CI_Plasma_Marble), 'rotate', [0,((360*2)/MAX_FRAMES)*FRAMENUMBER,0])


# End of Wheel Object #

    scene = Scene( CamType(CAM_TYPE),
               objects = [sun,Wheel],
               included = ["colors.inc", "textures.inc"],
               defaults = [Finish( 'ambient', 0.1, 'diffuse', 0.9)] )

    scene.render(ImageDir+ImageFrmtStr.format(OutputFileName,FRAMENUMBER), antialiasing=0.001, height=ImgHeight, width=ImgWidth)
    Frames.append(ImageClip(ImageDir+ImageFrmtStr.format(OutputFileName,FRAMENUMBER)).set_duration(1/FPS))
    

concat_clip = concatenate_videoclips(Frames, method="compose")
concat_clip.write_videofile(Mp4Dir+"{}.mp4".format(OutputFileName), fps=FPS)

