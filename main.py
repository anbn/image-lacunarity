import os, sys, time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq


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
        

def analyze_lacunarity(img, box_sizes=[1,2,4,8,16,32,64,128]):
    int_img = IntegralImage(img)

    result_log = np.zeros((len(box_sizes)))
    result_lac = np.zeros((len(box_sizes)))

    for n,r in enumerate(box_sizes):
        counts = np.zeros(r*r + 1)
        counts_range = np.arange(r*r+1)
        
        # N(r) = (M-r+1)^2
        for y in range(img.shape[0]-r+1):
            for x in range(img.shape[1]-r+1):
                s = int_img.sum((y,x),(r, r))
                counts[s] += 1

        # to probability distribution
        counts = counts/((img.shape[0]-r+1)*(img.shape[1]-r+1))

        z1 = np.sum(counts_range    * counts)
        z2 = np.sum(counts_range**2 * counts)
        lac = z2/(z1*z1)

        result_log[n] = np.log(r)
        result_lac[n] = np.log(lac)
        print r, lac

    return result_log, result_lac


def fit_and_predict(fx, fy, predict):
    func_linear = lambda params,x: params[0]*x+params[1]
    error_func  = lambda params,fx,fy: func_linear(params,fx)-fy
    final_params,success = leastsq(error_func,(1.0,2.0),args=(np.asarray(fx),np.asarray(fy)))
    predict = func_linear(final_params,predict)
    rmse = np.sqrt(np.mean((predict-fy)**2))
    return predict, rmse


def test():
    img = np.asarray(
          [[1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,0,0,0,0,0,0,0,0,1,1],
           [1,1,0,0,0,0,0,0,0,0,1,1],
           [1,1,0,0,0,0,0,0,0,0,1,1],
           [1,1,0,0,0,0,0,0,0,0,1,1],
           [1,1,0,0,0,0,0,0,0,0,1,1],
           [1,1,0,0,0,0,0,0,0,0,1,1],
           [1,1,0,0,0,0,0,0,0,0,1,1],
           [1,1,0,0,0,0,0,0,0,0,1,1],
           [1,1,0,0,0,0,0,0,0,0,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1]])

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


    img2 = np.zeros((144,144)) # np.round(np.random.rand(1200,1200))

    for y in range(12):
        for x in range(12):
            if img[y,x]==1:
                img2[12*y:12*(y+1),12*x:12*(x+1)] = 1

    plt.imshow(img2, interpolation="none", cmap="gray")
    plt.show()

    lo, la = analyze_lacunarity(img2)
    predicted_la, rmse = fit_and_predict(lo, la, lo)
    print "RMSE", rmse

    plt.plot(lo, la)
    plt.plot(lo, predicted_la)
    plt.show()

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    test()
