#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 13:33:25 2021

@author: leomeissner
"""
import random as rd
import copy
import matplotlib.pyplot as plt
import numpy as np



def diffusion(N0, T, H, L, nbfile = 4):
    N = [[0 for j in range (H)]for i in range (L)]
    N[2][2] = N0

    
    
    
    for t in range(T):
        Np = copy.deepcopy(N)

        for i in range(L):
            for j in range (H):
                # Pas vent
                Coord =[[i-1,j-1],[i,j-1],[i+1,j-1],[i-1,j],[i,j],[i+1,j],[i-1,j+1],[i,j+1],[i+1,j+1],[i-1,j-1],[i,j-1],[i+1,j-1],[i-1,j],[i,j],[i+1,j],[i-1,j+1],[i,j+1],[i+1,j+1], [i-1,j-1],[i,j-1],[i+1,j-1],[i-1,j],[i,j],[i+1,j],[i-1,j+1],[i,j+1],[i+1,j+1]]
                #Vent
                Coord_E =[[i-2,j+1],[i-2,j+2],[i-1,j+2],[i,j+2], [i+1,j+2],[i+2,j+2], [i+2,j+1]]
                Diag = [[i+2,j],[i+2,j+1],[i+2,j+2],[i+1,j+2], [i,j+2],[i-1,j+2], [i+2,j-1]]
                


                vent = Coord + Coord_E
                if N[i][j] >0:
                    nb = Np[i][j]
                    Np[i][j] = 0
                    for k in range (int(nb)):
                        Dpl = vent
                        a = rd.randint(0,len(Dpl)-1)
                        inew,jnew=Dpl[a]
                            
                        Np[inew][jnew]+= 1

    

                        
        N=copy.deepcopy(Np)
        
        
        plt.clf()
        plt.matshow(N,fignum = 0, cmap='nipy_spectral_r')
        plt.show()
        plt.pause(0.05)
        

    
    plt.clf()
    temps = [j for j in range (T+1)]
    # plt.plot(temps,rayon)
    # plt.title('Résultats avec 10 essais par densité', fontsize = 18)
    # plt.xlabel('Temps', fontsize = 16)
    # plt.ylabel('Rayon', fontsize = 16)
    
    x = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    y = []
    for i in range (L):
        for j in range (H):
            w = N[i][j]
            print(w)
            for k in range (w):
                if (j == 1) and (i!=0)and i!=4:
                    y.append(i-1)
                if j == 2 and (i!=0)and i!=4:
                    y.append(i+3-1)
                if j == 3 and (i!=0)and i!=4:
                    y.append(i+6-1)
                if i == 0 and j == 3:
                    y.append(9)
                if i == 0 and j == 4:
                    y.append(10)
                if i == 1 and j == 4:
                    y.append(11)
                if i == 2 and j == 4:
                    y.append(12)
                if i == 3 and j == 4:
                    y.append(13)
                if i == 4 and j == 4:
                    y.append(14)
                if i == 4 and j == 3:
                    y.append(15)
                

            
    plt.hist(y, range = (0, 16), bins = 16, color = 'green', edgecolor = 'blue', density = True)
    plt.xlabel('Numéro de case', fontsize = 16)
    plt.ylabel('Probabilités', fontsize = 18)
    plt.title("Probabilité de déplacement d'une particule", fontsize = 16)
    plt.show()

    return 


nbfile= 4
T=1; H=5; L=5; N0=100000
diffusion(N0,T,H,L)

