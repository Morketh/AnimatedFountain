from vapory import *

def RotateMotion(frame, fps, rps):
    """Return Rotation
    value: ((rps*360*frame)/fps)"""
    return ((rps*360*frame)/fps)

def GearObj(fnumber, fps, texture=CI_Texture):
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
                  ),texture, 'rotate', [0,RotateMotion(fnumber, fps, rps),0] )
    return Gear
