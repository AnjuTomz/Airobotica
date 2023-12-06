import fire
import config as cfg
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
import json, os, subprocess, sys
import io
import re


# python rasa_trainer.py --train=True --model=RealEstate
# python rasa_trainer.py --train=False --model=RealEstate

def model_engine(train, model):
    config = cfg.RASA_CONFIG_SPACY
    print(config)

    if train:
        print "Building rasa model"
        print "********************\n"

        with io.open(cfg.RASA_JSON_PATH + model + '.json', encoding="utf-8-sig") as f:
            data = json.loads(f.read())
        common = data['rasa_nlu_data'].get("common_examples", list())
        for i in range(len(common)):
            # common[i]['text']= ' '.join(dp.data_prep(common[i]['text'], "Tumi", remove_stopwords=False))
            common[i]['text'] = re.sub('[^a-zA-Z0-9.]', ' ', common[i]['text'].lower())
        data['rasa_nlu_data'].update({"common_examples": common})
        with open(cfg.RASA_JSON_PATH + model + '.json', 'wb') as f:
            json.dump(data, f)
        print "done preparing data for rasa"
        load_traning_data_path = cfg.RASA_JSON_PATH + model + '.json'
        model_path = cfg.MODEL_PATH + model

        training_data = load_data(load_traning_data_path)
        # print (training_data)
        trainer = Trainer(RasaNLUConfig(config))
        trainer.train(training_data)

        if not os.path.exists(model_path):
            os.makedirs(model_path)

        path_model = trainer.persist(path=model_path)  # , create_unique_subfolder=False)

        with open(config, 'rb') as f:
            configfile = json.load(f)

        configfile['server_model_dirs'][
            model] = path_model  # Modify the config.spacy.json based on created model with timestamp

        with open(config, 'wb') as f:
            json.dump(configfile, f)
    subprocess.call(["python", "-m", "rasa_nlu.server", "--port", "5000", "-c", "./rasa_nlu_module/config_spacy.json"])


if __name__ == "__main__":
    # tf_model_engine()
    fire.Fire(model_engine)
