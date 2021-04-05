import cv2
from Commun import strel
import numpy as np

def dilatation(im, el):
    return cv2.dilate(im, el)

def erosion(im, el):
    return cv2.erode(im, el)

def gradient(im, el):
    return dilatation(im, el) - erosion(im, el)

def ouverture(im, el):
    return dilatation(erosion(im, el), el)

def fermeture(im, el):
    return erosion(dilatation(im, el), el)

def dilatation_cond(im, m, el):
    dilate=dilatation(m, el)
    return np.minimum(dilate, im)

def erosion_cond(im, m, el):
    erod=erosion(m, el)
    return np.maximum(erod, im)

def reconstruction_inf(im, m, el):
    now = m
    prev = np.zeros(m.shape, m.dtype)
    while not np.array_equal(now, prev):
        prev=now
        now=dilatation_cond(im, now, el)
    return now

def reconstruction_sup(im, m, el):
    now = m
    prev = np.zeros(m.shape, m.dtype)
    while not np.array_equal(now, prev):
        prev=now
        now=erosion_cond(im, now, el)
    return now

def ouverture_recon(im, el_ouv, el_recon):
    m=ouverture(im, el_ouv)
    return reconstruction_inf(im, m, el_recon)

def fermeture_recon(im, el_ferm, el_recon):
    m=fermeture(im, el_ferm)
    return reconstruction_sup(im, m, el_recon)