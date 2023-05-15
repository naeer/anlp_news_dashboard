import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from collections import Counter
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')


annotated_df = pd.read_csv('./annotated_summaries_df_2.csv', encoding='iso-8859-1')
annotated_df.to_csv('my_data_utf8.csv', index=False, encoding='utf-8')
annotated_df = pd.read_csv('./my_data_utf8.csv', encoding='utf-8')
annotated_df.dropna(subset=['chat_gpt_summary'], inplace=True)
annotated_df = annotated_df.drop_duplicates(subset='url')
annotated_df = annotated_df[['url', 'chat_gpt_summary']]

print(annotated_df)

prep_df = pd.read_csv('./data_prep_app.csv', encoding='utf-8')
prep_df.dropna(subset=['article'], inplace=True)
prep_df = prep_df.drop_duplicates(subset='url')

print(prep_df)

annotated_df = prep_df.merge(annotated_df[['url', 'chat_gpt_summary']], on='url', how='inner')

print(annotated_df)

# Transform text into lower case

annotated_df = annotated_df.dropna(subset=['chat_gpt_summary'])
annotated_df['chat_gpt_summary_clean'] = annotated_df['chat_gpt_summary'].apply(
    lambda x: " ".join(x.lower() for x in x.split()))

# Drop rows with empty articles
annotated_df = annotated_df.dropna(subset=['article'])
annotated_df['article_clean'] = annotated_df['article'].apply(lambda x: " ".join(x.lower() for x in x.split()))

# Drop rows with missing summaries
annotated_df = annotated_df.dropna(subset=['headline'])
annotated_df['headline_clean'] = annotated_df['headline'].apply(lambda x: " ".join(x.lower() for x in x.split()))


# Function to Remove non-alphabetic characters (Data Cleaning) taken from:
# https://blog.paperspace.com/introduction-to-seq2seq-models/ and edited accordingly.
def text_strip(column):
    for row in column:
        row = re.sub(r"(\t)", " ", str(row)).lower()
        row = re.sub(r"(\r)", " ", str(row)).lower()
        row = re.sub(r"(\n)", " ", str(row)).lower()
        row = re.sub(r'[^a-zA-Z0-9\s]', '', str(row)).lower()

        # Remove consecutive _
        row = re.sub(r"(__+)", " ", str(row)).lower()

        # Remove consecutive -
        row = re.sub(r"(--+)", " ", str(row)).lower()

        # Remove consecutive ~
        row = re.sub(r"(~~+)", " ", str(row)).lower()

        # Remove consecutive +
        row = re.sub(r"(\+\++)", " ", str(row)).lower()

        # Remove consecutive .
        row = re.sub(r"(\.\.+)", " ", str(row)).lower()

        # Remove - <>()|&©ø"',;?~*!
        row = re.sub(r"[<>()|&©ø\[\]\'\",;?~*!]", " ", str(row)).lower()

        # Remove mailto:
        row = re.sub(r"(mailto:)", " ", str(row)).lower()

        # Remove \x9* in text
        row = re.sub(r"(\\x9\d)", " ", str(row)).lower()

        # Replace INC nums to INC_NUM
        row = re.sub(r"([iI][nN][cC]\d+)", "INC_NUM", str(row)).lower()

        # Replace CM# and CHG# to CM_NUM
        row = re.sub(r"([cC][mM]\d+)|([cC][hH][gG]\d+)", "CM_NUM", str(row)).lower()

        # Remove punctuations
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

# article_count = []
# summary_count = []

# for sent in annotated_df['article_clean']:
   # article_count.append(len(sent.split()))

# for sent in annotated_df['chat_gpt_summary_clean']:
   # summary_count.append(len(sent.split()))

# graph_df = pd.DataFrame()

# graph_df['text'] = article_count
# graph_df['summary'] = summary_count

# graph_df.hist(bins=10)
# plt.show()

# Remove stopwords
stop = stopwords.words('english')
stop.extend(['one', 'two', 'three', 'four', 'five', 'said'])
annotated_df['chat_gpt_summary_clean'] = annotated_df['chat_gpt_summary_clean'].apply(
    lambda x: " ".join(x for x in x.split() if x not in stop))
annotated_df['article_clean'] = annotated_df['article_clean'].apply(
    lambda x: " ".join(x for x in x.split() if x not in stop))
annotated_df['headline_clean'] = annotated_df['headline_clean'].apply(
    lambda x: " ".join(x for x in x.split() if x not in stop))

# Tokenization by word and sentence level to summary, article and headlines (cleaned and pre-cleaned)
annotated_df['chat_gpt_summary_wordtok'] = annotated_df['chat_gpt_summary'].apply(word_tokenize)
annotated_df['chat_gpt_summary_clean_wordtok'] = annotated_df['chat_gpt_summary_clean'].apply(word_tokenize)
annotated_df['article_wordtok'] = annotated_df['article'].apply(word_tokenize)
annotated_df['article_clean_wordtok'] = annotated_df['article_clean'].apply(word_tokenize)
annotated_df['headline_wordtok'] = annotated_df['headline'].apply(word_tokenize)
annotated_df['headline_clean_wordtok'] = annotated_df['headline_clean'].apply(word_tokenize)

annotated_df['chat_gpt_summary_sentok'] = annotated_df['chat_gpt_summary'].apply(sent_tokenize)
annotated_df['chat_gpt_summary_clean_sentok'] = annotated_df['chat_gpt_summary_clean'].apply(sent_tokenize)
annotated_df['article_sentok'] = annotated_df['article'].apply(sent_tokenize)
annotated_df['article_clean_sentok'] = annotated_df['article_clean'].apply(sent_tokenize)
annotated_df['headline_sentok'] = annotated_df['headline'].apply(sent_tokenize)
annotated_df['headline_clean_sentok'] = annotated_df['headline_clean'].apply(sent_tokenize)

# Sentiment analysis

sia = SentimentIntensityAnalyzer()


def get_sentence_sentiment_score(sentence):
    return sia.polarity_scores(sentence)['compound']


def get_sentiment_label(score):
    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    else:
        return 'neutral'


# Get sentiment score per sentence
sentence_scores = annotated_df['article_clean_sentok'].apply(lambda x: [get_sentence_sentiment_score(sentence) for sentence in x])

# Get average sentiment result per article and label
article_scores = sentence_scores.apply(lambda x: sum(x)/len(x))
annotated_df['article_sentiment_score'] = article_scores
annotated_df['article_sentiment_label'] = annotated_df['article_sentiment_score'].apply(get_sentiment_label)

print(annotated_df[['article', 'article_sentiment_score', 'article_sentiment_label']])

# Extract Named Entities in the article

nlp = spacy.load('en_core_web_sm')


def extract_named_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG']:
            entities.append(ent.text)
    return entities


annotated_df['named_entities'] = annotated_df['article'].apply(extract_named_entities)
print(annotated_df[['article', 'named_entities']])

# Get the top 5 entities by occurrence
def get_top_entities(entities_list):
    counter = Counter(entities_list)
    top_entities = counter.most_common(5)
    return [entity for entity, count in top_entities]


annotated_df['top_entities'] = annotated_df['named_entities'].apply(get_top_entities)
print(annotated_df[['article', 'top_entities']])

# Include count of occurrences.
def get_top_entities_with_count(entities_list):
    counter = Counter(entities_list)
    top_entities = counter.most_common(5)
    return [(entity, count) for entity, count in top_entities]


annotated_df['top_entities_with_count'] = annotated_df['named_entities'].apply(get_top_entities_with_count)
print(annotated_df[['article', 'top_entities_with_count']])

# Get the most frequent words including count.
def extract_top_words_with_count(words, n=5):
    # Count the frequency of each word
    word_counts = Counter(words)
    # Get the most common words
    top_words = word_counts.most_common(n)
    # Return a list of tuples with the word and its count
    return [(word, count) for word, count in top_words]


annotated_df['top_words'] = annotated_df['article_clean_wordtok'].apply(extract_top_words_with_count)
print(annotated_df[['article', 'top_words']])

annotated_df.to_csv('./data_app_st.csv', encoding='utf-8')
