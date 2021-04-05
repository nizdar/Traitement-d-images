import cv2
from Commun import strel, morpho, myutil
import numpy as np


def extraire_sombre(im_flash, s_sombre): # S=115 c bon
    im_Gvert = im_flash[:, :, 1]#ouvrir l'im dans le canal vert
    im_Gvert_seuil = myutil.myseuil(im_Gvert, s_sombre)
    return im_Gvert_seuil

def sans_sombre(im_flash, s_sombre):
    im_sombre=extraire_sombre(im_flash, s_sombre)
    im_Gbleu=im_flash[:, :, 0]#ouvrir l'im dans le canal bleu
    im_Gbleu[im_sombre<1]=255
    return im_Gbleu

def bande_seule(im_flash, s_sombre, s_bande): #s_bande=95 c bon
    im_res=sans_sombre(im_flash, s_sombre)
    im_res = myutil.myseuil(im_res, s_bande)
    el_ferm = strel.build('carre', 6)
    el_recon = strel.build('diamant', 1)
    im_res = morpho.fermeture_recon(im_res, el_ferm, el_recon)
    return im_res

def niveau_lumiere(im_flash, im_nocturne, s_sombre, s_bande):
    res = bande_seule(im_flash, s_sombre, s_bande)
    n = np.mean(im_nocturne[res < 1])
    return n

def existe_inondation(im_flash, im_nocturne, s_sombre, s_bande, seuil):
    n=niveau_lumiere(im_flash, im_nocturne, s_sombre, s_bande)
    if n>seuil :
        return False
    else:
        return True

im_flash = cv2.imread("Images/S6_SousEau_Couleur.jpg")
#im_flash = cv2.imread("Images/S5_Sec_Couleur.jpg")
cv2.imshow('image', im_flash)

im_nocturne = cv2.imread("Images/S6_SousEau_NB.jpg")
#im_nocturne = cv2.imread("Images/S5_Sec_NB.jpg")

#res = sans_sombre(im_flash, 115)

#res=bande_seule(im_flash, 115, 95)



print(existe_inondation(im_flash, im_nocturne, 115, 95, 240))

cv2.waitKey(0)



