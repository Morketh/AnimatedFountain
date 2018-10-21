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
from lib import static
from imageio.plugins.ffmpeg import get_exe

"""
Kinematic Logo Animation
By: Andrew Malone
"""

## SETTINGS ##

SceneName = "Fountain"
ImgWidth = 1920
ImgHeight = 1080
AnimationTime = 10 # seconds
FPS = 120
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

class Line(object):
    def __init__(self,xa,ya,za,xb,yb,zb):
        """Build a Line!"""
        self.PointA = vector(xa,ya,za)
        self.PointB = vector(xb,yb,zb)

    def Dist(self):
        """Returns distance between Pa and Pb"""
        DeltaX = self.PointA.x - self.PointB.x
        DeltaY = self.PointA.y - self.PointB.y
        DeltaZ = self.PointA.z - self.PointB.z
        return math.sqrt((DeltaX * DeltaX) + (DeltaY * DeltaY) + (DeltaZ * DeltaZ))

    def PointInTime(self,frame,fps,speed=1):
        """Returns (x,y,z) at time for the given line"""
        # distance at time 'frame' ((1/fps)*frame)
        X = self.PointA.x+((speed/fps)*frame)
        Y = self.PointA.y+((speed/fps)*frame)
        Z = self.PointA.z+((speed/fps)*frame)
        return X,Y,Z

def SceneCamNow(i,f_now,fps):
    """Returns camera at time if i == 2 elif i == 1 static cam """
    step=50
    path = Line(-35.0, 25.0, -35.0, 0.0, 35.0, 0.0)
    
    #
    if i == 1: # Static Cam
        return Camera('angle', 45, 'location', [-35.0, 25.0, -35.0], 'look_at', [0 , 1.0 , 0.0])
    elif i == 2: # Animated Cam
        point_now = path.PointInTime(f_now,fps,step)
        if point_now < path.PointB.rtn():
            return Camera('angle', 45, 'location', point_now, 'look_at', [0 , 1.0 , 0.0])
        else:
            return Camera('angle', 45, 'location', path.PointB.rtn(), 'look_at', [0 , 1.0 , 0.0])

# Generic sun object located at x,y,z
sun = LightSource([-900,2500,-3500], 'color', 'White')

CI_Texture = static.GetCITexture()

def GearObj(fnumber, fps, texture=CI_Texture):
    """Defines a Rotating Gear Obj at 'fnumber' with respect to 'fps' """
    rps = 1/4
    GearH = 1
    GearRad = 2
    SpokeW = (GearRad*2)+2
    SpokeAngle = 360/3

    ## Static Objects ##
    Axel = Cylinder([0,-(GearH/2),0], [0,(GearH/2),0], GearRad)
    # Start -x -y -z End x y z
    Spoke = Box([-SpokeW/2,-(GearH/2),0.5],[SpokeW/2,(GearH/2),-0.5])
    Gear = Object(Union(Axel,
                  Object(Spoke,'rotate',[0,SpokeAngle*1,0]),
                  Object(Spoke,'rotate',[0,SpokeAngle*2,0]),
                  Object(Spoke,'rotate',[0,SpokeAngle*3,0])
                  ),texture, 'rotate', [0,((rps*360)/fps)*fnumber,0] )
    return Gear

## Scene Animation ##
def RenderF2F(curFrame, stopFrame, _fps_=24):
    """Render the scene between curFrame and stopFrame at a default of 24 fps"""
    Frames = []
    while curFrame < stopFrame:
        curFrame += 1
        print("Rendering Frame: {} of {}".format(curFrame,stopFrame))
        #gnow = GearObj(curFrame, _fps_)
        gnow = static.Fountain()
        cnow = SceneCamNow(CAM_TYPE, curFrame, _fps_)

        scene = Scene( cnow,
                   objects = [sun,gnow],
                   included = ["colors.inc", "textures.inc"],
                   defaults = [Finish( 'ambient', 0.1, 'diffuse', 0.9)] )

        scene.render(ImageDir+ImageFrmtStr.format(OutputFileName,curFrame), antialiasing=0.001, height=ImgHeight, width=ImgWidth, remove_temp=False) # Keep Pov File for debugging
        Frames.append(ImageClip(ImageDir+ImageFrmtStr.format(OutputFileName,curFrame)).set_duration(1/_fps_))

    concat_clip = concatenate_videoclips(Frames, method="chain") # exception thrown MemoryError()
    concat_clip.write_videofile(Mp4Dir+"{}.mp4".format(OutputFileName), fps=_fps_)


print(get_exe())
#if __name__ == "__main__":
#RenderF2F(StartFrame, MAX_FRAMES,FPS)