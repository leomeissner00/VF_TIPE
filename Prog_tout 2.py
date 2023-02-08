#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 10:37:50 2021

@author: leomeissner


"""

import random as rd
import copy
import matplotlib.pyplot as plt
import numpy as np
L = 100      #nb de lignes
l = 100      #nb de colonnes
p = 0.5         #densité
z=2             #sommes des cases sur z "couches" autour


## Partie relative à la forêt de base

# Création de la forêt de densité p et de taille Lxl

def bernoulli(p):
    return 1 if rd.random() < p else 0


def creation_tableau(L, l, p):
    tabl = np.zeros([L,l])
    for i in range (2,L-2):
        for j in range (2,l-2):
            if bernoulli(p)== 1:
                tabl[i,j]=1
            else:
                tabl[i,j]=0

    return tabl


## Sous-fonctions

# Calcul du tour à létape n+1 à partir du tour à létape n

def tour_suivant(tabl,tabl_arbre_duree,tabl_arbre_max, compteur):
    tabl_nouv = copy.deepcopy(tabl)
    for i in range (2, L-2):
        for j in range (2, l-2):
            somme = somme_cases(i,j, tabl)
            if tabl[i, j] == 20:
                if tabl_arbre_duree[i,j] == tabl_arbre_max[i,j]:
                    tabl_arbre_duree[i,j] = 0
                    tabl_arbre_max[i,j] = 0
                    tabl_nouv[i,j] = 0.1
                    compteur -=1
                else:
                    tabl_arbre_duree[i,j] += 1
            if tabl [i, j] == 1:
                if somme >= 20:
                    tabl_nouv [i,j]= 20
                    tabl_arbre_max[i,j] = rd.randint(2,3)
                    tabl_arbre_duree[i,j] = 1
                    compteur += 1

    return tabl_nouv, compteur, tabl_arbre_duree,tabl_arbre_max



# Fait la somme des valeurs autour de la case i,j sur z couches

def somme_cases(i,j,tabl):
    somme = 0
    for x in range(-z,z+1):
        for y in range(-z,z+1):
            c=max(np.abs(x),np.abs(y))
            if c==0:
                c=1
            if np.abs(x)==np.abs(y):
                c=c*2
            somme += (1/c)*(tabl[i-x, j-y])

    return somme




## Script principale qui regroupe toutes les sous-parties

def jeu_de_la_vie (p):
    tabl = creation_tableau(L,l,p)
    # capteurs = creation_capteurs(L,l)
    tabl_arbre_duree = np.zeros ([L,l])
    tabl_arbre_max = np.zeros ([L,l])
    tabl[25,25]= 20
    compteur = 1
    percol = False
    plt.show()
    while compteur != 0 and not percol :
        tabl_aff = correction_affichage(tabl)
        # capteurs_aff=correction_affichage(capteurs)
        # tabl_general = tabl_et_capt(tabl_aff, capteurs_aff)
        plt.clf()
        plt.matshow(tabl_aff,fignum = 0, cmap='nipy_spectral_r')
        plt.show()
        plt.pause(0.05)
        # capteurs = tabl_capteurs_suivant(capteurs, tabl)
        a = tour_suivant(tabl,tabl_arbre_duree,tabl_arbre_max,compteur)
        tabl = a[0]
        compteur = a[1]
        for i in range (2,L-2):
            if tabl [i,l-3] == 20:
                percol = True

    return percol


def correction_affichage(tabl):
    tabl_aff = copy.deepcopy(tabl)
    for i in range (L):
            for j in range(L):
                if tabl[i, j] == 1:
                    tabl_aff[i, j] =56
                if tabl [i, j] == 0.1:
                    tabl_aff [i, j] = 0
                if tabl [i, j] == 0:
                    tabl_aff [i, j] = 100
                if tabl [i, j] ==20:
                    tabl_aff [i, j] = 20
                if tabl [i, j] == 0.001:
                    tabl_aff [i, j] = 80
    return tabl_aff
