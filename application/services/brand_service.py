import torch
import torchtext
from torchtext import data, datasets
import numpy as np
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
from pprint import pprint

from model.model import Model
from model.dict import Dict
from infrastructure.dao.firebase.brand_dao import BrandDao


class BrandService:

    def __init__(self):
        self.dict = Dict()
        self.dict.init()
        self.model = Model(len(self.dict.LABEL.vocab))
        self.brand_dao = BrandDao()

    def predict(self, text):
        outputs = self.model.predict(text, self.dict)
        outputs = outputs[0][0].cpu().detach().numpy().copy()

        outputs = [[idx, v] for idx, v, in enumerate(outputs)]
        outputs.sort(key=lambda o: o[1], reverse=True)
        outputs = [{
            'brand': self.brand_dao.find_by_brand_id(self.dict.LABEL.vocab.itos[output[0]]),
            'similarity': output[1].astype(np.float64)
        } for output in outputs]

        return outputs

