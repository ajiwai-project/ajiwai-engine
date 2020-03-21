import torch
import torch.nn as nn
import torch.optim as optim
import torchtext
from torchtext import data
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
from datetime import datetime
from tqdm import tqdm

from stop_words import create_stopwords


tokenizer = BertJapaneseTokenizer.from_pretrained('bert-base-japanese-whole-word-masking')    

class Model:
    def __init__(self, num_labels):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.num_labels = num_labels
        self.model = BertForSequenceClassification.from_pretrained('NICT_BERT-base_JapaneseWikipedia_100K', num_labels=num_labels).to(self.device)
        self.optimizer = optim.Adam([
            {'params': self.model.bert.encoder.layer[-1].parameters(), 'lr': 5e-5},
            {'params': self.model.classifier.parameters(), 'lr': 5e-5}
        ], betas=(0.9, 0.999))
        self.criterion = nn.CrossEntropyLoss()

    def predict(self, text):
        tokenized_text = tokenizer.tokenize(text)
        indexed_text = [TEXT.vocab.stoi[w] for w in tokenized_text]
        tensor_text = torch.tensor([indexed_text]).to(self.device)

        self.model.load_state_dict(torch.load('params/model_20200320151030.pth'))
        self.model.eval()
        outputs = self.model(tensor_text)
        print(outputs[0])
        print(torch.max(outputs[0], 1))
        print(LABEL.vocab.itos)


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

            torch.save(self.model.state_dict(), './params/model_{}.pth'.format(datetime.now().strftime('%Y%m%d%H%M%S')))
            print('epoch' + str(epoch+1) + ' loss: ' + str(epoch_loss))
      
if __name__ == "__main__":
    batch_size = 4
    stop_words = create_stopwords('assets/stop_words.txt')

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

    model = Model(len(LABEL.vocab))
    model.predict('私は獺祭が好きです。')