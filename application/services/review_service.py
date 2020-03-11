from json import loads, load
import torch
import torchtext
from torchtext import data, datasets
from torchtext.vocab import GloVe
from janome.tokenizer import Tokenizer
from functools import reduce
from pprint import pprint
import sys

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
    sentences = text.split('\n')
    return sentences


j_t = Tokenizer()
def tokenize(sentence):
    print(sentence)
    return [tok for tok in j_t.tokenize(sentence, wakati=True)]


def load_json_data(json):
    f = open(json, 'r')
    reviews = load(f)
    for review in reviews:
        sentences = [cleaning(content['text']) for content in review.values()]
        sentences = flatten(sentences)
        print(sentences)
        


if __name__ == '__main__':
    load_json_data('dump.json')
