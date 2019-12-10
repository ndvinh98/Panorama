import cv2
import numpy as np
import stitch
import utils
import timeit
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input directory")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
ap.add_argument("-r", "--resize",default=0,
	help="path to output directory")
args = vars(ap.parse_args())

#caculate execution time
print('Processing....') 
start = timeit.default_timer()


list_images=utils.loadImages(args['input'],args['resize'])
panorama=stitch.multiStitching(list_images,400)
cv2.imwrite(args['output']+'\\panorama.jpg',panorama)

stop = timeit.default_timer()
print('Complete!') 
print('Execution time: ', stop - start) 





#D:\ML\NMTGMT\Panorama\data\myhouse
#D:\ML\NMTGMT\Panorama

