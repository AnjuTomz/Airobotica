# Importing necessary packages

import sys
import json
import pandas as pd
import numpy as np
from config import RASA_CSV
from core import preprocessing

# Converting csv to  rasa json file
jd = []
def creating_json(csv1):
    
    #Reading data
    data = pd.read_csv(csv1)

    #Columns to List
    text,intent= preprocessing.columnstoList(data)

    
    
    for i in range(len(data)):
        
        jdata = { "text" : text[i],
                  "intent" : intent[i]
                }
        
        jd.append(jdata)
        


    cdata = { "rasa_nlu_data": {"common_examples":jd}}

 
    with open('/home/ubuntu/jessi/RealEstate/Data/Rasa/RE.json', 'w') as fp:
        json.dump(cdata, fp)
    
  


creating_json(RASA_CSV)
