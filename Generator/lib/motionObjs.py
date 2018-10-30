from vapory import *
from static import GetCITexture
SECOND = 1

class vector(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def rtn(self):
        return self.x, self.y, self.z

def RotateMotion(frame, fps, rps):
    """Return Rotation
    value: ((rps*360*frame)/fps)"""
    return ((rps*360*frame)/fps)

def GearObj(fnumber, fps, texture=GetCITexture(), offset=vector(0,0,0), scale=vector(0,0,0)):
    """Defines a Rotating Gear Obj at 'fnumber' with respect to 'fps' """
    rps = .25/SECOND
    GearH = 1
    GearRad = 2
    SpokeW = GearRad*3
    SpokeAngle = 360/3

    ## Static Objects ##
    Axel = Cylinder([0,-(GearH/2),0], [0,(GearH/2),0], GearRad)
    # Start -x -y -z End x y z
    Spoke = Box([-SpokeW/2,-(GearH/2),0.5],[SpokeW/2,(GearH/2),-0.5])
    Gear = Object(Union(Axel,
                  Object(Spoke,'rotate',[0,SpokeAngle*1,0]),
                  Object(Spoke,'rotate',[0,SpokeAngle*2,0]),
                  Object(Spoke,'rotate',[0,SpokeAngle*3,0])
                  ),texture, 'rotate', [0,RotateMotion(fnumber, fps, rps),0], 'translate',[offset.x,offset.y,offset.z], 'scale', [scale.x,scale.y,scale.z] )
    return Gear
