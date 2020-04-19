import torchtext
from torchtext import data
from transformers import BertJapaneseTokenizer
import pandas as pd

from model.stop_words import create_stopwords
from infrastructure.repositories.review_repository import ReviewRepository


class Dict:
    def __init__(self):
        stop_words = create_stopwords('model/assets/stop_words.txt')
        self.tokenizer = BertJapaneseTokenizer.from_pretrained(
            'bert-base-japanese-whole-word-masking')
        self.TEXT = data.Field(
            sequential=True,
            tokenize=self.tokenizer.tokenize,
            stop_words=stop_words,
            batch_first=True)
        self.LABEL = data.Field(sequential=False)
        self.review_repository = ReviewRepository()

    def init(self):
        reviews = self.review_repository.find_all()
        reviews_df = [[review[1]['brand_id'], review[1]['text']] for review in reviews]
        reviews_df = pd.DataFrame(reviews_df, columns=['brand_id', 'review'])
        reviews_df = self.delete_symbols(reviews_df)

        tokenizer = BertJapaneseTokenizer.from_pretrained(
            'bert-base-japanese-whole-word-masking')
        TEXT = data.Field(sequential=True, batch_first=True, tokenize=tokenizer.tokenize)
        LABEL = data.Field(sequential=False)

        self.train_ds = DataFrameDataset(reviews_df, fields={'review': self.TEXT, 'brand_id': self.LABEL})

        self.TEXT.build_vocab(self.train_ds)
        self.LABEL.build_vocab(self.train_ds)
    
    def delete_symbols(self, df):
        df['review'] = df['review'].str.replace('\d+年', '', regex=True)
        df['review'] = df['review'].str.replace('\d+月', '', regex=True)
        df['review'] = df['review'].str.replace('\d+日', '', regex=True)
        df['review'] = df['review'].str.replace('\d+', '0', regex=True)
        for symbol in open('model/assets/stop_symbols.txt', 'r'):
            symbol = symbol.replace('\n', '')
            df['review'] = df['review'].str.replace(symbol, '')
        return df


    def get_train_ds(self):
        return self.train_ds


class DataFrameDataset(data.Dataset):
    """
    pandas DataFrameからtorchtextのdatasetつくるやつ
    https://stackoverflow.com/questions/52602071/dataframe-as-datasource-in-torchtext
    """

    def __init__(self, examples, fields, filter_pred=None):
        """
         Create a dataset from a pandas dataframe of examples and Fields
         Arguments:
             examples pd.DataFrame: DataFrame of examples
             fields {str: Field}: The Fields to use in this tuple. The
                 string is a field name, and the Field is the associated field.
             filter_pred (callable or None): use only exanples for which
                 filter_pred(example) is true, or use all examples if None.
                 Default is None
        """
        self.examples = examples.apply(
            SeriesExample.fromSeries, args=(fields,), axis=1).tolist()
        if filter_pred is not None:
            self.examples = filter(filter_pred, self.examples)
        self.fields = dict(fields)
        # Unpack field tuples
        for n, f in list(self.fields.items()):
            if isinstance(n, tuple):
                self.fields.update(zip(n, f))
                del self.fields[n]


class SeriesExample(data.Example):
    """Class to convert a pandas Series to an Example"""
    @classmethod
    def fromSeries(cls, data, fields):
        return cls.fromdict(data.to_dict(), fields)

    @classmethod
    def fromdict(cls, data, fields):
        ex = cls()

        for key, field in fields.items():
            if key not in data:
                raise ValueError("Specified key {} was not found in "
                                 "the input data".format(key))
            if field is not None:
                setattr(ex, key, field.preprocess(data[key]))
            else:
                setattr(ex, key, data[key])
        return ex
