import numpy as np

from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

# WE CREATE THE TEXT THAT IS GOING TO MOVE, WE CENTER IT.

screensize = (720,460)
imgClip1 = ImageClip("img/IMG_1569.JPG")
imgClip2 = ImageClip("img/IMG_1570.JPG")
imgClip3 = ImageClip("img/IMG_1571.JPG")
imgClip4 = ImageClip("img/IMG_1572.JPG")
imgClip5 = ImageClip("img/IMG_1573.JPG")
imgClip6 = ImageClip("img/IMG_1574.JPG")
imgClip7 = ImageClip("img/IMG_1575.JPG")
imgClip8 = ImageClip("img/IMG_1576.JPG")
imgClip9 = ImageClip("img/IMG_1577.JPG")


cvc = CompositeVideoClip( [imgClip1, imgClip2,imgClip3], size=screensize)

# THE NEXT FOUR FUNCTIONS DEFINE FOUR WAYS OF MOVING THE LETTERS


# helper function
rotMatrix = lambda a: np.array( [[np.cos(a),np.sin(a)], 
                                 [-np.sin(a),np.cos(a)]] )

def vortex(screenpos,i,nletters):
    d = lambda t : 1.0/(0.3+t**8) #damping
    a = i*np.pi/ nletters # angle of the movement
    v = rotMatrix(a).dot([-1,0])
    if i%2 : v[1] = -v[1]
    return lambda t: screenpos+400*d(t)*rotMatrix(0.5*d(t)*a).dot(v)
    
def cascade(screenpos,i,nletters):
    v = np.array([0,-1])
    d = lambda t : 1 if t<0 else abs(np.sinc(t)/(1+t**4))
    return lambda t: screenpos+v*400*d(t-0.15*i)

def arrive(screenpos,i,nletters):
    v = np.array([-1,0])
    d = lambda t : max(0, 3-3*t)
    return lambda t: screenpos-400*v*d(t-0.2*i)
    
def vortexout(screenpos,i,nletters):
    d = lambda t : max(0,t) #damping
    a = i*np.pi/ nletters # angle of the movement
    v = rotMatrix(a).dot([-1,0])
    if i%2 : v[1] = -v[1]
    return lambda t: screenpos+400*d(t-0.1*i)*rotMatrix(-0.2*d(t)*a).dot(v)



# WE USE THE PLUGIN findObjects TO LOCATE AND SEPARATE EACH LETTER

#letters = findObjects(cvc) # a list of ImageClips
letters = [imgClip1, imgClip2,imgClip3,imgClip4, imgClip5,imgClip6,imgClip7, imgClip8,imgClip9]

# WE ANIMATE THE LETTERS

def moveLetters(letter,i, funcpos):
    return [ letter.set_pos(funcpos([1,1],i,9))]

clips = [ CompositeVideoClip( moveLetters(letter,i,vortex),
                              size = screensize).subclip(0,4)
          for i,letter in enumerate(letters)]

clips.extend([ CompositeVideoClip( moveLetters(letter,i,arrive),
                              size = screensize).subclip(0,4)
          for i,letter in enumerate(letters)])
# WE CONCATENATE EVERYTHING AND WRITE TO A FILE

final_clip = concatenate_videoclips(clips)
final_clip.write_videofile('coolImageEffects.avi',fps=25,codec='mpeg4')