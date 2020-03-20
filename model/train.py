import torch
import torch.nn as nn
import torch.optim as optim
import torchtext
from torchtext import data, datasets
from torchtext.vocab import GloVe
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
from tqdm import tqdm
from datetime import datetime
from stop_words import create_stopwords
from pprint import pprint

batch_size = 8

if __name__ == '__main__':
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    stop_words = create_stopwords('assets/stop_words.txt')
    tokenizer = BertJapaneseTokenizer.from_pretrained(
        'bert-base-japanese-whole-word-masking')

    TEXT = data.Field(
        sequential=True,
        tokenize=tokenizer.tokenize,
        stop_words=stop_words,
        batch_first=True)
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

    model = BertForSequenceClassification.from_pretrained(
        'NICT_BERT-base_JapaneseWikipedia_100K', num_labels=len(LABEL.vocab)).to(device)
    optimizer = optim.Adam([
        {'params': model.bert.encoder.layer[-1].parameters(), 'lr': 5e-5},
        {'params': model.classifier.parameters(), 'lr': 5e-5}
    ], betas=(0.9, 0.999))
    criterion = nn.CrossEntropyLoss()

    for epoch in tqdm(range(20)):
        epoch_loss = 0.0
        for batch in train_iter:
            inputs, labels = batch.Text, batch.Label
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            loss, logit = model(input_ids=inputs, labels=labels)
            loss.backward()
            epoch_loss += loss.data
            optimizer.step()

        torch.save(model.state_dict(), './params/model_{}.pth'.format(datetime.now().strftime('%Y%m%d%H%M%S')))
        print('epoch' + str(epoch+1) + ' loss: ' + str(epoch_loss))
