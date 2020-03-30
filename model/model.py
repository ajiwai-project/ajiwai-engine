import torch
import torch.nn as nn
import torch.optim as optim
import torchtext
from torchtext import data
from transformers import BertForSequenceClassification
from datetime import datetime
from tqdm import tqdm

from model.stop_words import create_stopwords
from model.dict import Dict


class Model:
    def __init__(self, num_labels):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.num_labels = num_labels
        self.model = BertForSequenceClassification.from_pretrained('model/NICT_BERT-base_JapaneseWikipedia_100K', num_labels=num_labels).to(self.device)
        self.optimizer = optim.Adam([
            {'params': self.model.bert.encoder.layer[-1].parameters(), 'lr': 5e-5},
            {'params': self.model.classifier.parameters(), 'lr': 5e-5}
        ], betas=(0.9, 0.999))
        self.criterion = nn.CrossEntropyLoss()

    def predict(self, text, dict):
        tokenized_text = dict.tokenizer.tokenize(text)
        indexed_text = [dict.TEXT.vocab.stoi[w] for w in tokenized_text]
        tensor_text = torch.tensor([indexed_text]).to(self.device)

        self.model.load_state_dict(torch.load('model/params/model_20200320151030.pth'))
        self.model.eval()
        outputs = self.model(tensor_text)
        return outputs


    def train(self, train_iter, epoch_num=10):
        self.model.train()

        for epoch in tqdm(range(epoch_num)):
            epoch_loss = 0.0
            for batch in train_iter:
                inputs, labels = batch.Text, batch.Label
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                self.optimizer.zero_grad()

                loss, logit = self.model(input_ids=inputs, labels=labels)
                loss.backward()
                epoch_loss += loss.data
                self.optimizer.step()

            torch.save(self.model.state_dict(), 'model/params/model_{}.pth'.format(datetime.now().strftime('%Y%m%d%H%M%S')))
            print('epoch' + str(epoch+1) + ' loss: ' + str(epoch_loss))
      

if __name__ == "__main__":
    batch_size = 4
    stop_words = create_stopwords('model/assets/stop_words.txt')

    dict = Dict()
    dict.init()

    model = Model(len(dict.LABEL.vocab))
    model.predict('辛口でフルーティ', dict)