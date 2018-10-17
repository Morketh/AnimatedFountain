/*
VARIABLE DEFINITIONS

vector Force (net)

vector Velocity (i) (speed of particle Positive Y)
vector Velocity (f) 

vector Acceleration

vector Pos (i)
vector Pos (f)
      
float Mass = .05 // 1 drop of water in grams      

Gravity = -Y * 9.8 // M/s^2  Gravity is on our Y axis and pulling DOWN at 9.8 M/s^2

*/


// PoVRay 3.7 Scene File " ... .pov"
// author:  ...
// date:    ...
//------------------------------------------------------------------------
#version 3.7;
global_settings{ assumed_gamma 1.0 }
#default{ finish{ ambient 0.1 diffuse 0.9 }} 
//------------------------------------------------------------------------
#include "colors.inc"
#include "textures.inc"
#include "glass.inc"
#include "metals.inc"
#include "golds.inc"
#include "stones.inc"
#include "woods.inc"
#include "shapes.inc"
#include "shapes2.inc"
#include "functions.inc"
#include "math.inc"
#include "transforms.inc"
//------------------------------------------------------------------------
#declare Camera_0 = camera {/*ultra_wide_angle*/ angle 15      // front view
                            location  <0.0 , 1.0 ,-40.0>
                            right     x*image_width/image_height
                            look_at   <0.0 , 1.0 , 0.0>}
#declare Camera_1 = camera {/*ultra_wide_angle*/ angle 45   // diagonal view
                            location  <10.0 , 6.0 ,-10.0>
                            right     x*image_width/image_height
                            look_at   <0.0 , 1 , 0.0>}
#declare Camera_2 = camera {/*ultra_wide_angle*/ angle 90  //right side view
                            location  <3.0 , 1.0 , 0.0>
                            right     x*image_width/image_height
                            look_at   <0.0 , 1.0 , 0.0>}
#declare Camera_3 = camera {/*ultra_wide_angle*/ angle 90        // top view
                            location  <0.0 , 10.0 ,-0.001>
                            right     x*image_width/image_height
                            look_at   <0.0 , 1.0 , 0.0>}
camera{Camera_1}
//------------------------------------------------------------------------
// sun -------------------------------------------------------------------
light_source{<-900,2500,-3500> color White}                                   





// sky -------------------------------------------------------------------      
#declare skybox =
sky_sphere{ pigment{ gradient <0,1,0>
                     color_map{ [0   color rgb<1,1,1>         ]//White
                                [0.4 color rgb<0.14,0.14,0.56>]//~Navy
                                [0.6 color rgb<0.14,0.14,0.56>]//~Navy
                                [1.0 color rgb<1,1,1>         ]//White
                              }
                     scale 2 }
           } // end of sky_sphere 
           
           
// ground -----------------------------------------------------------------
//---------------------------------<<< settings of squared plane dimensions
#declare RasterScale = 1.0;
#declare RasterHalfLine  = 0.025;  
#declare RasterHalfLineZ = 0.025; 
//-------------------------------------------------------------------------
#macro Raster(RScale, HLine) 
       pigment{ gradient x scale RScale
                color_map{[0.000   color rgbt<1,1,1,0>*1.0]
                          [0+HLine color rgbt<1,1,1,0>*1.0]
                          [0+HLine color rgbt<1,1,1,1>]
                          [1-HLine color rgbt<1,1,1,1>]
                          [1-HLine color rgbt<1,1,1,0>*1.0]
                          [1.000   color rgbt<1,1,1,0>*1.0]} }
 #end// of Raster(RScale, HLine)-macro    
//-------------------------------------------------------------------------
    
#declare ground =
plane { <0,1,0>, 0    // plane with layered textures
        texture { pigment{color rgb<1,1,1>*0.05} }
        texture { Raster(RasterScale,RasterHalfLine ) rotate<0,0,0> }
        texture { Raster(RasterScale,RasterHalfLineZ) rotate<0,90,0>}
        rotate<0,0,0>
      }
//------------------------------------------------ end of squared plane XZ





//------------------------------ the Axes --------------------------------
#macro Axis_( AxisLen, Dark_Texture,Light_Texture) 
 union{
    cylinder { <0,-AxisLen,0>,<0,AxisLen,0>,0.05
               texture{checker texture{Dark_Texture } 
                               texture{Light_Texture}
                       translate<0.1,0,0.1>}
             }
    cone{<0,AxisLen,0>,0.2,<0,AxisLen+0.7,0>,0
          texture{Dark_Texture}
         }
     } // end of union                   
#end // of macro "Axis()"
//------------------------------------------------------------------------
#macro AxisXYZ( AxisLenX, AxisLenY, AxisLenZ, Tex_Dark, Tex_Light)
//--------------------- drawing of 3 Axes --------------------------------
union{
#if (AxisLenX != 0)
 object { Axis_(AxisLenX, Tex_Dark, Tex_Light)   rotate< 0,0,-90>}// x-Axis
 text   { ttf "arial.ttf",  "x",  0.15,  0  texture{Tex_Dark} 
          rotate<20,-45,0> scale 0.75 translate <AxisLenX+0.05,0.4,-0.10> no_shadow}
#end // of #if 
#if (AxisLenY != 0)
 object { Axis_(AxisLenY, Tex_Dark, Tex_Light)   rotate< 0,0,  0>}// y-Axis
 text   { ttf "arial.ttf",  "y",  0.15,  0  texture{Tex_Dark}    
          rotate<10,0,0> scale 0.75 translate <-0.65,AxisLenY+0.50,-0.10>  rotate<0,-45,0> no_shadow}
#end // of #if 
#if (AxisLenZ != 0)
 object { Axis_(AxisLenZ, Tex_Dark, Tex_Light)   rotate<90,0,  0>}// z-Axis
 text   { ttf "arial.ttf",  "z",  0.15,  0  texture{Tex_Dark}
          rotate<20,-45,0> scale 0.85 translate <-0.75,0.2,AxisLenZ+0.10> no_shadow}
#end // of #if 
} // end of union
#end// of macro "AxisXYZ( ... )"
//------------------------------------------------------------------------

#declare Texture_A_Dark  = texture {
                               pigment{ color rgb<1,0.45,0>}
                               finish { phong 1}
                             }
#declare Texture_A_Light = texture { 
                               pigment{ color rgb<1,1,1>}
                               finish { phong 1}
                             }

//object{ AxisXYZ( 3.5, 2.8, 4, Texture_A_Dark, Texture_A_Light)}

//-------------------------------------------------- end of coordinate axes

/*                                                                          
#declare Jade_Map =
color_map {
    [0.0 rgb <0.1, 0.0, 0.1>]
    [0.8 rgb <0.0, 0.3, 0.0>]
    [0.8 rgb <0.1, 0.0, 0.1>]
    [1.0 rgb <0.0, 0.2, 0.0>]
}
*/
// Drew Wells' superb Jade.  Color map works nicely with other textures, too.
#declare Jade = 
pigment {
    marble
    turbulence 1.8
    color_map { Jade_Map }
}
                                                                          
                                                                          
                                                                          
//--------------------------------------------------------------------------
//---------------------------- objects in scene ----------------------------
//--------------------------------------------------------------------------


/* lets define a fountain structure first */    


// Global Varables
#declare FountTexture = Jade; // Fountain Texture

// Fountain Base variables
#declare FountThickness = .25; // Fountain Thickness
#declare FountH = 1;          // Fountain Base Higth
#declare FountR = 2.5;          // Fountain Base Radius

// Fountain Center Variables
#declare FountainCH = 1.5;
#declare FountainCR = .5;


// Object definitions

#declare FountainBase =
difference {
    cylinder { <0,0,0>, <0,FountH,0>, FountR }
    // subtract the center
    cylinder { <0,FountThickness,0>, <0,(FountH + FountThickness),0>, (FountR - FountThickness) }
}

#declare Fountain =
union {
    object { FountainBase }
    cylinder { <0,FountThickness,0>, <0,FountainCH,0>, FountainCR }
    //texture { FountTexture }
}


object { 
    Fountain
    translate <-2.5,0,0>
    texture { Jade }        
}
    
object { 
    Fountain
    translate <2.5,0,0>
    texture { Blood_Marble }
    }