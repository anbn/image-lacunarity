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

#-------------------------------------------------------------------------------

class IntegralImage:
    def __init__(self, img):
        self.int_img = np.zeros(img.shape, dtype='int')
    
        for y in range(img.shape[0]):
            zeile = 0
            for x in range(img.shape[1]):
                zeile += img[y,x]
                self.int_img[y,x] = self.int_img[y-1,x] + zeile 
    
    
    def sum(self, p1, p2):
        """
        to get sum from integral image, p1 and p2 are both included 
            i.e. (0,0)(0,0) is value of first pixel
                 (0,0)(1,1) is value of first 2x2 box
                 (1,1)(1,1) is value of first diagonal pixel
        """
        s = self.int_img[p1[0]+p2[0]-1, p1[1]+p2[1]-1]
        print self.int_img[p1[0]+p2[0]-1, p1[1]+p2[1]-1],
        if p1[0]>0:
            s -= self.int_img[p1[0]-1, p1[1]+p2[1]-1]
        if p1[1]>0:
            s -= self.int_img[p1[0]+p2[0]-1, p1[1]-1]
        if p1[0]>0 and p1[1]>0:
            s += self.int_img[p1[0]-1, p1[1]-1]
            print "+",self.int_img[p1[0], p1[1]],
        print ""
        return s
        
        
        #if p1[1]>0:
        #    s -= self.int_img[p2[0],p1[1]-1]
        #if p1[0]>0:
        #    s -= self.int_img[p1[0]-1,p2[1]]
        #if p1[0]>0 and p1[1]>0:
        #    s += self.int_img[p1[0]-1,p1[1]-1]
        #return s;

#-------------------------------------------------------------------------------

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

    int_img = IntegralImage(img)

    print int_img.int_img


    box_size = 2
    counts = np.zeros(box_size * box_size+1)
    
    print "=",int_img.sum((0,0),(1,1))
    print "=",int_img.sum((0,0),(2,2))
    print "=",int_img.sum((0,0),(3,3))
    print "=",int_img.sum((0,0),(4,4))
    print "=",int_img.sum((1,1),(4,4))
    print "=",int_img.sum((0,0),(12,12))
    print "=",int_img.sum((1,0),(11,12))
    print "=",int_img.sum((2,0),(10,12))

    print "=",int_img.sum((1,2),(11,10))

    #for y in range(img.shape[0]-1):
    #    for x in range(img.shape[1]-1):
    #        s = int_img.sum((y,x),(y+box_size-1,x+box_size-1))
    #        counts[s] += 1

    #print counts
 

    # plt.figure(4),plt.imshow(distribution, cmap="jet"), plt.colorbar()
    # plt.show()
