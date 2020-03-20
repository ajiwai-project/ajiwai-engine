import torch
import torchtext
from torchtext import data, datasets
from torchtext.vocab import GloVe
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
from tqdm import tqdm
import sys

from stop_words import create_stopwords

if __name__ == "__main__":
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


    text = sys.argv[1]
    tokenized_text = tokenizer.tokenize(text)
    indexed_text = [TEXT.vocab.stoi[x] for x in tokenized_text]
    tensor_text = torch.tensor([indexed_text]).to(device)

    model = BertForSequenceClassification.from_pretrained(
        'NICT_BERT-base_JapaneseWikipedia_100K', num_labels=len(LABEL.vocab)).to(device)
    model.load_state_dict(torch.load('params/model_20200320151030.pth'))
    model.eval()
    outputs = model(tensor_text)
    print(outputs[0])
    print(torch.max(outputs[0], 1))
    print(LABEL.vocab.itos)
