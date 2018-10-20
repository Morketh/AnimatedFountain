from vapory import *

"""
Defines commonly used textures, colors and other static scene items
By: Andrew Malone
Python: 3.6
Pov-Ray: 3.7
Date: 10/19/2018
"""

def GetCITexture():
    """Returns the CI Texture
    Green and Black Marble with touches of sky blue"""
    CI_ColorMap = ColorMap([0.0,  'rgb', [0.0, 0.0, 0.0]],
                           [0.7,  'rgb', [0.0, 0.3, 0.0]],
                           [0.5,  'rgb', [0.0, 0.7, 0.0]],
                           [0.6,  'rgb', [0.0, 0.2, 0.0]],
                           [0.65, 'rgb', [0.0, 1.0, 1.0]],
                           [0.75, 'rgb', [0.0, 0.2, 0.0]],
                           [0.8,  'rgb', [0.0, 0.5, 0.0]],
                           [1.0,  'rgb', [0.0, 1.0, 0.0]])

    return Texture(Pigment('marble', 'turbulence', 2.75, CI_ColorMap, 'scale', 2.5, 'rotate', [0, 7.5 ,0]))
