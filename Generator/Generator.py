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
from lib import static, motionObjs
#from imageio.plugins.ffmpeg import get_exe

"""
Kinematic Logo Animation
By: Andrew Malone
"""

## SETTINGS ##

SceneName = "Fountain"
ImgWidth = 1920
ImgHeight = 1080
AnimationTime = 20 # seconds
FPS = 80
CAM_TYPE = 1 # see CamType() for a list of camera definitions

# starting frame for animations this MUST satisfy 0 < FRAMENUMBER < MAX_FRAMES
# As long as this is true any animation sequence (or subset) can be rendered
StartFrame = 0

# SCENE GLOBALS #
CWD = os.getcwd()

## Internal Variables ##
MAX_FRAMES = AnimationTime*FPS
OutputFileName = "{}_{}-frames_{}-FPS".format(SceneName,MAX_FRAMES,FPS)
ImageFrmtStr = "{}-{:04}.png"
ImageDir = CWD+"\\img\\"
Mp4Dir = CWD+"\\mp4\\"

class vector(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def rtn(self):
        return self.x, self.y, self.z

class LineMotion(object):
    def __init__(self,xa,ya,za,xb,yb,zb):
        """Build a Line! Defines total displacement between 2 points
        in order to get any point along the path in respect to time
       PointInTime() may be called."""
        self.PointA = vector(xa,ya,za)
        self.PointB = vector(xb,yb,zb)
        Distance = self._Dist_()

    def _Dist_(self):
        """Returns distance between Pa and Pb"""
        self.DeltaX = self.PointA.x - self.PointB.x
        self.DeltaY = self.PointA.y - self.PointB.y
        self.DeltaZ = self.PointA.z - self.PointB.z
        return math.sqrt((self.DeltaX * self.DeltaX) + (self.DeltaY * self.DeltaY) + (self.DeltaZ * self.DeltaZ))

    def PointInTime(self,frame,fps,speed=1):
        """Returns (x,y,z) at time for the given line"""
        # distance at time 'frame' ((1/fps)*frame)
        X = (frame*speed+self.DeltaX*fps)/fps
        Y = (frame*speed+self.DeltaY*fps)/fps
        Z = (frame*speed+self.DeltaZ*fps)/fps
        return X,Y,Z

def SceneCamNow(i,f_now,fps):
    """Returns camera at time if i == 2 elif i == 1 static cam """
    step=50
    path = LineMotion(-35.0, 25.0, -35.0, 0.0, 60.0, 0.0)
    #
    if i == 1: # Static Cam
        return Camera('angle', 45, 'location', [0, 35.0, 0.0], 'look_at', [0 , 0.0 , 0.0])
    elif i == 2: # Animated Cam
        point_now = path.PointInTime(f_now,fps,step)
        if point_now < path.PointB.rtn():
            return Camera('angle', 45, 'location', point_now, 'look_at', [0 , 1.0 , 0.0])
        else:
            return Camera('angle', 45, 'location', [path.PointB.x, path.PointB.y, path.PointB.z], 'look_at', [0 , 1.0 , 0.0])

# Generic sun object located at x,y,z
sun = LightSource([-900,2500,-3500], 'color', 'White')

CI_Texture = static.GetCITexture()

## Scene Animation ##
def RenderF2F(curFrame, stopFrame, _fps_=24):
    """Render the scene between curFrame and stopFrame at a default of 24 fps"""
    Frames = []
    while curFrame < stopFrame:
        curFrame += 1
        print("Rendering Frame: {} of {}".format(curFrame,stopFrame))
        gear = motionObjs.GearObj(curFrame, _fps_,offset=vector(0,0,4))
        # insert Textured Loading bar to scale from left to right of screen over total frames
        #gnow = static.Fountain()
        cnow = SceneCamNow(CAM_TYPE, curFrame, _fps_)

        scene = Scene( cnow,
                   objects = [sun,gear],
                   included = ["colors.inc", "textures.inc"],
                   defaults = [Finish( 'ambient', 0.1, 'diffuse', 0.9)] )

        scene.render(ImageDir+ImageFrmtStr.format(OutputFileName,curFrame), antialiasing=0.001, height=ImgHeight, width=ImgWidth, remove_temp=False) # Keep Pov File for debugging
        Frames.append(ImageClip(ImageDir+ImageFrmtStr.format(OutputFileName,curFrame)).set_duration(1/_fps_))

    concat_clip = concatenate_videoclips(Frames, method="chain") # exception thrown MemoryError()
    concat_clip.write_videofile(Mp4Dir+"{}.mp4".format(OutputFileName), fps=_fps_)


#print(get_exe())
#if __name__ == "__main__":
RenderF2F(StartFrame, MAX_FRAMES,FPS)