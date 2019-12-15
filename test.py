import cv2
import numpy as np
import stitch
import utils

#load images
list_images=utils.loadImages('data/myhouse',resize=0)

#wrap 2 image
#if choose list_images[0] as pivot
pano,non_blend,left_side,right_side=stitch.warpTwoImages(list_images[0],list_images[1],400,True)
img = np.array(non_blend,dtype=float)/float(255)
cv2.imshow('rs.jpg',img)
cv2.waitKey(0)