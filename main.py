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
    
    
    def sum(self, p1, box_size):
        s = self.int_img[p1[0]+box_size[0]-1, p1[1]+box_size[1]-1]
        if p1[0]>0:
            s -= self.int_img[p1[0]-1, p1[1]+box_size[1]-1]
        if p1[1]>0:
            s -= self.int_img[p1[0]+box_size[0]-1, p1[1]-1]
        if p1[0]>0 and p1[1]>0:
            s += self.int_img[p1[0]-1, p1[1]-1]
        return s
        
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

    r = 2 # box size
    counts = np.zeros(r*r + 1)
    
    # N(r) = (M-r+1)^2
    for y in range(img.shape[0]-r+1):
        for x in range(img.shape[1]-r+1):
            s = int_img.sum((y,x),(r, r))
            counts[s] += 1

    # to probability distribution
    counts = counts/((img.shape[0]-r+1)*(img.shape[1]-r+1))

    print counts

    z1,z2 = 0,0
    for i in range(counts.shape[0]):
        z1 += i * counts[i]
        z2 += i*i * counts[i]

    print z1,z2
    print "Lacunarity =", z2/(z1*z1)

 

    # plt.figure(4),plt.imshow(distribution, cmap="jet"), plt.colorbar()
    # plt.show()
