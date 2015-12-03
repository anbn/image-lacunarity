import os, sys, time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as sm


#IMAGE_DIR = "images"
IMAGE_DIR = "images"

IMAGE_SIZE = (600, 800)
RESIZE_IMG = 0.5
EDGE_THRES = 0.9


def get_integral_image(img):
    #res = np.cumsum(img)
    #res.reshape(img.shape)
    
    res = np.zeros(img.shape, dtype='int')

    for y in range(img.shape[0]):
        zeile = 0
        for x in range(img.shape[1]):
            zeile += img[y,x]
            res[y,x] = res[y-1,x] + zeile 
    return res


def get_sum(int_img, p1, p2):
    """
    to get sum from integral image, p1 and p2 are both included 
        i.e. (0,0)(0,0) is value of first pixel
             (0,0)(1,1) is value of first 2x2 box
             (1,1)(1,1) is value of first diagonal pixel
    """
    s = int_img[p2]
    if p1[1]>0:
        s -= int_img[p2[0],p1[1]-1]
    if p1[0]>0:
        s -= int_img[p1[0]-1,p2[1]]
    if p1[0]>0 and p1[1]>0:
        s += int_img[p1[0]-1,p1[1]-1]
    return s;

if __name__ == "__main__":
    print "Lacunarity"
    print " started", time.strftime("%a %d.%m.%Y %H.%M")

    np.set_printoptions(precision=4, suppress=True, linewidth=160)

    img = np.asarray(
          [[1,1,0,1,1,1,0,1,0,1,1,0],
           [0,0,0,0,0,1,0,0,0,1,1,1],
           [0,1,0,1,1,1,1,1,0,1,1,0],
           [1,0,1,1,1,0,0,0,0,0,0,0],
           [1,1,0,1,0,1,0,0,1,1,0,0],
           [0,1,0,1,1,0,0,1,0,0,1,0],
           [0,0,0,0,0,1,1,1,1,1,1,1],
           [0,1,1,0,0,0,1,1,1,1,0,0],
           [0,1,1,1,0,1,1,0,1,0,0,1],
           [0,1,0,0,0,0,0,0,0,1,1,1],
           [0,1,0,1,1,1,0,1,1,0,1,0],
           [0,1,0,0,0,1,0,1,1,1,0,1]])

    int_img = get_integral_image(img)

    print img
    print int_img
    print get_sum(int_img, (0,0),(0,0))
    #print get_sum(int_img, (0,0),(11,11))
    #print get_sum(int_img, (1,0),(11,11))
    #print get_sum(int_img, (2,7),(8,9))
    #print get_sum(int_img, (8,1),(11,5))
    #print get_sum(int_img, (0,0),(1,1))
    



    # plt.figure(4),plt.imshow(distribution, cmap="jet"), plt.colorbar()
    # plt.show()
