from json import load
import argparse
import pandas as pd

import sys

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


if __name__ == '__main__':
    args = parse_arguments()
    reviews_json = load_and_cleaning(args.f)
    reviews_df = json_to_data_frame(reviews_json)
    reviews_df = delete_symbols(reviews_df)

    reviews_df.to_csv(args.o, header=False, index=False)
