import cv2
import numpy as np
import stitch
import utils
import timeit



start = timeit.default_timer()

list_images=utils.loadImages('data/BK',reize=True)
panorama=stitch.multiStitching(list_images,400)
cv2.imwrite('result/panorama.jpg',panorama)

stop = timeit.default_timer()
print('Execution time: ', stop - start) 






