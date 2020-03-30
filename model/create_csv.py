from json import load
import argparse
import pandas as pd
import sys
import torchtext
from torchtext.data import Field, Dataset, Example, BucketIterator
from transformers import BertJapaneseTokenizer


def parse_arguments():
    p = argparse.ArgumentParser(description='Hyperparams')
    p.add_argument('-f', type=str, default='assets/dump.json',
                   help='name of json file')
    p.add_argument('-o', type=str, default='assets/output.csv',
                   help='name of output file')
    return p.parse_args()


def json_to_data_frame(json):
    data_frame = []
    for review in json:
        for value in review.values():
            raw_sentences = value['text']
            sentences = raw_sentences.replace('\r\n', '')
            data_frame.append([sentences, value['brand_id']])
    data_frame = [data for data in data_frame if len(data[0]) != 0]
    df = pd.DataFrame(data_frame, columns=['review', 'brand_id'])
    return df


def load_and_cleaning(json):
    f = open(json, 'r')
    reviews = load(f)
    for idx, review in enumerate(reviews):
        try:
            item = [item for item in review.items()]
            review_id = item[0][0]
            review_obj = item[0][1]
            reviews[idx][review_id]['text'] = review_obj['text']
        except KeyError:
            print('error')
            sys.exit()
    return reviews


def delete_symbols(df):
    df['review'] = df['review'].str.replace('\d+年', '', regex=True)
    df['review'] = df['review'].str.replace('\d+月', '', regex=True)
    df['review'] = df['review'].str.replace('\d+日', '', regex=True)
    df['review'] = df['review'].str.replace('\d+', '0', regex=True)
    for symbol in open('assets/stop_symbols.txt', 'r'):
        symbol = symbol.replace('\n', '')
        df['review'] = df['review'].str.replace(symbol, '')
    return df


class DataFrameDataset(Dataset):
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


class SeriesExample(Example):
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


if __name__ == '__main__':
    args = parse_arguments()
    reviews_json = load_and_cleaning(args.f)
    reviews_df = json_to_data_frame(reviews_json)
    reviews_df = delete_symbols(reviews_df)

    tokenizer = BertJapaneseTokenizer.from_pretrained('bert-base-japanese-whole-word-masking')

    TEXT = Field(sequential=True, batch_first=True, tokenize=tokenizer.tokenize)
    LABEL = Field(sequential=False)

    train_ds = DataFrameDataset(reviews_df, fields={'review': TEXT, 'brand_id': LABEL})

    TEXT.build_vocab(train_ds)
    LABEL.build_vocab(train_ds)

    train_iter = BucketIterator(
        dataset=train_ds,
        batch_size=4,
        repeat=False
    )

    for batch in train_iter:
        print(batch.review)
    # reviews_df.to_csv(args.o, header=False, index=False)
