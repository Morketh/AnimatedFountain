#include "colors.inc"
#include "textures.inc"
light_source {
<-900,2500,-3500>
color
White 
}
object {
union {
cylinder {
<0,-0.5,0>
<0,0.5,0>
2 
}
object {
box {
<-3.0,-0.5,0.5>
<3.0,0.5,-0.5> 
}
rotate
<0,120.0,0> 
}
object {
box {
<-3.0,-0.5,0.5>
<3.0,0.5,-0.5> 
}
rotate
<0,240.0,0> 
}
object {
box {
<-3.0,-0.5,0.5>
<3.0,0.5,-0.5> 
}
rotate
<0,360.0,0> 
} 
}
texture {
pigment {
marble
turbulence
2.75
color_map { [ 0.0 rgb <0.0,0.0,0.0> ]
[ 0.7 rgb <0.0,0.3,0.0> ]
[ 0.5 rgb <0.0,0.7,0.0> ]
[ 0.6 rgb <0.0,0.2,0.0> ]
[ 0.65 rgb <0.0,1.0,1.0> ]
[ 0.75 rgb <0.0,0.2,0.0> ]
[ 0.8 rgb <0.0,0.5,0.0> ]
[ 1.0 rgb <0.0,1.0,0.0> ] }
scale
2.5
rotate
<0,7.5,0> 
} 
}
rotate
<0,8640.0,0> 
}
camera {
angle
45
location
<-35.0,25.0,-30.0>
look_at
<0,1.0,0.0>
right
<1.7777777777777777,0,0> 
}
global_settings{

}