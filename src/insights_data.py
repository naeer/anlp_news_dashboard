import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re




df = pd.read_csv('./final_app_data.csv', encoding='iso-8859-1')
df.to_csv('my_data_3_utf8.csv', index=False, encoding='utf-8')
df = pd.read_csv('./my_data_3_utf8.csv', encoding='utf-8')


# Articles per keyword
article_counts = df.groupby('keyword')['keyword'].count().reset_index(name='count')
article_counts = article_counts.sort_values('count', ascending=False)
plt.figure(figsize=(10, 6))
plt.bar(article_counts['keyword'], article_counts['count'])
plt.xlabel('Keyword')
plt.ylabel('Number of Articles')
plt.title('Number of Articles per Keyword')
plt.xticks(rotation=90)
#plt.show()

# Histogram Number of words

plt.figure(figsize=(10, 6))
plt.hist(df['num_words'], bins=20, edgecolor='black')
plt.xlabel('Number of Words')
plt.ylabel('Frequency')
plt.title('Distribution of Number of Words in Articles')
#plt.show()

# Top entities

named_entities_string = ' '.join(df['named_entities'])
named_entities_list = re.findall(r'\b[A-Z][a-zA-Z]+\b', named_entities_string)
entity_counts = Counter(named_entities_list)
top_20_entities = entity_counts.most_common(20)
top_20_entities_list, top_20_counts = zip(*top_20_entities)
plt.figure(figsize=(10, 6))
plt.bar(top_20_entities_list, top_20_counts)
plt.xlabel('Named Entities')
plt.ylabel('Count')
plt.title('Top 20 Named Entities across Articles')
plt.xticks(rotation=90)
plt.show()

# Articles per sentiment
article_counts = df.groupby('article_sentiment_label')['article_sentiment_label'].count().reset_index(name='count')
article_counts = article_counts.sort_values('count', ascending=False)
plt.figure(figsize=(10, 6))
plt.bar(article_counts['article_sentiment_label'], article_counts['count'])
plt.xlabel('Sentiment')
plt.ylabel('Number of Articles')
plt.title('Number of Articles per Sentiment')
plt.xticks(rotation=90)
plt.show()










