import numpy as np
import random
import pandas as pd
import tensorflow as tf
from generated_data import *

class Model :
    """
    Model of prediction based on restaurant's data
    """
    def __init__(self) :
        """
        Init variables
        """
        #self.database = pd.DataFrame(columns = ["donnee"])
        self.database = []
        self.batch = 15
        self.mean, self.std = 0, 0
             
    def get_data(self, dataset) :
        """
        add new dataset
        """
        #print("shape_init", dataset.shape)
        #print("Nan nunber", dataset.isna().sum().sum())
        dataset = self.clean_data(dataset)
        #print("shape_finale", dataset.shape)
        #print("Nan nunber", dataset.isna().sum().sum())
        self.database.append(dataset)
        
        #print("get_data done")
        
    def clean_data(self, data) :
        """
        """
        arrival = data["arrival"]
        #high_value = arrival.max()
        liste_stock = []
        for i in range(len(arrival)-1) :
            if arrival.iloc[i] == arrival.iloc[i+1] :
                liste_stock.append(i+1)
        data.drop(liste_stock, inplace = True)
        data.reset_index(drop=True, inplace=True)
        return data
    
    def preprocessing_data(self, data) :
        """
        """
        #print("data",data.head(100))
        arrival = data["arrival"].astype(int)
        waiting = data["waiting"]
        max_value = arrival.max() + 1
        #max_value = int(max_value)
        data_waiting = np.zeros(max_value)
        #print("data_waiting", np.shape(data_waiting))
        
        for j in range(len(waiting)) :
            data_waiting[arrival.iloc[j]] = waiting.iloc[j] 

        #Change zero's values
        for j in range(1,len(data_waiting)) :
            if data_waiting[j] == 0 :
                data_waiting[j] = data_waiting[j-1]
        #print(np.shape(data_waiting))
        #data_waiting = np.expand_dims(data_waiting, axis=-1)
        #print(np.shape(data_waiting))
        #print(data_waiting)
        return data_waiting
        
    def generate_data_rnn(self) :
        """
        turn data to list. The index are arrival the value are the waiting link to the arrival 
        """
        data_rnn = []
        for i in range(len(self.database)) :
            #print(i)
            data_waiting = self.preprocessing_data(self.database[i])

            data_rnn.append(np.array(data_waiting))
            #print(len(data_rnn))

        print("generate_data_rnn done")
        return data_rnn
    
    def visualisation(self) :
        """
        visualise dataset to see evolution of the curbe
        """
        data_visualise = np.concatenate(self.generate_data_rnn(), axis = 0)
        data_visualise = pd.DataFrame({"waiting":data_visualise})
        
        print("visualise done")
        return data_visualise
    
    def normalise(self, data) :
        """
        Normalise dataset. rnn methode is sensibled to high values
        """
        
        mean = data.mean()
        std = data.std()
        print("normalise done")
        return mean, std
    
    def generate_batch(self, n_future = 1) :    
        """
        generate batch for training 
        """
        train_X =  []
        train_Y =  []

        list_len = []
        data_rnn = self.generate_data_rnn()
        print(len(data_rnn))
        data = np.concatenate(data_rnn, axis = 0)
        data = pd.DataFrame({"waiting":data})
        self.mean, self.std = self.normalise(data)
        
        
        data_batch = self.generate_data_rnn()
        len_data_batch = len(data_batch)
        
        #normalise dataset
        for i in range(len_data_batch) :
            data_batch[i] = (data_batch[i]-self.mean.iloc[0])/self.std.iloc[0]
            list_len.append(len(data_batch[i]))
            
        #print("normalise",data_batch)
        max_len = max(list_len)
        index_max = list_len.index(max_len)
        max_data = data_batch[index_max]
        
        #print("min_len", min_len)
        for i in range(len_data_batch) :
            data_batch[i] = np.concatenate([data_batch[i], max_data[len(data_batch[i]):]])
            #print(len(data_batch[i]))
        
        if len(data_batch) <= 25 :

            step_batch = len_data_batch-n_future
            for i in range(max_len) :
                X = []
                
                for j in range(step_batch) :        
                    X.append(data_batch[j][i])

                train_X.append(X)
                train_Y.append([data_batch[-1][i]])
            inputs, outputs = np.array(train_X), np.array(train_Y) 
            test = np.concatenate([inputs[-max_len:,-step_batch+1:], outputs[-max_len:]], axis = 1) 
            
        if len(data_batch) > 25 :
            step_batch = 25
            for k in range(len_data_batch-step_batch-n_future+1) :
                for i in range(max_len) :
                    X = []
                    for j in range(k, k+step_batch) :        
                        X.append(data_batch[j][i])

                    train_X.append(X)
                    train_Y.append([data_batch[k+step_batch][i]])
                           
            inputs, outputs = np.array(train_X), np.array(train_Y) 
            test = np.concatenate([inputs[-max_len:,-step_batch+1:], outputs[-max_len:]], axis = 1) 
            
        inputs = np.expand_dims(inputs, axis=-1)
        outputs = np.expand_dims(outputs, axis=-1)
        test = np.expand_dims(test, axis=-1)
        print("inputs{} outputs{} test{}".format(np.shape(inputs), np.shape(outputs), np.shape(test)))
        print("generate_batch done")
        return inputs, outputs, test
   
    def rnn(self, inputs, outputs) :
        """
        compute rnn deep learning method
        """
        #Set model
        model = tf.keras.models.Sequential() 

        model.add(tf.keras.layers.InputLayer(input_shape=(inputs.shape[1],inputs.shape[2])))
        # Stack LSM cells 
        #model.add(tf.keras.layers.LSTM(128, activation = 'relu'))
        model.add(tf.keras.layers.LSTM(128, return_sequences = True))
        model.add(tf.keras.layers.LSTM(128, return_sequences = True))
        model.add(tf.keras.layers.LSTM(128, return_sequences = True))
        model.add(tf.keras.layers.LSTM(128, return_sequences = True))
        model.add(tf.keras.layers.LSTM(128, return_sequences = True))
        model.add(tf.keras.layers.LSTM(128, return_sequences =  False, activation = 'relu'))
                                    
        #model.add(tf.keras.layers.LSTM(128, activation = 'relu'))
        model.add(tf.keras.layers.Dropout(0.2))
        #Create the output of the model
        model.add(tf.keras.layers.Dense(outputs.shape[1]))

        #Compile Model
        model.compile(loss="mse", optimizer="sgd", metrics=["accuracy"])
        
        history = model.fit(inputs, outputs, epochs =10, validation_split=0.1)
        print("******* RNN MODEL SET *******")
        return model

    def prediction_next_day(self) :
        """
        deep learning methode. prediction of next day
        """
        
        inputs, outputs, test = self.generate_batch()
        #print("inputs", inputs)
        #print("outputs", outputs)

        model_rnn = self.rnn(inputs, outputs)
        forcast = model_rnn.predict(test)
        
        forcast_denormalise = forcast*self.std.iloc[0]+self.mean.iloc[0]
        return forcast_denormalise
