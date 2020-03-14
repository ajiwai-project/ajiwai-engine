from json import loads, load
import argparse
import torch
import torchtext
from torchtext import data, datasets
from torchtext.vocab import GloVe
from janome.tokenizer import Tokenizer
import pandas as pd
from functools import reduce

from pprint import pprint
import sys


def parse_arguments():
    p = argparse.ArgumentParser(description='Hyperparams')
    p.add_argument('-f', type=str, default='assets/dump.json',
                   help='name of json file')
    p.add_argument('-o', type=str, default='assets/output.csv',
                   help='name of output file')
    return p.parse_args()

def flatten(list):
    return reduce(lambda a, b: a + b, list)

def cleaning(text):
    text = text.replace('\r', '')
    text = text.replace('\u3000', '')
    text = text.replace('‼️', '').replace('❗', '').replace('❓️', '').replace('♨️', '').replace('✨', '')
    text = text.replace('(', '').replace(')', '')
    text = text.replace('^', '').replace('*', '').replace('_', '').replace('▽', '')
    text = text.replace('o', '').replace('○', '').replace('■', '').replace('-', '')
    text = text.replace('´', '').replace('`', '').replace('◒', '').replace('~', '')
    text = text.replace('✧', '').replace('•́', '').replace('•̀', '').replace('∀', '')
    text = text.replace('!', '').replace('•́', '').replace('•̀', '').replace('∀', '')
    text = text.replace(' ', '')
    return text


j_t = Tokenizer()
def tokenizer(sentence):
    return [tok for tok in j_t.tokenize(sentence, wakati=True)]

def json_to_data_frame(json):
    data_frame = []
    for review in json:
        for value in review.values():
            raw_sentences = value['text']
            sentences = raw_sentences.split('\n')
            sentences = [sentence.split('。') for sentence in sentences]
            sentences = flatten(sentences)
            for sentence in sentences:
                data_frame.append([sentence, value['brand_id']])
    data_frame = [data for data in data_frame if len(data[0]) != 0]
    df = pd.DataFrame(data_frame, columns=['review', 'brand_id'])
    return df

def load_and_cleaning(json):
    f = open(json, 'r')
    reviews = load(f)
    for idx, review in enumerate(reviews):
        try:
            item = [item for item in review.items()]
            review_id = item[0][0]
            review_obj = item[0][1]
            reviews[idx][review_id]['text'] = cleaning(review_obj['text'])
        except KeyError:
            print('error')
            sys.exit()

    return reviews


if __name__ == '__main__':
    args = parse_arguments()
    reviews_json = load_and_cleaning(args.f)
    reviews_df = json_to_data_frame(reviews_json)
    reviews_df.to_csv(args.o)
