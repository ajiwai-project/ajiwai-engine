import torch
import torchtext
from torchtext import data, datasets
from transformers import BertJapaneseTokenizer, BertForSequenceClassification

from model.model import Model
from model.dict import Dict


class BrandService:
    

    def predict(self, text):
        """
            modelで予想
            idからブランドをget
            return
        """
        dict = Dict()
        dict.make('model/assets/output.csv')
        model = Model(len(dict.LABEL.vocab))
        model.predict(text, dict)


        


