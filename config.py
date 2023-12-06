# -*- coding: utf-8 -*-

#ROOT = "/home/ubuntu/jessi/RealEstate/"

ROOT = "F:\\amdbot"

MODEL_PATH = ROOT + "Model/"


ACTUAL_CSV_FILE = ROOT+ "/Data/RealEstatenew.csv"

PREPARED_CSV_PATH= ROOT+ "/Data/Prepared_RealEstate_01new.csv"

INPUT_PATH = ROOT + "Input/"

DUMP_PATH =  ROOT + "dump/"

RASA_JSON_PATH = ROOT + "Data/Rasa/"

RASA_CSV = ROOT + '/Data/Rasa/realestate_intent.csv'

RASA_PARSER_URL = 'http://localhost:8081/parse?q='

RASA_CONFIG_SPACY = ROOT + "/rasa_nlu_module/config_spacy.json"


USER_DATA_PATH = ROOT + '/users_data/'

CSV_DATA_FILE_PATH = ROOT + '/Data/Tumi_filtered.csv'

FAQ_PATH = ROOT + "/Data/FAQs.csv"

FAQVOCAB_PATH = ROOT + "/Trainer/faqdata/spellcheck_model/faqvocab.txt"

FAQ_MATRIX = ROOT + "/Trainer/faqdata/tfidf_model/sparse_matrix.npy"

VOCAB_PATH = ROOT + "/Trainer/spellcheck_model/big.txt"

SMALLTALK_PATH = ROOT + "/Data/smalltalk.csv"

SMALLVOCAB_PATH = ROOT + "/Trainer/smalltalk/spellcheck_model/smalltalkvocab.txt"

SMALLTALK_MATRIX = ROOT + "/Trainer/smalltalk/tfidf_model/sparse_matrix.npy"

EXPLOREVOCAB_PATH = ROOT + "/Trainer/explore/spellcheck_model/explorevocab.txt"

UIFLOW_PATH = ROOT + "/Data/datas.csv"

UIFLOW_MATRIX = ROOT + "/Trainer/uiflow/tfidf_model/sparse_matrix.npy"
