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

#import os
#import numpy as np
#import mido
#from vapory import *
#from moviepy.editor import VideoClip, AudioFileClip
import time
#from lib import fluidsynth
import os, math
from vapory import *
from moviepy.editor import *

"""
Kinematic Logo Animation
By: Andrew Malone
"""

## SETTINGS ##

SceneName = "GreenGear"
ImgWidth = 1920
ImgHeight = 1080
AnimationTime = 10 # seconds
FPS = 116
CAM_TYPE = 2 # see CamType() for a list of camera definitions

# starting frame for animations this MUST satisfy 0 < FRAMENUMBER < MAX_FRAMES
# As long as this is true any animation sequence (or subset) can be rendered
FRAMENUMBER = 0

# SCENE GLOBALS #
CWD = os.getcwd()

## Internal Variables ##
MAX_FRAMES = AnimationTime*FPS
OutputFileName = "{}_{}-frames_{}-FPS".format(SceneName,MAX_FRAMES,FPS)
ImageFrmtStr = "{}-{:04}.png"
ImageDir = CWD+"\\img\\"
Mp4Dir = CWD+"\\mp4\\"

# speed 120 FPS
# 't' is pos at time
def SceneCamNow(i,f_now,fps):
    """Returns camera at time if i == 2 elif i == 1 static cam """
    step=1
    iy = 25
    fy = iy+6.5
    ix = -30
    fx = 0
    iz = -30
    fz = 0
    
    y = iy + (fy-iy)*0.5*fps
    x = ix + (fx-ix)*0.5*fps
    z = iz + (fz-iz)*0.5*fps
    
    #
    if i == 1: # Static Cam
        return Camera('angle', 45, 'location', [0.0 , 1.0,-2.0], 'look_at', [0 , 1.0 , 0.0])
    elif i == 2: # Animated Cam
        return Camera('angle', 45, 'location', [-35.0 , 25.0 ,-30.0], 'look_at', [0 , 1.0 , 0.0])

# Generic sun object located at x,y,z
sun = LightSource([-900,2500,-3500], 'color', 'White')

CI_Texture = GetCITexture()

# End of Colors and Textures #

def GearObj(fnumber, fps, texture=CI_Texture):
    """Defines a Rotating Gear Obj at 'fnumber' with respect to 'fps' """
    rps = 0.75
    WheelH = 1
    WheelRadius = 2
    SpokeW = (WheelRadius*2)+2
    SpokeAngle = 360/3

    ## Static Objects ##
    Axel = Cylinder([0,-(WheelH/2),0], [0,(WheelH/2),0], WheelRadius)
    # Start -x -y -z End x y z
    Spoke = Box([-SpokeW/2,-(WheelH/2),0.5],[SpokeW/2,(WheelH/2),-0.5])
    Wheel = Object(Union(Axel,
                   Object(Spoke,'rotate',[0,SpokeAngle*1,0]),
                   Object(Spoke,'rotate',[0,SpokeAngle*2,0]),
                   Object(Spoke,'rotate',[0,SpokeAngle*3,0])
                   ),texture, 'rotate', [0,((rps*360)/fps)*fnumber,0] )
    return Wheel



## Scene Animation ##
Frames = []
while FRAMENUMBER < MAX_FRAMES:
    FRAMENUMBER += 1
    print("Rendering Frame: {} of {}".format(FRAMENUMBER,MAX_FRAMES))
    gnow = GearObj(FRAMENUMBER, FPS)
    cnow = SceneCamNow(CAM_TYPE, FRAMENUMBER, FPS)

# End of Wheel Object #

    scene = Scene( cnow,
               objects = [sun,gnow],
               included = ["colors.inc", "textures.inc"],
               defaults = [Finish( 'ambient', 0.1, 'diffuse', 0.9)] )

    scene.render(ImageDir+ImageFrmtStr.format(OutputFileName,FRAMENUMBER), antialiasing=0.001, height=ImgHeight, width=ImgWidth, remove_temp=False) # Keep Pov File for debugging
    Frames.append(ImageClip(ImageDir+ImageFrmtStr.format(OutputFileName,FRAMENUMBER)).set_duration(1/FPS))
    

concat_clip = concatenate_videoclips(Frames, method="chain") # exception thrown MemoryError()
concat_clip.write_videofile(Mp4Dir+"{}.mp4".format(OutputFileName), fps=FPS)