#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 17:55:15 2021

@author: leomeissner
"""

import random as rd
import copy
import matplotlib.pyplot as plt
import numpy as np

n = 130
N0= 10000

N = np.zeros([n,n])
N[int(n/4),int(n/4)] = N0



S = []
L_A = []

for i in range (n):
    for j in range(n-i):
        S.append([i,j])
        
for i in range (n):
    for j in range (n-i):
        Adj = [[i+1,j-1], [i,j-1], [i-1,j], [i-1,j+1], [i,j+1], [i+1,j]]
        
        if j == 0:
            Adj = [[i-1,j], [i-1,j+1], [i,j+1], [i+1,j]]
        if i == 0:
            Adj = [[i+1,j-1], [i,j-1], [i,j+1], [i+1,j]]
        if i+j == n-1:
            Adj = [[i+1,j-1], [i,j-1], [i-1,j], [i-1,j+1]]
        
        if j == 0 and i == 0:
            Adj = [[i,j+1], [i+1,j]]
        if i == 0 and i+j == n-1:
            Adj = [[i+1,j-1], [i,j-1]]
        if j == 0 and i+j == n-1:
            Adj =[[i-1,j], [i-1,j+1]]
        

        L_A.append(Adj)
        
def indice_S(elt):
    i,j = elt
    ind = 0
    if i !=0:
        for k in range (i):
            ind += n-k
    if j != 0:
        ind += j
    return ind

def bernoulli(p):
    return 1 if rd.random() < p else 0


def creation_tableau_T(n, p):
    tabl_T = np.zeros([n,n])
    for i in range (n):
        for j in range(n-i):
            if bernoulli(p)== 1:
                tabl_T[i,j]=1
    return tabl_T


def somme_T(i,j, tabl_T):
    k = indice_S([i,j])
    S_adj = L_A[k]
    S_somme = []
    somme = 0
    Adj_adj = copy.deepcopy(S_adj)
    for S in S_adj:
        k = indice_S(S)
        Adj_adj += L_A[k]
    
    for S in Adj_adj:
        if S not in S_somme:
            S_somme.append(S)
        
    for elt in S_somme:
        g= elt[0]
        f=elt[1]
        if elt in S_adj + [[i,j]] :
            somme += tabl_T[g,f]
        else:
            somme += tabl_T[g,f]/4
        
    return somme


def mvt_particules_T(N):
    Np = copy.deepcopy(N)
    for i in range (n):
        for j in range(n-i):
            k = indice_S([i,j])
            Dpl = L_A[k] + [[i,j]]
            if N[i,j] >0:
                nb = Np[i,j]
                Np[i,j] = 0
                for k in range (int(nb)):
                    a = rd.randint(0,len(Dpl)-1)
                    inew,jnew=Dpl[a]
                    Np[inew,jnew]+= 1
                    
    N=copy.deepcopy(Np)
        
                    
    return Np




def tour_suivant_T(tabl_T,compteur, N, tabl_arbre_duree):
    tabl_nouv = copy.deepcopy(tabl_T)
    for i in range (n):
        for j in range(n-i):
            
            if tabl_T[i, j] == 20:
                if N [i][j] != 0:
                    tabl_nouv [i,j]= 20
                    tabl_arbre_duree [i,j] +=1
                else:
                    tabl_nouv[i,j] = 0.1
                    compteur -= 1
                if tabl_arbre_duree[i,j] >= 70 :
                    if bernoulli(0.2):
                        tabl_nouv [i,j]= None
                        compteur -= 1
                
            
            if (tabl_T [i, j] == 1) or (tabl_T[i,j] == 0.1):
                b= somme_T(i,j, tabl_T)
                
                if ((N [i,j] != 0) and b>=20):
                    tabl_nouv [i,j]= 20
                    tabl_arbre_duree [i,j] +=1
                    compteur += 1
                
    return tabl_nouv, compteur, N, tabl_arbre_duree
                    
                    
                    
                    
                    
                    
def main_T(N0, n, p):
    N = np.zeros([n,n])
    N[int(n/4),int(n/4)] = N0

    

    compteur_t = 0
    temps=[]
    
    tabl_T = creation_tableau_T(n,p)
    tabl_arbre_duree = np.zeros ([n,n])
    
    tabl_T[int(n/4),int(n/4)]= 20
    tabl_T[int(n/4),int((n/4)+1)]= 20
    tabl_T[int((n/4)+1),int(n/4)]= 20
    tabl_T[int((n/4)+1),int((n/4)+1)]= 20
    compteur = 4
    perco = False
    
 
    plt.show()
    while not perco and compteur_t!= 1000 and compteur != 0:
        
        Np = mvt_particules_T(N)
        #perco = test_perco(tabl, perco)
        
        
        compteur_t +=1
        temps.append(compteur_t)
        if compteur_t%100 == 0:
            
            print(compteur_t)
                        
        N=copy.deepcopy(Np)
        perco = test_perco(tabl_T, perco)
        
        tabl_aff = correction_affichage(tabl_T)
        plt.clf()
        plt.matshow(tabl_aff,fignum = 0, cmap='nipy_spectral_r')
        plt.show()
        plt.pause(0.05)
        
        a = tour_suivant_T(tabl_T,compteur,N, tabl_arbre_duree)
        tabl_T = a[0]
        compteur = a[1]
        
    return perco                   
                    
                    
                    
                    
                    
def correction_affichage(tabl):
    tabl_aff = copy.deepcopy(tabl)
    for i in range (n):
            for j in range(n-i):
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



def Nbre_reussite (p):
    N_reussite = 0
    essai = 30
    for k in range (essai):
        percol = main_T(N0, n, p)
        if percol :
            N_reussite += 1
    percent = N_reussite / essai
    return percent



def diagramme ():
    x = []
    y = []
    for k in range (50,60):
        p = 0.01 * k
        f = Nbre_reussite(p)
        x.append(p)
        y.append(f)
        print(x)
        print(y)

    return (x,y)

def test_perco (tabl, perco):       
    for j in range (n):
            if tabl[j,0] == 20:
                tabl[j,0] = 1000
                perco = True
    return perco


# Ancienne moyen de rechercher l'indice
# ind = None
#     k = 0
#     while ind == None:
#         if elt == S[k]:
#             ind = k
#         k += 1
#     return ind

#Ancien moyen de faire la somme
# def somme_T(i,j, tabl_T):
#     k = indice_S([i,j])
#     S_adj = L_A[k]
#     somme = tabl_T[i,j]
#     for elt in S_adj:
#         g= elt[0]
#         f=elt[1]
#         somme += tabl_T[g,f]
        
#     return somme    
