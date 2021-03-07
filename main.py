import cv2
import stitch
import utils
import timeit
import argparse


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="path to input directory")
ap.add_argument("-o", "--output", required=True, help="path to output directory")
ap.add_argument("-r", "--resize", type=int, default=0, help="resize input images")
args = vars(ap.parse_args())

# caculate execution time
print("Processing....")
start = timeit.default_timer()

# load images
list_images = utils.loadImages(args["input"], args["resize"])

# create panorama, default using ORB with nfeatures=3000, u can change to SIFT, SURF in features.py or add some argument
panorama = stitch.multiStitching(list_images)

# save
cv2.imwrite(args["output"] + "\\panorama.jpg", panorama)

stop = timeit.default_timer()
print("Complete!")
print("Execution time: ", stop - start)
