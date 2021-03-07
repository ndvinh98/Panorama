import cv2
import numpy as np


def findAndDescribeFeatures(image, opt="ORB"):
    """find and describe features of @image,
        if opt='SURF', SURF algorithm is used.
        if opt='SIFT', SIFT algorithm is used.
        if opt='ORB', ORB algorithm is used.
        @Return keypoints and features of img"""
    # Getting gray image
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if opt == "SURF":
        md = cv2.xfeatures2d.SURF_create()
    if opt == "ORB":
        md = cv2.ORB_create(nfeatures=3000)
    if opt == "SIFT":
        md = cv2.xfeatures2d.SIFT_create()
    # Find interest points and Computing features.
    keypoints, features = md.detectAndCompute(grayImage, None)
    # Converting keypoints to numbers.
    # keypoints = np.float32(keypoints)
    features = np.float32(features)
    return keypoints, features


def matchFeatures(featuresA, featuresB, ratio=0.75, opt="FB"):
    """matching features beetween 2 @features.
         If opt='FB', FlannBased algorithm is used.
         If opt='BF', BruteForce algorithm is used.
         @ratio is the Lowe's ratio test.
         @return matches"""
    if opt == "BF":
        featureMatcher = cv2.DescriptorMatcher_create("BruteForce")
    if opt == "FB":
        # featureMatcher = cv2.DescriptorMatcher_create("FlannBased")
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        featureMatcher = cv2.FlannBasedMatcher(index_params, search_params)

    # performs k-NN matching between the two feature vector sets using k=2
    # (indicating the top two matches for each feature vector are returned).
    matches = featureMatcher.knnMatch(featuresA, featuresB, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good.append(m)
    if len(good) > 4:
        return good
    raise Exception("Not enought matches")


def generateHomography(src_img, dst_img, ransacRep=5.0):
    """@Return Homography matrix, @param src_img is the image which is warped by homography,
        @param dst_img is the image which is choosing as pivot, @param ratio is the David Lowe’s ratio,
        @param ransacRep is the maximum pixel “wiggle room” allowed by the RANSAC algorithm
        """

    src_kp, src_features = findAndDescribeFeatures(src_img)
    dst_kp, dst_features = findAndDescribeFeatures(dst_img)

    good = matchFeatures(src_features, dst_features)

    src_points = np.float32([src_kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_points = np.float32([dst_kp[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(src_points, dst_points, cv2.RANSAC, ransacRep)
    matchesMask = mask.ravel().tolist()
    return H, matchesMask


def drawKeypoints(img, kp):
    img1 = img
    cv2.drawKeypoints(img, kp, img1, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return img1


def drawMatches(src_img, src_kp, dst_img, dst_kp, matches, matchesMask):
    draw_params = dict(
        matchColor=(0, 255, 0),  # draw matches in green color
        singlePointColor=None,
        matchesMask=matchesMask[:100],  # draw only inliers
        flags=2,
    )
    return cv2.drawMatches(
        src_img, src_kp, dst_img, dst_kp, matches[:100], None, **draw_params
    )
