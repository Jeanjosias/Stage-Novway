#### helper contain fonction used to generate our data ####

import random
import pandas as pd

def Fonction_test_zero(Temps_preparation_restant) :
        if len(Temps_preparation_restant) !=0 :
            Test_zero_preparation = [Temps_preparation_restant[i][1] for i in range(len(Temps_preparation_restant))]
            if 0 in Test_zero_preparation :
                return True  


def Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente) :
    if len(Temps_de_relaxation_restant) != 0 :
        for r in range(len(Temps_de_relaxation_restant)) :
            if Temps_de_relaxation_restant[r][1] == 0 : 
                        Client_associe_relaxation = Temps_de_relaxation_restant[r][0]
                        if len(Patience) != 0 :
                            for w in range(len(Table_occupe)) :
                                if Table_occupe[w][0] == Client_associe_relaxation :
                                        for b in range(len(Patience)) :
                                            if Patience[b][1] <= Table_occupe[w][1] : 
                                                Liste_attente.loc[Patience[b][0]-1] = Patience[b][0]
                                                del Patience[b]
                                                break                
                                        
                                                
def Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible) :
    if len(Temps_de_relaxation_restant) != 0 :
        for r in range(len(Temps_de_relaxation_restant)) :
            if Temps_de_relaxation_restant[r][1] == 0 : 
                    Client_associe_relaxation = Temps_de_relaxation_restant[r][0]  
                    Liste_sortie.append(Client_associe_relaxation) 
                    for i in range(len(Table_occupe)) :
                        if Table_occupe[i][0] == Client_associe_relaxation :           
                            Table_disponible.append(Table_occupe[i][1])

        Mouvement(Temps_de_relaxation_restant)

    
            
def Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente) :
    Mouvement (Temps_preparation_restant)
    Mouvement (Temps_pour_manger_restant)
    
    if len(Temps_preparation_restant) != 0 :
        for n in range(len(Temps_preparation_restant)) :
            Temps_preparation_restant[n][1] -= 1 
    if len(Temps_pour_manger_restant) != 0 :
        for n in range(len(Temps_pour_manger_restant)) :
            Temps_pour_manger_restant[n][1] -= 1 
    if len(Temps_de_relaxation_restant) != 0 :
        for n in range(len(Temps_de_relaxation_restant)) :
            Temps_de_relaxation_restant[n][1] -= 1  
    if len(Patience) != 0 :
        for g in range(len(Patience)) :
            client_patient = Patience[g][0]
            Temps_attente.iloc[client_patient-1] += 1 

def Mouvement (L) :
    P = []
    for i in range(len(L)) : 
        if L[i][1] <= 0 :
            P.append(i)
    P.reverse()      
    for i in P :
        del L[i]


def Table(client, system) :
    table = system["Accompagnant"].iloc[client - 1] + 1
    system["Table_souhaite"].iloc[client - 1] = table
    return table


def Accompagneur(client, system, Accompagneur_max) :
    if system["Accompagnant"].iloc[client - 1] == 0 :
        accompagneur = random.randint(0, Accompagneur_max)
        system["Accompagnant"].iloc[client - 1] = accompagneur


def Plat_choisi(client, system): 
    entree = random.randint(0,3)
    resistance = random.randint(0,3)
    dessert = random.randint(0,3)
    system["Nombre_entree"].iloc[client - 1] = entree
    system["Nombre_resistance"].iloc[client - 1] = resistance
    system["Nombre_dessert"].iloc[client - 1] = dessert

def Temps_cuisine(client, system, performance):
    Tp = (system["Nombre_entree"].iloc[client - 1]*random.randint(6,8) + system["Nombre_resistance"].iloc[client - 1]*random.randint(8,10) + system["Nombre_dessert"].iloc[client - 1]*random.randint(4,6))//performance
    system["Temps_preparation"].iloc[client - 1] = Tp
    return Tp

def Temps_manger(client, system, Accompagnant):
    Tm = (system["Nombre_entree"].iloc[client - 1]*random.randint(5,7) + system["Nombre_resistance"].iloc[client - 1]*random.randint(7,9) + system["Nombre_dessert"].iloc[client - 1]*random.randint(4,6))//(Accompagnant.iloc[client - 1, 1]+1)
    system["Temps_pour_manger"].iloc[client - 1] = Tm
    return Tm

def Temps_relaxation(client, system):
    Tr = random.randint(1,10)
    system["Temps_de_relaxation"].iloc[client - 1] = Tr
    return Tr

def Entree(client, table, Table_disponible, Table_occupe) :
    T = []
    for t in range(len(Table_disponible)) : 
        if table <= Table_disponible[t] : 
            T.append(t)
            break
    if len(T) != 0 :
        if Table_disponible[T[0]] >= table :
            Table_occupe.append([client, Table_disponible[T[0]]])
            for r in range(len(Table_occupe)) :
                    if Table_occupe[r][0] == client :
                        break
            del Table_disponible[T[0]]
            return True
        else :
            return False 
    else :
        return False

