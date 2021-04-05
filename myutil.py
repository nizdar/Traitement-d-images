import numpy as np
import cv2

def myseuil(im, s):
    im_s = np.zeros(im.shape, im.dtype)
    #im_s = np.zeros(im)
    im_s[im >= s]=255
    return im_s

def myseuil_interactif(im):
    global seuil

    def myseuil_interactif_callback(val):
        global seuil
        seuil=val
        cv2.imshow('Seuil Interactif', myseuil(im, seuil))

    cv2.namedWindow('Seuil Interactif')
    cv2.createTrackbar('Seuil', 'Seuil Interactif', 100, 256, myseuil_interactif_callback)
    myseuil_interactif_callback(100)

    cv2.waitKey(0)
    cv2.destroyWindow('Seuil Interactif')
    return seuil

def bruit_sel(im, p):
    bruit=np.random.rand(im.shape[0], im.shape[1])
    im[bruit<p/100]=255
    return im

def bruit_poivre_sel(im, p):
    bruit=np.random.rand(im.shape[0], im.shape[1])
    im[bruit<p/200]=255
    im[np.logical_and(bruit>=p/200, bruit<p/100)]=0
    return im