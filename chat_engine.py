import sys, simplejson, os
import logging,pandas as pd
import config as cfg
import numpy as np
import json
import re


logger = logging.getLogger(__name__)


if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from operations import rasa_handler, product_filter, preprocessor
from core import creatingtfidf
from core import preprocessing 
from core import training 
from core import similaritymatching_condition 
from sklearn.metrics.pairwise import cosine_similarity
import replacement
from rep import replacements
import extractLocationCityArea

def prepare_answer(status_code, response_type, conf,flow_type,UniqueId,intent="", prod_list="", message ="",keyword="",
                   button="",image="",link=[],video=[],pdf="") :
    ans = {
                "typeOfResponse":response_type,
                "statusCode": status_code,
                "confidence": conf,
                "flow_type": flow_type,
                "UniqueId":UniqueId,
                "intent": intent,
                "data": prod_list,
                "message": message,
                "keyword": keyword,
                "button": button,
                "image": image,
                "link": link,
                "video": video,
                "dropdown": pdf
                
        }

    return simplejson.dumps(ans,ignore_nan=True)


def get_actual_data(unique_id):
    org_data = pd.read_csv(cfg.ACTUAL_CSV_FILE)
    return org_data.loc[org_data['UniqueId'] == unique_id]


def prepare_product(unique_id):
    sample = get_actual_data(unique_id)
    # logger.info(unique_id)
    # logger.info(sample.iloc[0]['Description'])
    # description = ''
    # if not isNaN(sample.iloc[0]['Description']):
    #     description = unicode(sample.iloc[0]['Description'],errors = 'ignore')

    attribute = {
                        "city": sample.iloc[0]['city'],
                        "property_type": sample.iloc[0]['property_type'],
                        "location": sample.iloc[0]['location'],
                        "description": "Some Description",
                        "imageUrl": sample.iloc[0]['property_image'],
                        "salePrice": sample.iloc[0]['sales_price'],
                        "actualPrice": sample.iloc[0]['actual_price'],
                        "property_area":sample.iloc[0]['property_area']
                    }
    return attribute


def answer_not_found():
    but = ["Processors","Graphics","Gaming","Shop","Drivers & Support"]
    return prepare_answer(200, "button", 1,"ui","no uniqueid","No answer", [], "I don't have an answer for this query. You can choose from the below options to know more about AMD:- ","no keyword",but)



def wrapper(company_name, query, request_type, user_id,flow_type):
    
    if re.match(r'^[_#\W]+$', str(query)):
        print(query)
        logger.info("query - {} -Empty query after pre processing \n".format(query))
        return prepare_answer(1, "", 0, flow_type, "", [], "Sorry! I didn't get you. Can you please rephrase your query?")
    elif query.lower() == "rera":
        logger.info("query - {} -Response Successful \n".format(query))
        return prepare_answer(2, "text", 1, flow_type, "FAQ", [], "The Real Estate Act makes it mandatory for all commercial and residential real estate projects where the land is over        500 square metres, or eight apartments, to register with the Real Estate Regulatory Authority (RERA) for launching a project, in order to provide greater transparency in               project-marketing and execution.")
    elif query.lower() == "khata":
        logger.info("query - {} -Response Successful \n".format(query))
        return prepare_answer(2, "text", 1,flow_type, "FAQ", [], "The Khata certificate is issued by the BBMP, the BDA or a village panchayat in the name of the present owner or owners        . This is only an assessment register which compiles all the details of each property in the city")
    if not query:
        logger.error("no input query \n")
        return prepare_answer(500, "", 0, flow_type, "", [], "dont enter empty query")
    print(query)
    query = ' '.join(query.split())
    query = query.lower()


    query = preprocessing.hi_hello_check(query)
    print(query)

    if flow_type == "back":
        print("entered loop")
        repquery = replacement.replace(query,replacements)
        

        print(repquery)
            
        spellc_query = []
        spellc_query.append(repquery)
        spellc_query = preprocessing.spellchecking(spellc_query)
        print(spellc_query)
        squery = ''.join(spellc_query)
        print(squery)
        
        if not squery:
            logger.info("query - {} -Empty query after pre processing \n".format(query))
            return prepare_answer(404,"",0,flow_type,"",[],"Currently i am not trained for this query")

       
        # query = spellcorrected query
        intent,intent_confidence = rasa_handler.fetch_rasa_intent(squery, company_name)
        print(intent)
        
        # intent = "Explore"      # For testing

        if intent == "small talk":

            inputques = []
            inputques.append(query)
            inputques = preprocessing.tokenization_spellcheck(inputques)
                        
                         
            im = creatingtfidf.createTfidfVectorizer_Instance(inputques,training.SMALL_VECT )

            #Loading the tfidf matrix from disk
            qm = np.load(cfg.SMALLTALK_MATRIX)

            #Checking cosine similarity
            coslist = cosine_similarity(qm, im).flatten()
            resp_data,status_code = similaritymatching_condition.similarity_check(query,coslist,training.smresponse)
                      
            resp_data = unicode(resp_data, errors='ignore')
            confidence = max(coslist)
            intent = "small talk"
                                    
             
            
            logger.info("query - {} -Response Successful \n".format(query))


            
            return  prepare_answer(1, "text", confidence,flow_type, intent, [], resp_data)

        elif intent == "FAQ":
            print("Entered loop")
            inp = []
            inp.append(query)
            inp = preprocessing.tokenization_spellcheck(inp)
                        
                         
            im = creatingtfidf.createTfidfVectorizer_Instance(inp,training.FAQ_VECT)

            #Loading the tfidf matrix from disk
            qm = np.load(cfg.FAQ_MATRIX)

            #Checking cosine similarity
            coslist = cosine_similarity(qm, im).flatten()
            resp_data,status_code,keyword = similaritymatching_condition.faqsim_check(query,coslist,training.response,training.keyword)
            print(keyword)     
                        
            resp_data = unicode(resp_data, errors='ignore')
            confidence = max(coslist)
            intent = "FAQ"
            
            logger.info("query - {} -Response Successful \n".format(query))

            
            return prepare_answer(2, "text", confidence, flow_type, intent, [], resp_data,keyword)
            
        elif intent == "Explore":

            stemmed_query = " ".join(preprocessor.tokenize_and_stem(squery))
            print(stemmed_query+"hh")
            stat_code = extractLocationCityArea.extract(stemmed_query)
            if stat_code == 3.3:
                filtered_data = product_filter.stat_3_3(stemmed_query)
                prod_list = []
                filtered_data = filtered_data.iloc[:, ]
                for index, row in filtered_data.iterrows():
                    prod_list.append(prepare_product(row['UniqueId']))
                return prepare_answer(3.3, "image", 1,flow_type, intent, prod_list, "Show property area")
            elif stat_code == 3.1:
                filtered_data = product_filter.stat_3_1(stemmed_query)
                prod_list = []
                filtered_data = filtered_data.iloc[:, ]
                for index, row in filtered_data.iterrows():
                    prod_list.append(prepare_product(row['UniqueId']))
                return prepare_answer(3.1, "image", 1, flow_type, intent, prod_list, "show flat type")
            elif stat_code == 3.2:
                filtered_data = product_filter.stat_3_2(stemmed_query)
                prod_list = []
                filtered_data = filtered_data.iloc[:, ]
                for index, row in filtered_data.iterrows():
                    prod_list.append(prepare_product(row['UniqueId']))
                return prepare_answer(3.2, "image", 1, flow_type, intent, prod_list, "show flat type")
            elif stat_code == 3.4:
                filtered_data = product_filter.stat_3_4(stemmed_query)
                prod_list = []
                filtered_data = filtered_data.iloc[:, ]
                for index, row in filtered_data.iterrows():
                    prod_list.append(prepare_product(row['UniqueId']))
                return prepare_answer(3.4, "image", 1, flow_type, intent, prod_list, "show location")
            elif stat_code == 3.5:
                filtered_data = product_filter.stat_3_5(stemmed_query)
                prod_list = []
                filtered_data = filtered_data.iloc[:, ]
                for index, row in filtered_data.iterrows():
                    prod_list.append(prepare_product(row['UniqueId']))
                return prepare_answer(3.5, "image", 1, flow_type, intent, prod_list, "show city")
            elif stat_code == 3.6:
                filtered_data = product_filter.stat_3_6(stemmed_query)
                prod_list = []
                filtered_data = filtered_data.iloc[:, ]
                for index, row in filtered_data.iterrows():
                    prod_list.append(prepare_product(row['UniqueId']))
                return prepare_answer(3.6, "image", 1, flow_type, intent, prod_list, "show property location")
            elif stat_code == 3.7:
                filtered_data = product_filter.stat_3_7(stemmed_query)
                prod_list = []
                filtered_data = filtered_data.iloc[:, ]
                for index, row in filtered_data.iterrows():
                    prod_list.append(prepare_product(row['UniqueId']))
                return prepare_answer(3.7, "image", 1, flow_type, intent, prod_list, "show property area")
            elif stat_code == 3.8:
                filtered_data = product_filter.stat_3_8(stemmed_query)
                if filtered_data.empty:


                    return prepare_answer(1, "image", 1, flow_type, intent, [], "Property not available.")
                else:
                    prod_list = []
                    filtered_data = filtered_data.iloc[:, ]
                    for index, row in filtered_data.iterrows():
                        prod_list.append(prepare_product(row['UniqueId']))
                    return prepare_answer(3.8, "image", 1, flow_type, intent, prod_list, "show property area")
                
            elif stat_code == 3:
                filtered_data = product_filter.travers(stemmed_query)
                prod_list = []
                print(filtered_data)
                if filtered_data.empty:
                    return prepare_answer(1, "text", 0, flow_type, intent, [],
                                          "No product found, please try rephrasing your query")
                else:
                    filtered_data = filtered_data.iloc[:, ]
                    for index, row in filtered_data.iterrows():
                        prod_list.append(prepare_product(row['UniqueId']))
                    return prepare_answer(3, "image", 0, flow_type, intent, prod_list, "show all images")







    else:

       
       uiquery = []
       uiquery.append(query)
       uiquery = preprocessing.tokenization_spellcheck(uiquery)
       im = creatingtfidf.createTfidfVectorizer_Instance(uiquery,training.UIFLOW_VECT)

       #Loading the tfidf matrix from disk
       qm = np.load(cfg.UIFLOW_MATRIX)
       button=[]
       #Checking cosine similarity
       coslist = cosine_similarity(qm, im).flatten()
       resp_data,status_code,button,image,link,video,pdf,response_type,UniqueId = similaritymatching_condition.ui_simcheck(uiquery,coslist,training.btnresponse,training.button,
                                                                        training.image,training.link,training.video,training.pdf,training.response_type,training.UniqueId)
       confidence = max(coslist)
       logger.info("query - {} -Response Successful \n".format(query))
      
       

       btn = button.split(",")
       img=image.split(",")
       lnk=link.split(",")
       vid=video.split(",")
       pd=pdf.split(",")



      
       return prepare_answer(status_code, response_type, confidence,flow_type,UniqueId,"", [],
                             resp_data,"",btn,img,lnk,vid,pd)
            


if __name__ == "__main__":
    print(wrapper("AMD", "","", "",""))