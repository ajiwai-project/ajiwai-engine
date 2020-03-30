import torch
import torchtext
from torchtext import data, datasets
import numpy as np
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
from pprint import pprint

from model.model import Model
from model.dict import Dict
from infrastructure.repositories.review_repository import ReviewRepository


class ReviewService:

    def __init__(self):
        self.dict = Dict()
        self.dict.init()
        self.model = Model(len(self.dict.LABEL.vocab))
        self.review_repository = ReviewRepository()

    def get_reviews(self):
        return self.review_repository.find_all()

    def train(self):
        pprint(reviews)
