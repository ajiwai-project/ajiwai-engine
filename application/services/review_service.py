import torch
import torchtext
from torchtext import data, datasets
import numpy as np
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
from pprint import pprint

from model.model import Model
from model.dict import Dict
from infrastructure.dao.review_dao import ReviewDao


class ReviewService:

    def __init__(self):
        self.dict = Dict()
        self.dict.make('model/assets/output.csv')
        self.review_dao = ReviewDao()

    def train(self):
        reviews = self.dict.init()
        pprint(reviews)

