import cv2
import numpy as np
import os
 
from os.path import isfile, join
 
def convert_frames_to_video(pathIn,pathOut,fps):
    '''
    pathIn is the directiry cotaining frames
    pathOut is the output file desired
    fps is the framerate

    '''
    
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
 
    # for sorting the file names properly
    # split name into two, take second part & again split into two and take first
    # example : f-102.jpg to [f, 120.jpg], then take 102.jpg to split [102, jpg] 
    #           and use 102 part to sort
    files.sort(key = lambda f: int(f.split("-")[1].split(".")[0]))
    #print(files)

 
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        print(filename,layers)
        #inserting the frames into an image array
        frame_array.append(img)
 
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
 
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()