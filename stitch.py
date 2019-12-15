import cv2
import numpy as np
import features
import utils

def blendingMask(height, width, barrier, smoothing_window, left_biased=True):

    mask = np.zeros((height, width))
    
    offset = int(smoothing_window/2)
    try:
        if left_biased:
            mask[:,barrier-offset:barrier+offset+1]=np.tile(np.linspace(1,0,2*offset+1).T, (height, 1))
            mask[:,:barrier-offset] = 1
        else:
            mask[:,barrier-offset:barrier+offset+1]=np.tile(np.linspace(0,1,2*offset+1).T, (height, 1))
            mask[:,barrier+offset:] = 1
    except:
        if left_biased:
            mask[:,barrier-offset:barrier+offset+1]=np.tile(np.linspace(1,0,2*offset).T, (height, 1))
            mask[:,:barrier-offset] = 1
        else:
            mask[:,barrier-offset:barrier+offset+1]=np.tile(np.linspace(0,1,2*offset).T, (height, 1))
            mask[:,barrier+offset:] = 1
    
    return cv2.merge([mask, mask, mask])
    
def panoramaBlending(dst_img,src_img,width_original_dst,side,smoothing_window = 400,showstep=False):
    h,w,_=dst_img.shape
    barrier = width_original_dst -int(smoothing_window/2)
    mask1 = blendingMask(h, w, barrier, smoothing_window = smoothing_window, left_biased = True)
    mask2 = blendingMask(h, w, barrier, smoothing_window = smoothing_window, left_biased = False)

    if showstep:
        nonblend=src_img+dst_img
    else:
        nonblend=None
        leftside=None
        rightside=None

    if side=='left':
        dst_img=cv2.flip(dst_img,1)
        src_img=cv2.flip(src_img,1)
        dst_img=(dst_img*mask1)
        src_img=(src_img*mask2)
        pano=src_img+dst_img
        pano=cv2.flip(pano,1)
        if showstep:
            leftside=cv2.flip(src_img,1)
            rightside=cv2.flip(dst_img,1)
    else:
        dst_img=(dst_img*mask1)
        src_img=(src_img*mask2)
        pano=src_img+dst_img
        if showstep:
            leftside=dst_img
            rightside=src_img

    
    return pano,nonblend,leftside,rightside

def warpTwoImages(src_img, dst_img,smoothing_window = 400,showstep=False):

	#generate Homography matrix
    H=features.generateHomography(src_img,dst_img)

	#get height and weigh of two images
    h1,w1 = src_img.shape[:2]
    h2,w2 = dst_img.shape[:2]

	#extract conners of two images
    pts1 = np.float32([[0,0],[0,h1],[w1,h1],[w1,0]]).reshape(-1,1,2)
    pts2 = np.float32([[0,0],[0,h2],[w2,h2],[w2,0]]).reshape(-1,1,2)

	#aply homography to conners of src_img
    pts1_ = cv2.perspectiveTransform(pts1, H)
    pts = np.concatenate((pts1_, pts2), axis=0)

    #find max min of x,y coordinate
    [xmin, ymin] = np.int64(pts.min(axis=0).ravel() - 0.5)
    [xmax, ymax] = np.int64(pts.max(axis=0).ravel() + 0.5)
    t = [-xmin,-ymin]

 
    #top left point of image which apply homography matrix, which has x coordinate < 0, has side=left
    #otherwise side=right
    #transformed image is merged to the left side or right side of pivot image
    if(pts[0][0][0]<0):
        side='left'
        width_pano=w2+t[0]
    else:
        width_pano=int(pts1_[3][0][0])
        side='right'
    height_pano=ymax-ymin

    #generating height and width of panorama
    # translate
    Ht = np.array([[1,0,t[0]],[0,1,t[1]],[0,0,1]]) 
    src_img_wrapped = cv2.warpPerspective(src_img, Ht.dot(H), (width_pano,height_pano))

    #generating size of src_img_wrapped which has the same size of dst_img
    dst_img_rz=np.zeros((height_pano,width_pano,3))
    if side=='left':
        dst_img_rz[t[1]:h1+t[1]-abs(h2-h1),t[0]:w2+t[0]] = dst_img
    else:
        dst_img_rz[t[1]:h1+t[1]-abs(h2-h1),:w2] = dst_img

    #blending panorama
    pano2,nonblend,leftside,rightside=panoramaBlending(dst_img_rz,src_img_wrapped,w2,side,smoothing_window=smoothing_window,showstep=showstep)

    #crop black region
    pano2=crop(pano2,h2,pts)
    return pano2,nonblend,leftside,rightside

def multiStitching(list_images,smoothing_window):
    '''assume that the list_images was supplied in left-to-right order, choose middle image then 
    divide the array into 2 sub-arrays, left-array and right-array. Stiching middle image with each
    image in 2 sub-arrays. @param list_images is The list which containing images, @param smoothing_window is 
    the value of smoothy side after stitched, @param output is the folder which containing stitched image
    '''
    n=int(len(list_images)/2+0.5)
    left=list_images[:n]
    right=list_images[n-1:]
    right.reverse()
    while len(left)>1:
        dst_img=left.pop()
        src_img=left.pop()
        left_pano,_,_,_=warpTwoImages(src_img,dst_img,smoothing_window)
        left_pano=left_pano.astype('uint8')
        left.append(left_pano)

    while len(right)>1:
        dst_img=right.pop()
        src_img=right.pop()
        right_pano,_,_,_=warpTwoImages(src_img,dst_img,smoothing_window)
        right_pano=right_pano.astype('uint8')
        right.append(right_pano)

    #if width_right_pano > width_left_pano, Select right_pano as pivot. Otherwise is left_pano
    if(right_pano.shape[1]>=left_pano.shape[1]):
        fullpano,_,_,_=warpTwoImages(left_pano,right_pano)
    else:
        fullpano,_,_,_=warpTwoImages(right_pano,left_pano)
    return fullpano

def crop(panorama,h_dst,conners):
    '''crop panorama based on image which choosing as pivot.
    @param panorama is the panorama
    @param h_dst is the hight of pivot image
    @param conner is the tuple which containing 4 conners of transformed image and 
    4 conners of pivot image'''
    #find max min of x,y coordinate
    [xmin, ymin] = np.int32(conners.min(axis=0).ravel() - 0.5)
    [xmax, ymax] = np.int32(conners.max(axis=0).ravel() + 0.5)
    t = [-xmin,-ymin]
    conners=conners.astype(int)

    #conners[0][0][0] is the X coordinate of top-left point of transformed image
    #If it has value<0, transformed image is merged to the left side of pivot image
    #otherwise is merged to the right side of pivot image
    if conners[0][0][0]<0:
        n=abs(-conners[1][0][0]+conners[0][0][0])
        panorama=panorama[t[1]:h_dst+t[1],n:,:]
    else:
        if(conners[2][0][0]<conners[3][0][0]):
            panorama=panorama[t[1]:h_dst+t[1],0:conners[2][0][0],:]
        else:
            panorama=panorama[t[1]:h_dst+t[1],0:conners[3][0][0],:]
    return panorama
