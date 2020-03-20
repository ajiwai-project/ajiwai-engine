import torch
import torchtext
from torchtext import data, datasets
from transformers import BertJapaneseTokenizer, BertForSequenceClassification



class BrandService:
    
    def __init__(self):
        pass

    def _create_stopwords(self, file_path):
        stop_words = []
        for w in open(file_path, "r"):
            w = w.replace('\n','')
            if len(w) > 0:
                stop_words.append(w)
        return stop_words    


    def predict(self, text):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        stop_words = _create_stopwords('model/assets/stop_words.txt')

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

        tokenized_text = tokenizer.tokenize(text)
        indexed_text = [TEXT.vocab.stoi[x] for x in tokenized_text]
        tensor_text = torch.tensor([indexed_text]).to(device)

        model = BertForSequenceClassification.from_pretrained(
            'model/NICT_BERT-base_JapaneseWikipedia_100K', num_labels=len(LABEL.vocab)).to(device)
        model.load_state_dict(torch.load('model/params/model_20200320151030.pth'))
        model.eval()
        outputs = model(tensor_text)
        print(outputs[0])
        print(torch.max(outputs[0], 1))
        print(LABEL.vocab.itos)
