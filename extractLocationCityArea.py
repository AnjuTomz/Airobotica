import chat_engine
import pandas as pd
import config as cfg
import replacement
from rep import replacements1

def extract(query):
    info = []
    P_area = []
    P_type = []
    P_location = []
    P_city = []

    data = pd.read_csv(cfg.PREPARED_CSV_PATH)
    property_area = data["Prepared_property_area"].drop_duplicates()#["1bhk","2bhk"]
    for x in property_area:
        P_area.append(replacement.replace(x,replacements1))
    print(P_area)
    property_type = data["Prepared_property_type"].drop_duplicates()#["flat","villa","rk"]
    for x in property_type:
        P_type.append(replacement.replace(x,replacements1))
    print(P_type,"hh")
    property_location = data["Prepared_location"].drop_duplicates()#["hebbal","hsr","electron"]
    for x in property_location:
        P_location.append(replacement.replace(x,replacements1))
    print(P_location)
    property_city = data["Prepared_city"].drop_duplicates()
    for x in property_city:
        P_city.append(replacement.replace(x,replacements1))
    print(P_city)

    extracted_area = [x for x in P_area if x in query.split()]
    info.append(extracted_area)
    extracted_location = [x for x in P_location if x in query.split()]
    info.append(extracted_location)
    extracted_type = [x for x in P_type if x in query.split()]
    info.append(extracted_type)
    extracted_city = [x for x in P_city if x in query.split()]
    info.append(extracted_city)
    print(info)
    if len(info[2]) > 0 and len(info[0]) == 0 and len(info[1]) == 0 and len(info[3]) == 0:#i want flat
        return 3.3
        #return chat_engine.prepare_answer(3.3, "text", 1, "product found", [], "Show property area")
    elif len(info[0]) > 0 and len(info[1]) == 0 and len(info[2]) == 0 and len(info[3]) == 0:#i want 1bhk
        return 3.1
        #return chat_engine.prepare_answer(3.1, "text", 1, "product_found", [], "show flat type")
    elif len(info[0]) > 0 and len(info[3]) > 0 and len(info[1]) == 0 and len(info[2]) == 0:#i want 1bhk in bangalore
        return 3.2
        #return chat_engine.prepare_answer(3.2, "text", 1, "product found", [], "show flat type")
    elif len(info[0]) > 0 and len(info[2]) > 0 and len(info[3]) > 0 and len(info[1]) == 0:#i want 1bhk flat in bangalore
        return 3.4
        #return chat_engine.prepare_answer(3.4, "text", 1, "product found", [], "show location")
    elif len(info[0]) > 0 and len(info[2]) > 0 and len(info[1]) == 0 and len(info[3]) == 0:#i want 1bhk flat
        return 3.5
        #return chat_engine.prepare_answer(3.5,"text", 1, "product found", [], "show city")
    elif len(info[2]) > 0 and len(info[3]) > 0 and len(info[0]) == 0 and len(info[1]) == 0:#i want flat in bangalore
        return 3.6
        #return chat_engine.prepare_answer(3.6,"text", 1, "product found", [], "show property location")
    elif len(info[1]) > 0 and len(info[2]) > 0 and len(info[0]) == 0 and len(info[3]) == 0:#i want flat in hebbal
        return 3.7
    elif len(info[0]) > 0 and len(info[1]) > 0 and len(info[2]) > 0 and len(info[3]) == 0:
        return 3.8
    else:
        return 3
# query = "i want 1bhk in jubile hill "
# a = extract(query)
# print(a)


