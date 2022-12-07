########## SET BANK DATASET ############
import pandas as pd
import glob as gb


path = "Projet_py\\Stage_novway\\real_data\\*.xlsx"

file = gb.glob(path)

liste_day = [pd.read_excel(document)[["arrival", "waiting"]] for document in file]


#print(liste_data[0])