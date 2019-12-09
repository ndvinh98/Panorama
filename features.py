import cv2
import numpy as np

def findAndDescribeFeatures(image):
	'''find and describe features of image, @Return keypoints and features of img'''
	#Getting gray image
	grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#Find and describe the features.
	sift = cv2.xfeatures2d.SURF_create()
	#Low sift = cv2.xfeatures2d.SIFT_create()

	#Find interest points.
	keypoints = sift.detect(grayImage, None)

	#Computing features.
	keypoints, features = sift.compute(grayImage, keypoints)

	#Converting keypoints to numbers.
	keypoints = np.float32([kp.pt for kp in keypoints])

	return keypoints, features

def matchFeatures(featuresA, featuresB):
	'''matching features beetween 2 features, @return matches'''
	# Slow: featureMatcher = cv2.DescriptorMatcher_create("BruteForce")
	featureMatcher = cv2.DescriptorMatcher_create("FlannBased")

	#performs k-NN matching between the two feature vector sets using k=2 
	#(indicating the top two matches for each feature vector are returned).
	matches = featureMatcher.knnMatch(featuresA,featuresB, k=2)
	return matches

def generateHomography(src_img, dst_img, ratio=0.75, ransacRep=5.0):
	'''@Return Homography matrix, @param src_img is the image which is transforming by homography,
	@param dst_img is the image which is choosing as pivot, @param ratio is the David Lowe’s ratio,
	@param ransacRep is the maximum pixel “wiggle room” allowed by the RANSAC algorithm
	'''

	src_kp,src_features=findAndDescribeFeatures(src_img)
	dst_kp,dst_features=findAndDescribeFeatures(dst_img)
	matches=matchFeatures(src_features,dst_features)
	good = []
	for m,n in matches:
		# Lowe's ratio test
		if m.distance<ratio*n.distance:
			good.append(m)

	src_points = np.float32([src_kp[m.queryIdx] for m in good])
	dst_points = np.float32([dst_kp[m.trainIdx] for m in good])

	if len(good)>4:
		H, status = cv2.findHomography(src_points, dst_points, cv2.RANSAC,ransacRep)
		return H
	else:
		return None