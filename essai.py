#!/usr/bin/python-3.2
# -*- coding:Utf-8 -*

import random
import math

lamb = 1 #lambda
mu = 1
c = 3 #nombre de serveurs
N = -1 #nombre max dans la file d'attente, -1 si infini
i = 0 #nombre initial de personnes dans la file
phi = 0.000000001 #les serveurs tombent en panne suivant une loi exp de taux phi
r = 1 #temps de réparation des serveurs Exponentiels de taux 1/r

serv = range(c) #serveurs opérationnels et libres
serv_bis = [] #serveurs down qui étaient libres au moment de la défaillance



pertes = 0

def exp(l) :
    return (-1/l * math.log(random.uniform(0,1)))

N_attente = 0 #nombre de personnes dans la file d'attente
N_service = 0 #nombre de personnes en traitement par les serveurs (donc N-service - c est le nombre de serveur libres)

    
liste_chronologique = []
#contient la liste des évenements futurs. Est en fait un tas.
#ses éléments sont des paires (timestamp, action)

def tps_arrivee():
    return exp(lamb)

def tps_traitement() :
    return exp(mu)

def tps_crash():
    return exp(phi)

def tps_rep():
    return exp(r)



def ajout_elem_tas((a,b,c)) :
    indice = len(liste_chronologique)
    liste_chronologique.append((a,b,c))
    while (indice > 0) :
        indice_bis = indice / 2
        #print indice
        #print indice_bis
        print liste_chronologique
        (temps, action, num_serv) = liste_chronologique[indice_bis]
        if (temps <= a) :
            break
        liste_chronologique[indice_bis] = (a,b,c)
        liste_chronologique[indice] = (temps, action, num_serv)
        indice = indice_bis

def min_tas() :
    (a,b,c) = liste_chronologique[0]
    length = len(liste_chronologique) - 1
    (time, action, num_serv) = liste_chronologique[length]
    liste_chronologique[0] = (time, action, num_serv)
    del liste_chronologique[length]
    indice = 0
    indice_bis = 1
    while (indice_bis < length) :
        if (indice_bis < length - 1 and liste_chronologique[indice_bis][0] > liste_chronologique[indice_bis+1][0]):
            indice_bis = indice_bis +1
        if (time > liste_chronologique[indice_bis][0]) :
            liste_chronologique[indice] = liste_chronologique[indice_bis]
            liste_chronologique[indice_bis] = (time, action, num_serv)
            indice = indice_bis
            indice_bis = 2 * indice + 1
        else:
            break
    return (a, b, c)



def arrivee(timestamp) :
    global N_service
    global N_attente
    global pertes
    global serv
    if (serv <> []) :
        N_service = N_service + 1
        num_serv = serv[0]
        del serv[0]
        timestamp_sortie = timestamp + tps_traitement()
        ajout_elem_tas((timestamp_sortie, "sortie", num_serv))
    else :
        if (N == -1 or N > N_attente) :
            N_attente = N_attente + 1
        else :
            pertes = pertes + 1
    ajout_elem_tas((timestamp + tps_arrivee(), "arrivee", -1))

def sortie(timestamp, num_serv) :
    global N_attente
    global N_service
    global serv
    if (N_attente > 0) :
        N_attente = N_attente - 1
        ajout_elem_tas((timestamp + tps_traitement(), "sortie", num_serv))
    else :
        N_attente = 0
        serv.append(num_serv)
        N_service = N_service - 1

def crash(timestamp, num_serv) :
    global serv
    temps_reparation = tps_rep()
    if (not (num_serv in serv)) :
        for each in range(len(liste_chronologique)):
            (time, string, num_serv_bis) = liste_chronologique[each]
            if (num_serv == num_serv_bis):
                liste_chronologique[each] = (time + temps_reparation, string, num_serv)
        ajout_elem_tas((timestamp + temps_reparation + tps_crash(), "crash", num_serv))
    else :
        serv.remove(num_serv)
        ajout_elem_tas((timestamp + temps_reparation, "reparation", num_serv))
        serv_bis.append(num_serv)


def reparation(timestamp, num_serv) :
    serv.append(num_serv)
    serv_bis.remove(num_serv)
    ajout_elem_tas((timestamp + tps_crash(), "crash", num_serv))
            




arrivees = 0
resultats = []

#Simulateur AVEC défaillance des serveurs
b = True
b_bis = True

for each in range(c) :
    ajout_elem_tas((tps_crash(), "crash", each))
    
    
for each in range(i+1) :
    arrivee(0)
    arrivees = arrivees + 1
resultats.append((0, N_service, N_attente))
b = b and (N_service == c-len(serv)-len(serv_bis))
b_bis = b_bis and (N_service == c-len(serv))
                   
while (arrivees < 10):
    (time, action, num_serv) = min_tas()
    print action
    if (action == "arrivee") :
        arrivee(time)
        arrivees = arrivees + 1
    elif (action == "sortie") :
        sortie(time, num_serv)
    elif (action == "reparation") :
        reparation(time, num_serv)
    elif (action == "crash") :
        crash(time, num_serv)
    resultats.append((time, N_service, N_attente))
    b_bis = b_bis and (N_service == c-len(serv))
    b = b and (N_service == c-len(serv)-len(serv_bis))
    print b
    #print liste_chronologique

print resultats
print pertes
print b
print b_bis
