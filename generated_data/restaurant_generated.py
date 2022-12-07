from helper import *
#from generated_data.helper import *


def resto(Nombre_client, Accompagneur_max, Temps_ouverture, Table_disponible, cuisinier_disponible, performance) : 
    
    Clients = [i+1 for i in range(Nombre_client)]
    systeme = pd.DataFrame({"Clients" : Clients})
    Instant_arrive = random.sample(range(Temps_ouverture), Nombre_client)

    Instant_arrive.sort()
    Instant_arrive[0] = 0

    systeme = systeme.assign(arrival = Instant_arrive)


    column_elements = [0 for i in range(Nombre_client)]
    column_title = ['Accompagnant', 'Table_souhaite', 'Nombre_entree', 'Nombre_resistance', 
                    'Nombre_dessert', 'Temps_preparation', 
                    'Temps_pour_manger', 'Temps_de_relaxation', 'waiting']

    for i in range(len(column_title)) :
        systeme.insert(i+2, column_title[i], column_elements)

    #Parametres
    Client = systeme["Clients"]
    Temps_attente = systeme["waiting"]
    Accompagnant = systeme[["Clients", "Accompagnant"]] 
    Instant_arrive = systeme[["Clients", "arrival"]] 
    Liste_attente = Client.copy()
    
    Table_occupe = []
     
    t = 0  
    Patience = []
    Liste_attente_cuisinier = []
    Temps_preparation_restant = []
    Temps_pour_manger_restant = []
    Temps_de_relaxation_restant = []
    Liste_sortie = []
    cont = True
    while cont : 
        if len(Liste_sortie) == Nombre_client :
            cont = False 
            print("ok")
        if t > 4000 :
            cont = False
            print("no")
        if len(Liste_attente) != 0 : 
            for client in Liste_attente :
                    client = min(Liste_attente)
                    j = client - 1 
                    if t >= Instant_arrive.iloc[j,1] : 
                        Accompagneur(client, systeme, Accompagneur_max)
                        Liste_attente = Liste_attente.drop(j, axis = 0)
                        table = Table(client, systeme)
                        if Entree(client, table, Table_disponible, Table_occupe) == True : 
                            Plat_choisi(client, systeme)
                            cuisine = Temps_cuisine(client, systeme, performance)
                            if len(Liste_attente_cuisinier) != 0 :
                                if cuisinier_disponible != 0 : 
                                        cuisinier_disponible = cuisinier_disponible-1
                                        Temps_preparation_restant.append(Liste_attente_cuisinier[0])
                                        del Liste_attente_cuisinier[0]                                                                                                         
                                        Liste_attente_cuisinier.append([client, cuisine])    
                                else :
                                        Liste_attente_cuisinier.append([client, cuisine])    
                            if len(Liste_attente_cuisinier) == 0 :
                                if cuisinier_disponible != 0 :
                                        cuisinier_disponible -= 1
                                        Temps_preparation_restant.append([client, cuisine])
                                else :
                                        Liste_attente_cuisinier.append([client, cuisine])
                            
                        
                        else :
                            Patience.append([client, table])
                            if len(Liste_attente_cuisinier) != 0 :
                                if cuisinier_disponible != 0 : 
                                        cuisinier_disponible = cuisinier_disponible-1
                                        Temps_preparation_restant.append(Liste_attente_cuisinier[0])
                                        del Liste_attente_cuisinier[0]                                                                                                         
                    else :      
                        if len(Liste_attente_cuisinier) != 0 :
                            if cuisinier_disponible != 0 : 
                                cuisinier_disponible = cuisinier_disponible-1
                                Temps_preparation_restant.append(Liste_attente_cuisinier[0])
                                del Liste_attente_cuisinier[0]                                                                                                         
                        
                    if Fonction_test_zero(Temps_preparation_restant) == True :                         
                        for i in range(len(Temps_preparation_restant)) :
                            if Temps_preparation_restant[i][1] == 0 :
                                
                                cuisinier_disponible = cuisinier_disponible + 1 
                                Client_associe_preparation = Temps_preparation_restant[i][0]
                                manger = Temps_manger(client, systeme, Accompagnant)
                                Temps_pour_manger_restant.append([Client_associe_preparation, manger])
                        
                        if Fonction_test_zero(Temps_pour_manger_restant) == True :
                            for z in range(len(Temps_pour_manger_restant)) :
                                if Temps_pour_manger_restant[z][1] == 0 : 
                                        Client_associe_manger = Temps_pour_manger_restant[z][0] 
                                        relaxation = Temps_relaxation(client, systeme)
                                        Temps_de_relaxation_restant.append([Client_associe_manger, relaxation])                   
                        
                            if Fonction_test_zero(Temps_de_relaxation_restant) == True :
                                Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                t += 1
                            else :
                                Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                t += 1
                        else :                                     
                            if len(Temps_de_relaxation_restant) != 0 :
                                if Fonction_test_zero(Temps_de_relaxation_restant) == True :
                                        Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                        Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                        Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                        t += 1                                                         
                                else :
                                        Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                        Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                        Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                        t += 1
                            else :
                                Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                t += 1
                                                            
                    else :
                            if len(Temps_pour_manger_restant) != 0 : 
                                if Fonction_test_zero(Temps_pour_manger_restant) == True :
                                
                                        for z in range(len(Temps_pour_manger_restant)) :
                                            if Temps_pour_manger_restant[z][1] == 0 : 
                                                Client_associe_manger = Temps_pour_manger_restant[z][0] 
                                                relaxation = Temps_relaxation(client, systeme)
                                                Temps_de_relaxation_restant.append([Client_associe_manger, relaxation])                   
                                        
                                        if Fonction_test_zero(Temps_de_relaxation_restant) == True :
                                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                            t += 1
                                            
                                        else :
                                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                            t += 1     
                                else :
                                        if len(Temps_de_relaxation_restant) != 0 :
                                            if Fonction_test_zero(Temps_de_relaxation_restant) == True :
                                                Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                                Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                                Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                                t += 1                                               
                                            else :
                                                Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                                Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                                Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                                t += 1
                                        else :
                                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                            t += 1                                                            
                            else :
                                if len(Temps_de_relaxation_restant) != 0 :
                                        if Fonction_test_zero(Temps_de_relaxation_restant) == True :    
                                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                            t += 1
                                            
                                        else :
                                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                            t += 1                                         
                                else : 
                                        Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                        Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                        Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                        t += 1
    
        else :         
            if len(Liste_attente_cuisinier) != 0 :
                    if cuisinier_disponible != 0 : 
                        cuisinier_disponible = cuisinier_disponible-1
                        Temps_preparation_restant.append(Liste_attente_cuisinier[0])
                        del Liste_attente_cuisinier[0]
                        
            if Fonction_test_zero(Temps_preparation_restant) == True :  
                    for i in range(len(Temps_preparation_restant)) :
                        if Temps_preparation_restant[i][1] == 0 :
                            
                            cuisinier_disponible = cuisinier_disponible + 1 
                            Client_associe_preparation = Temps_preparation_restant[i][0]
                            manger = Temps_manger(client, systeme, Accompagnant)
                            Temps_pour_manger_restant.append([Client_associe_preparation, manger])
                    
                    if Fonction_test_zero(Temps_pour_manger_restant) == True :
                        for z in range(len(Temps_pour_manger_restant)) :
                            if Temps_pour_manger_restant[z][1] == 0 : 
                                Client_associe_manger = Temps_pour_manger_restant[z][0] 
                                relaxation = Temps_relaxation(client, systeme)
                                Temps_de_relaxation_restant.append([Client_associe_manger, relaxation])                   
                    
                        if Fonction_test_zero(Temps_de_relaxation_restant) == True :
                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                            t += 1
                        else :
                            
                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                            t += 1
                    else :                                     
                        if len(Temps_de_relaxation_restant) != 0 :
                            if Fonction_test_zero(Temps_de_relaxation_restant) == True :
                                Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                t += 1                                                         
                            else :
                                Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                t += 1
                        else :
                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                            t += 1
                                                    
            else :
                        if len(Temps_pour_manger_restant) != 0 : 
                            if Fonction_test_zero(Temps_pour_manger_restant) == True :
                                
                                for z in range(len(Temps_pour_manger_restant)) :
                                        if Temps_pour_manger_restant[z][1] == 0 :
                                            Client_associe_manger = Temps_pour_manger_restant[z][0] 
                                            relaxation = Temps_relaxation(client, systeme)
                                            Temps_de_relaxation_restant.append([Client_associe_manger, relaxation])                   
                                
                                if Fonction_test_zero(Temps_de_relaxation_restant) == True :
                                        Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                        Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                        Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                        t += 1
                                        
                                else :
                                        Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                        Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                        Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                        t += 1        
                            else :
                                if len(Temps_de_relaxation_restant) != 0 :
                                        if Fonction_test_zero(Temps_de_relaxation_restant) == True :
                                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                            t += 1                                               
                                        else :
                                            Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                            Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                            Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                            t += 1
                                else :
                                        Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                        Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                        Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                        t += 1                                                             
                        else :
                            if len(Temps_de_relaxation_restant) != 0 :
                                if Fonction_test_zero(Temps_de_relaxation_restant) == True :    
                                        Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                        Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                        Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                        t += 1
                                        
                                else :
                                        Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                        Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                        Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                        t += 1                                         
                            else : 
                                Reprogramation (Temps_de_relaxation_restant, Patience, 
                    Table_occupe, Liste_attente)
                                Sortie(Temps_de_relaxation_restant, Table_occupe, 
           Liste_sortie, Table_disponible)
                                Temps(Temps_preparation_restant, Temps_pour_manger_restant, 
          Temps_de_relaxation_restant, Patience, Temps_attente)
                                t += 1
    
    #time_max = systeme["Temps_attente"].max()
    time_max = 500
    systeme["waiting"] = 120*systeme["waiting"]//time_max
    
    systemee = systeme[["arrival","waiting"]]
    
    return systeme

df = resto(102, 3, 800, [2,2,2,2,3,3,4,4], 6, 3)

print(df) 