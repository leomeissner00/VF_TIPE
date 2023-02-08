#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 10:01:59 2021

@author: leomeissner
"""


import random as rd
import copy
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#sur le front doc sur les feux
#https://www.france.tv/france-5/sur-le-front/2321841-des-forets-francaises.html



## Forêt avec maillage carré + diffusion de particules


def main_graphe_carre(N0, L, l, p):
    N = np.zeros([L,l])
    N[int(L/2),int(l/2)] = N0

    
    rayon = []
    compteur_t = 0
    temps=[]
    
    tabl = creation_tableau(L,l,p)
    tabl_arbre_duree = np.zeros ([L,l])
    
    tabl[int(L/2),int(l/2)]= 20
    tabl[int(L/2),int((l/2)+1)]= 20
    tabl[int((L/2)+1),int(l/2)]= 20
    tabl[int((L/2)+1),int((l/2)+1)]= 20
    compteur = 4
    perco = False
    
 
    plt.show()
    while not perco and compteur_t!= 1000 and compteur != 0:
        
        Np = mvt_particules(N, compteur_t)
        mesure_rayon(tabl, rayon)
        perco = test_perco(tabl, perco)
        
        
        compteur_t +=1
        temps.append(compteur_t)
        if compteur_t%100 == 0:
            
            print(compteur_t)
                        
        N=copy.deepcopy(Np)
        
        tabl_aff = correction_affichage(tabl)
        plt.clf()
        plt.matshow(tabl_aff,fignum = 0, cmap='nipy_spectral_r')
        plt.show()
        plt.pause(0.05)
        
        a = tour_suivant(tabl,compteur,N, tabl_arbre_duree)
        tabl = a[0]
        compteur = a[1]
        

    
    plt.clf()
    plt.plot(temps,rayon)
    return perco




def creation_tableau(L, l, p):
    tabl = np.zeros([L,l])
    for i in range (2,L-2):
        for j in range (2,l-2):
            if bernoulli(p)== 1:
                tabl[i,j]=1
            else:
                tabl[i,j]=0
    return tabl




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




def tour_suivant(tabl,compteur, N, tabl_arbre_duree):
    tabl_nouv = copy.deepcopy(tabl)
    for i in range (2, L-2):
        for j in range (2, l-2):
            
            if tabl[i, j] == 20:
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
                
            
            if (tabl [i, j] == 1) or (tabl[i,j] == 0.1):
                
                if (N [i][j] != 0) and (somme_cases(i,j, tabl)>=20):
                    tabl_nouv [i,j]= 20
                    tabl_arbre_duree [i,j] +=1
                    compteur += 1
                
    return tabl_nouv, compteur, N, tabl_arbre_duree




def mesure_rayon (tabl, rayon):
    maxi = 0
    for i in range (int(L/2),L):
            if (i>50) and (tabl[i, int(L/2)] == 20):
                if maxi <= np.sqrt((i-(L/2))**2) :
                        maxi = np.sqrt((i-(L/2))**2)
                
    rayon.append(maxi)
    

def test_perco (tabl, perco):       
    for j in range (L-2):
            if tabl[j,L-3] == 20:
                tabl[j,L-3] = 1000
                perco = True
    return perco



def mvt_particules(N, compteur_t):
    Np = copy.deepcopy(N)
    
    for i in range(L-1):
        for j in range (l-1):
            # Pas vent
            Coord =[[i-1,j-1],[i,j-1],[i+1,j-1],[i-1,j],[i,j],[i+1,j],[i-1,j+1],[i,j+1],[i+1,j+1],[i-1,j-1],[i,j-1],[i+1,j-1],[i-1,j],[i,j],[i+1,j],[i-1,j+1],[i,j+1],[i+1,j+1], [i-1,j-1],[i,j-1],[i+1,j-1],[i-1,j],[i,j],[i+1,j],[i-1,j+1],[i,j+1],[i+1,j+1]]
            #Vent
            Coord_E =[[i-2,j+1],[i-2,j+2],[i-1,j+2],[i,j+2], [i+1,j+2],[i+2,j+2], [i+2,j+1]]
            Diag = [[i+2,j],[i+2,j+1],[i+2,j+2],[i+1,j+2], [i,j+2],[i-1,j+2], [i+2,j-1]]
            
            if compteur_t <= 70:
                vent = Diag
            else :
                vent = Coord_E
            if N[i,j] >0:
                nb = Np[i,j]
                Np[i,j] = 0
                for k in range (int(nb)):
                    
                    if j<L-3 or i<L-3 or i> 2:
                        Dpl = Coord + vent
                    else :
                        Dpl = Coord
                    a = rd.randint(0,len(Dpl)-1)
                    
                    
                    
                    inew,jnew=Dpl[a]
                        
                    Np[inew,jnew]+= 1
    return Np
        

        
## Utile pour tout


def bernoulli(p):
    return 1 if rd.random() < p else 0



def correction_affichage(tabl):
    tabl_aff = copy.deepcopy(tabl)
    for i in range (1,L-1):
        for j in range (1,l-1):
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
    essai = 10
    for k in range (essai):
        percol = main_graphe_carre(N0,L,l,p)
        if percol :
            N_reussite += 1
    percent = N_reussite / essai
    return percent



def diagramme ():
    x = []
    y = []
    for k in range (25,75):
        p = 0.01 * k
        f = Nbre_reussite(p)
        x.append(p)
        y.append(f)

    return (x,y)


x = [0.25,0.26,0.27,0.28,0.29,0.29,0.30,0.31,0.32]
y = [0.00,0.00,0.00,0.00,0.00,0.00,0.01,0.07,0.07]

L=200; N0=10000; l =200; z =2; p= 0.82



def func(x, a):
    return np.sqrt(2*a*x)

def graphe(func,N0, L, l, p):
    liste= main_graphe_carre(N0, L, l, p)
    plt.clf()
    coeff, pcov = curve_fit(func, liste[1], liste[2])
    lx = liste[1]
    ly = [func(x, coeff[0]) for x in lx]
    plt.clf()
    plt.xlabel('temps')
    plt.ylabel('rayon du front de feu')
    plt.title('Courbe de l\'avancée du front de feu')
    plt.plot(lx,ly)
    plt.plot(lx,liste[2])
    plt.show()
    print(coeff)



## Forêt avec le maillage en triangle:

n = 200
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
        
        tabl_aff = correction_affichage(tabl_T)
        plt.clf()
        plt.matshow(tabl_aff,fignum = 0, cmap='nipy_spectral_r')
        plt.show()
        plt.pause(0.05)
        
        a = tour_suivant_T(tabl_T,compteur,N, tabl_arbre_duree)
        tabl_T = a[0]
        compteur = a[1]
        

    return perco                   
     



## Plot des différents graphiques


##Feu 10 essais

# x2 = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
# y2 = [0.0,0.0,0.1,0.3,0.6,0.8,1.0,1.0,1.0,1.0]
# plt.plot(x2, y2, color='g', linestyle=':',marker='.')

# plt.title('Résultats avec 10 essais par densité', fontsize = 18)
# plt.xlabel('Densité de la forêt', fontsize = 16)
# plt.ylabel('Taux de percolation', fontsize = 16)
# plt.show()


## Feu avec 50 essais 

# x = [0.1,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.50,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.61,0.62,0.63,0.64,0.65,0.7,0.8,0.9,1.0]
# y = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.08,0.1,0.22,0.23,0.24,0.28,0.3,0.36,0.4,0.46,0.46,0.47,0.47,0.48,0.5,0.54,0.62,0.62,0.62,0.66,0.64,0.72,0.7,0.82,0.82,0.86,0.87,0.9,0.90,0.9,0.90,0.95,0.95,0.98,0.98,0.98,0.99,1.0 , 1.0, 1.0, 1.0, 1.0]


# plt.plot(x, y, color='r', linestyle=':',marker='.')

# yhat = savgol_filter(y, 51, 5) # window size 51, polynomial order 3


# plt.plot(x,yhat, color='b')
# plt.show()

# plt.title('Résultats avec 50 essais par densité', fontsize = 18)
# plt.xlabel('Densité de la forêt', fontsize = 16)
# plt.ylabel('Taux de percolation', fontsize = 16)





## Billes 10 essais

# x1=[0,0.05,0.1, 0.125,0.17,0.2,0.25,0.35,0.4,0.5,0.625,0.75,0.875,1]

# y1=[0,0,0,0.1,0.2,0.3,0.5,0.6,0.67,0.8,0.9,1,1,1]

# plt.plot(x1,y1, color ='b', linestyle=':', marker= '.')
# plt.title('Courbe statistique des résultats', fontsize = 18)
# plt.xlabel('Densité', fontsize = 16)
# plt.ylabel('Taux de percolation totale', fontsize = 16)
# plt.show()


## Histogramme:

# x = [1, 2, 3, 4, 5, 6, 7, 8, 0]
# y = [1, 2, 3, 4, 5, 6, 7, 8, 0 ,1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 9, 10, 11, 12, 13, 14, 15]
# plt.hist(y, range = (0, 16), bins = 16, color = 'yellow', edgecolor = 'red', density = True)
# plt.xlabel('valeurs')
# plt.ylabel('nombres')
# plt.title('Exemple d\' histogramme simple')



## Ancien modèle:
    
L = 100      #nb de lignes
l = 100      #nb de colonnes
p = 0.5         #densité
z=2             #sommes des cases sur z "couches" autour


## Partie relative à la forêt de base

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



## Annexe

def tabl_et_capt(tabl_aff, capteurs):
    tabl_general = np.zeros([L,2*l])
    for i in range(L):
        for j in range(l):
            tabl_general[i, j] = tabl_aff [i, j]
    for i in range(L):
        for j in range(l):
            tabl_general[i, L + j] = capteurs[i, j]
    return tabl_general


## Partie sur les capteurs


#creer un tableauavec des capteurs toutes les 3 cases

def creation_capteurs(L,l):
    capteurs = np.zeros([L,l])
    for i in range (1,L-1):
        for j in range (1,l-1):
            if j%3 == 0 and i%3 == 0:
                capteurs[i,j]=30
    return capteurs


# calcul le tableau des capteurs pour le tour suivant

def tabl_capteurs_suivant (capteurs, tabl ):
    capteurs_suivant = copy.deepcopy (capteurs)
    for i in range(3,L-3,3):
        for j in range (3,l-3,3):
            somme = somme_cases(i,j,tabl)
            if somme>= 20 :
                capteurs_suivant[i,j] = 70
    return capteurs_suivant

