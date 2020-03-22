import torchtext
from torchtext import data
from transformers import BertJapaneseTokenizer

from model.stop_words import create_stopwords


class Dict:
    def __init__(self):
        stop_words = create_stopwords('model/assets/stop_words.txt')
        self.tokenizer = BertJapaneseTokenizer.from_pretrained('bert-base-japanese-whole-word-masking')
        self.TEXT = data.Field(
            sequential=True,
            tokenize=self.tokenizer.tokenize,
            stop_words=stop_words,
            batch_first=True)    
        self.LABEL = data.Field(sequential=False)

    def make(self, input_file='assets/output.csv'):
        train = data.TabularDataset(
            path=input_file,
            format='csv',
            fields=[('Text', self.TEXT), ('Label', self.LABEL)]
        )

        self.TEXT.build_vocab(train)
        self.LABEL.build_vocab(train)
        