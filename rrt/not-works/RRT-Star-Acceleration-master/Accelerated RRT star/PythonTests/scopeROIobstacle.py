import numpy as np
import cv2
#input is point in img. the function flood from the start point and find all the pixels
#in image that are connnected to the start point pixel AND in the same color
# can think on that as BFS 
# the return rectangle is not minimal. 
def findROI(wholeImg,startPoint): 
    h, w = wholeImg.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    floodflags = 4
    floodflags |= cv2.FLOODFILL_FIXED_RANGE 
    floodflags |= (255 << 8)
    num,im,mask,rect = cv2.floodFill(wholeImg, mask, startPoint, 222, floodflags)
    rect = np.int0(rect)
    return rect #return x,y of ROI and w,h . overall return 4 vars