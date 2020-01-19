"""
Image Stitching Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to stitch two images of overlap into one image.
To this end, you need to find feature points of interest in one image, and then find
the corresponding ones in another image. After this, you can simply stitch the two images
by aligning the matched feature points.
For simplicity, the input two images are only clipped along the horizontal direction, which
means you only need to find the corresponding features in the same rows to achieve image stiching.

Do NOT modify the code provided to you.
You are allowed use APIs provided by numpy and opencv, except “cv2.findHomography()” and
APIs that have “stitch”, “Stitch”, “match” or “Match” in their names, e.g., “cv2.BFMatcher()” and
“cv2.Stitcher.create()”.
"""
import cv2
import numpy as np
import random

def compute_keypoint(image):
    
    gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    kaze = cv2.KAZE_create()
    kp, des = kaze.detectAndCompute(gray,None)
    
    kp = np.float32([i.pt for i in kp])
    return (kp,des)
 
def match_keypoint(kpl,kpr,desl,desr):
    
    matcher = cv2.BFMatcher()
    rawMatches = matcher.knnMatch(desr, desl, 2)
    matches = []
    
    # loop over the raw matches
    for m in rawMatches:
        if m[0].distance < m[1].distance * 0.75:
                matches.append((m[0].trainIdx, m[0].queryIdx))
            
                
    ptsA = np.float32([kpr[i] for (_, i) in matches])
    ptsB = np.float32([kpl[i] for (i, _) in matches])
 
    (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC)
 
    return (matches, H, status)


def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """


    #raise NotImplementedError
    
    kpl,desl=compute_keypoint(left_img)
    kpr,desr=compute_keypoint(right_img)
    
    m,H,s=match_keypoint(kpl,kpr,desl,desr)

    result = cv2.warpPerspective(right_img, H,(right_img.shape[1] + left_img.shape[1], right_img.shape[0]))

    result[0:left_img.shape[0], 0:left_img.shape[1]] = left_img
    
    return result


if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task2_result.jpg',result_image)


