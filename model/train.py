import torch
import torch.nn as nn
import torch.optim as optim
import torchtext
from torchtext import data, datasets
from torchtext.vocab import GloVe
from transformers import BertJapaneseTokenizer, BertForSequenceClassification

from stop_words import create_stopwords
from pprint import pprint

batch_size = 32

if __name__ == '__main__':
    stop_words = create_stopwords('assets/stop_words.txt')
    tokenizer = BertJapaneseTokenizer.from_pretrained(
        'bert-base-japanese-whole-word-masking')

    TEXT = data.Field(
        sequential=True, tokenize=tokenizer.tokenize, stop_words=stop_words)
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
    print(len(LABEL.vocab))
    batch = next(iter(train_iter))
    model = BertForSequenceClassification.from_pretrained(
        'NICT_BERT-base_JapaneseWikipedia_100K', num_labels=len(LABEL.vocab))

    optimizer = optim.Adam([
        {'params': model.bert.encoder.layer[-1].parameters(), 'lr': 5e-5},
        {'params': model.classifier.parameters(), 'lr': 5e-5}
    ], betas=(0.9, 0.999))
    criterion = nn.CrossEntropyLoss()

    optimizer.zero_grad()

    model.train()
    loss, logit = model(input_ids=batch.Text, labels=batch.Label)
    print(loss, logit)
