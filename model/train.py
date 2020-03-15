import torch
import torchtext
from torchtext import data, datasets
from torchtext.vocab import GloVe
from janome.tokenizer import Tokenizer
from pprint import pprint
import sys

from stop_words import create_stopwords

j_t = Tokenizer()
batch_size = 5


def tokenizer(text):
    return [tok.base_form for tok in j_t.tokenize(text) if tok.part_of_speech not in ['助詞', '記号']]


if __name__ == '__main__':
    stop_words = create_stopwords('assets/stop_words.txt')
    TEXT = data.Field(sequential=True, tokenize=tokenizer,
                      stop_words=stop_words)
    LABEL = data.Field(sequential=False)

    train = data.TabularDataset(
        path='assets/output.csv',
        format='csv',
        fields=[('Text', TEXT), ('Label', LABEL)]
    )

    TEXT.build_vocab(train)
    LABEL.build_vocab(train)

    train_iter = data.BucketIterator(
        dataset=train,
        batch_size=batch_size,
        repeat=False
    )

    # TODO
    pprint(TEXT.vocab.itos)
