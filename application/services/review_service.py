import torch
import torchtext
from torchtext import data, datasets
from torchtext.data import Field, Dataset, Example, BucketIterator
import numpy as np
import pandas as pd
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
from pprint import pprint

from model.model import Model
from model.dict import Dict
from infrastructure.repositories.review_repository import ReviewRepository


class ReviewService:

    def __init__(self):
        self.dict = Dict()
        self.review_repository = ReviewRepository()

    def get_reviews(self):
        return self.review_repository.find_all()

    def train(self):
        self.dict.init()
        train_ds = self.dict.get_train_ds()
        
        train_iter = BucketIterator(
            dataset=train_ds,
            batch_size=4,
            repeat=False
        )

        self.model = Model(len(self.dict.LABEL.vocab))
        self.model.train(train_iter)
        
        
    def delete_symbols(self, df):
        df['review'] = df['review'].str.replace('\d+年', '', regex=True)
        df['review'] = df['review'].str.replace('\d+月', '', regex=True)
        df['review'] = df['review'].str.replace('\d+日', '', regex=True)
        df['review'] = df['review'].str.replace('\d+', '0', regex=True)
        for symbol in open('model/assets/stop_symbols.txt', 'r'):
            symbol = symbol.replace('\n', '')
            df['review'] = df['review'].str.replace(symbol, '')
        return df