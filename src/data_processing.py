import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import spacy
from time import time
import matplotlib.pyplot as plt


nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
import streamlit as st

annotated_df = pd.read_csv('./annotated_summaries_df.csv', encoding='iso-8859-1')

# print(annotated_df)
# print(annotated_df['chat_gpt_summary'].head(5))
# print(annotated_df['article'].head(5))
# print(annotated_df['source'].head(5))
# print(annotated_df['date'].head(5))
# print(annotated_df['headline'].head(5))
# print(annotated_df['url'].head(5))

# Transform text into lower case

# annotated_df['chat_gpt_summary'] = annotated_df['chat_gpt_summary'].fillna('').astype(str)
annotated_df = annotated_df.dropna(subset=['chat_gpt_summary'])
annotated_df['chat_gpt_summary_clean'] = annotated_df['chat_gpt_summary'].apply(
    lambda x: " ".join(x.lower() for x in x.split()))

# annotated_df['article'] = annotated_df['article'].fillna('').astype(str)
annotated_df = annotated_df.dropna(subset=['article'])
annotated_df['article_clean'] = annotated_df['article'].apply(lambda x: " ".join(x.lower() for x in x.split()))

# annotated_df['headline'] = annotated_df['headline'].fillna('').astype(str)
annotated_df = annotated_df.dropna(subset=['headline'])
annotated_df['headline_clean'] = annotated_df['headline'].apply(lambda x: " ".join(x.lower() for x in x.split()))


# Transform date to YYYY-MM-dd
# annotated_df['date'] = pd.to_datetime(annotated_df['date'], format='%d/%m/%Y')
# annotated_df['date'] = annotated_df['date'].dt.strftime("%Y-%m-%d")
# annotated_df['date'] = pd.to_datetime(annotated_df['date'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce')
# annotated_df['date'] = pd.to_datetime(annotated_df['date'], infer_datetime_format=True, errors='coerce')
# annotated_df['date'] = annotated_df['date'].dt.strftime('%Y-%m-%d')


def parse_date(date_string):
    try:
        return pd.to_datetime(date_string, format='%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        return pd.to_datetime(date_string, format='%d/%m/%Y')


# print(annotated_df['date'].apply(lambda x: type(x)).head(10))
# annotated_df['date'] = annotated_df['date'].apply(parse_date)
# annotated_df['date'] = annotated_df['date'].dt.strftime('%Y-%m-%d')

# Remove puntuation
# annotated_df['chat_gpt_summary_clean'] = annotated_df['chat_gpt_summary_clean'].str.replace('[^\w\s]', '')


# Remove non-alphabetic characters (Data Cleaning)

def text_strip(column):
    for row in column:
        row = re.sub(r"(\t)", " ", str(row)).lower()
        row = re.sub(r"(\r)", " ", str(row)).lower()
        row = re.sub(r"(\n)", " ", str(row)).lower()

        # Remove _ if it occurs more than one time consecutively
        row = re.sub(r"(__+)", " ", str(row)).lower()

        # Remove - if it occurs more than one time consecutively
        row = re.sub(r"(--+)", " ", str(row)).lower()

        # Remove ~ if it occurs more than one time consecutively
        row = re.sub(r"(~~+)", " ", str(row)).lower()

        # Remove + if it occurs more than one time consecutively
        row = re.sub(r"(\+\++)", " ", str(row)).lower()

        # Remove . if it occurs more than one time consecutively
        row = re.sub(r"(\.\.+)", " ", str(row)).lower()

        # Remove the characters - <>()|&©ø"',;?~*!
        row = re.sub(r"[<>()|&©ø\[\]'\",;?~*!]", " ", str(row)).lower()

        # Remove mailto:
        row = re.sub(r"(mailto:)", " ", str(row)).lower()

        # Remove \x9* in text
        row = re.sub(r"(\\x9\d)", " ", str(row)).lower()

        # Replace INC nums to INC_NUM
        row = re.sub(r"([iI][nN][cC]\d+)", "INC_NUM", str(row)).lower()

        # Replace CM# and CHG# to CM_NUM
        row = re.sub(r"([cC][mM]\d+)|([cC][hH][gG]\d+)", "CM_NUM", str(row)).lower()

        # Remove punctuations at the end of a word
        row = re.sub(r"(\.\s+)", " ", str(row)).lower()
        row = re.sub(r"(-\s+)", " ", str(row)).lower()
        row = re.sub(r"(:\s+)", " ", str(row)).lower()

        # Replace any url to only the domain name
        try:
            url = re.search(r"((https*:\/*)([^\/\s]+))(.[^\s]+)", str(row))
            repl_url = url.group(3)
            row = re.sub(r"((https*:\/*)([^\/\s]+))(.[^\s]+)", repl_url, str(row))
        except:
            pass

            # Remove multiple spaces
        row = re.sub(r"(\s+)", " ", str(row)).lower()

        # Remove the single character hanging between any two spaces
        row = re.sub(r"(\s+.\s+)", " ", str(row)).lower()

        yield row


annotated_df['chat_gpt_summary_clean'] = list(text_strip(annotated_df['chat_gpt_summary_clean']))
annotated_df['article_clean'] = list(text_strip(annotated_df['article_clean']))
annotated_df['headline_clean'] = list(text_strip(annotated_df['headline_clean']))

# Load data as batches

nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])

# Process text as batches and yield Doc objects in order
annotated_df['headline_clean'] = [str(doc) for doc in nlp.pipe(annotated_df['headline_clean'], batch_size=5000)]
annotated_df['article_clean'] = [str(doc) for doc in nlp.pipe(annotated_df['article_clean'], batch_size=5000)]
annotated_df['chat_gpt_summary_clean'] = ['_START_ '+ str(doc) + ' _END_' for doc in nlp.pipe(annotated_df['chat_gpt_summary_clean'], batch_size=5000)]

# Determine maximum sequence lenghts

article_count = []
summary_count = []

for sent in annotated_df['article_clean']:
    article_count.append(len(sent.split()))

for sent in annotated_df['chat_gpt_summary_clean']:
    summary_count.append(len(sent.split()))

graph_df = pd.DataFrame()

graph_df['text'] = article_count
graph_df['summary'] = summary_count

graph_df.hist(bins=10)
plt.show()

# Remove stopwords
stop = stopwords.words('english')
stop.extend(['abcdefghijk'])
annotated_df['chat_gpt_summary_clean'] = annotated_df['chat_gpt_summary_clean'].apply(
    lambda x: " ".join(x for x in x.split() if x not in stop))
annotated_df['article_clean'] = annotated_df['article_clean'].apply(
    lambda x: " ".join(x for x in x.split() if x not in stop))
annotated_df['headline_clean'] = annotated_df['headline_clean'].apply(
    lambda x: " ".join(x for x in x.split() if x not in stop))

# Tokenization
annotated_df['chat_gpt_summary_wordtok'] = annotated_df['chat_gpt_summary'].apply(word_tokenize)
annotated_df['chat_gpt_summary_clean_wordtok'] = annotated_df['chat_gpt_summary_clean'].apply(word_tokenize)
annotated_df['article_wordtok'] = annotated_df['article'].apply(word_tokenize)
annotated_df['article_clean_wordtok'] = annotated_df['article_clean'].apply(word_tokenize)
annotated_df['headline_wordtok'] = annotated_df['headline'].apply(word_tokenize)
annotated_df['headline_clean_wordtok'] = annotated_df['headline_clean'].apply(word_tokenize)

annotated_df['chat_gpt_summary_sentok'] = annotated_df['chat_gpt_summary'].apply(word_tokenize)
annotated_df['chat_gpt_summary_clean_sentok'] = annotated_df['chat_gpt_summary_clean'].apply(word_tokenize)
annotated_df['article_sentok'] = annotated_df['article'].apply(word_tokenize)
annotated_df['article_clean_sentok'] = annotated_df['article_clean'].apply(word_tokenize)
annotated_df['headline_sentok'] = annotated_df['headline'].apply(word_tokenize)
annotated_df['headline_clean_sentok'] = annotated_df['headline_clean'].apply(word_tokenize)

annotated_df.to_csv('./output_test7.csv')
