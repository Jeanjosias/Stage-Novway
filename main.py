#### main file ####
#from http import client

import numpy as np
from deep_learning import *
from real_data.restaurant_searching import *
from generated_data.restaurant_generated import *
from generated_data.restaurant3times_generated import *
from generated_data.helper import *

def run_searching() :
    list_next_day = []
    resto1 = Model()
    number_set = 20
    for i in range(number_set) :
        alpha = random.randint(-1,2)
        beta = random.randint(-1,2)
        
        choise1 = random.randint(0,3)
        choise2 = random.randint(0,3)
        
        arrival_choise = random.randint(0,3) 
        
        liste = [len(liste_day[choise1]["waiting"]), len(beta*liste_day[choise2]["waiting"])]
        min_liste = min(liste)
        
        waiting = alpha*liste_day[choise1]["waiting"] + beta*liste_day[choise2]["waiting"]
        waiting = waiting.iloc[:min_liste]
        
        #print("Nan nunber waiting", waiting.isna().sum().sum())
        #waiting = pd.DataFrame(waiting, column = waiting)
        arrival = liste_day[arrival_choise]["arrival"]
        liste = [len(waiting), len(arrival)]
        min_liste = min(liste)
        #print("Nan nunber arrival", arrival.isna().sum().sum())
        
        data_generate = pd.concat([arrival, waiting], axis = 1)
        data_generate = data_generate[:min_liste]
        #print("Nan nunber data_generate", data_generate.isna().sum().sum())
        
        #print("")
        resto1.get_data(data_generate)

    number_set = 20
    for i in range(number_set) :
        alpha = random.randint(-1,2)
        beta = random.randint(-1,2)
        
        choise1 = random.randint(0,3)
        choise2 = random.randint(0,3)
        
        arrival_choise = random.randint(0,3) 
        
        liste = [len(liste_day[choise1]["waiting"]), len(beta*liste_day[choise2]["waiting"])]
        min_liste = min(liste)
        
        waiting = alpha*liste_day[choise1]["waiting"] + beta*liste_day[choise2]["waiting"]
        waiting = waiting.iloc[:min_liste]
        
        #print("Nan nunber waiting", waiting.isna().sum().sum())
        #waiting = pd.DataFrame(waiting, column = waiting)
        arrival = liste_day[arrival_choise]["arrival"]
        liste = [len(waiting), len(arrival)]
        min_liste = min(liste)
        #print("Nan nunber arrival", arrival.isna().sum().sum())
        
        data_generate = pd.concat([arrival, waiting], axis = 1)
        data_generate = data_generate[:min_liste]
        #print("Nan nunber data_generate", data_generate.isna().sum().sum())
        
        #print("")
        resto1.get_data(data_generate)
        next = resto1.prediction_next_day()
        list_next_day.append(next)
        
        print("************ iteration", i,"**************")

def run_generated() :
    rest = Model()
    esperance_client_number = random.randint(50, 150)
    variance_client_number = random.randint(20, 40)
    
    accompagneur_max = random.randint(3, 6)
    time_service = random.randint(int(esperance_client_number*1.5), int(esperance_client_number*3.5))
    number_table = esperance_client_number//10
    number_cuisinier = number_table//3
    table = random.randint(1, accompagneur_max+1, number_table)
    performance = random.randint(3, 6)
    
    for i in range(40) :
        client_mumber = random.randint(esperance_client_number-variance_client_number, 
                                   esperance_client_number+variance_client_number)
        day = resto(client_mumber, accompagneur_max, time_service, table, number_cuisinier, performance)
        
        rest.get_data(day)
    
    liste_forcast = []
    for i in range(20) :      
        day = resto(client_mumber, accompagneur_max, time_service, table, number_cuisinier, performance)
        rest.get_data(day)
        forcast = rest.prediction_next_day()
        liste_forcast.append(forcast)
        print("************ iteration", i,"**************")
        
def run_3timesgenerated() :
    rest = Model()
    esperance_client_number = random.randint(150, 300)
    variance_client_number = random.randint(20, 40)
    
    accompagneur_max = random.randint(3, 6)
    time_service = random.randint(int(esperance_client_number*3.5), int(esperance_client_number*5.5))
    number_table = esperance_client_number//10
    number_cuisinier = number_table//3
    table = random.randint(1, accompagneur_max+1, number_table)
    performance = random.randint(3, 6)
    
    for i in range(40) :
        client_mumber = random.randint(esperance_client_number-variance_client_number, 
                                   esperance_client_number+variance_client_number)
        day = resto3times(client_mumber, accompagneur_max, time_service, table, number_cuisinier, performance)
        
        rest.get_data(day)
    
    liste_forcast = []
    for i in range(20) :      
        day = resto3times(client_mumber, accompagneur_max, time_service, table, number_cuisinier, performance)
        rest.get_data(day)
        forcast = rest.prediction_next_day()
        liste_forcast.append(forcast)
        print("************ iteration", i,"**************")
        

if __name__ == "__main__" :
    
    #run_3timesgenerated() 
    run_searching()