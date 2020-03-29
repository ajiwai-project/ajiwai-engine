import torchtext
from torchtext import data
from transformers import BertJapaneseTokenizer
import pandas as pd

from model.stop_words import create_stopwords
from infrastructure.dao.brand_dao import BrandDao
from infrastructure.dao.review_dao import ReviewDao


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
        self.review_dao = ReviewDao()

    def init(self):
        review_docs = self.review_dao.find_all()
        reviews = [[doc.to_dict()['text'], doc.to_dict()['brand_id']]
                   for doc in review_docs]
        df = pd.DataFrame(reviews, columns=['review', 'brand_id'])

    def make(self, input_file='assets/output.csv'):
        train = data.TabularDataset(
            path=input_file,
            format='csv',
            fields=[('Text', self.TEXT), ('Label', self.LABEL)]
        )

        self.TEXT.build_vocab(train)
        self.LABEL.build_vocab(train)


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
