from datetime import datetime, timedelta
from news import ArticlesFromNewsAPI
from api import get_articles
import pandas as pd

# Get the current date
current_date = datetime.now()

# Calculate the date one month ago
one_month_ago = current_date - timedelta(days=29)

from_date = one_month_ago


if __name__ == "__main__":

    keywords = ['facebook','snapchat','instagram','tiktok','twitter']

    df = pd.DataFrame(columns=['keyword','source', 'date', 'headline', 'article', 'url'])
    for keyword in keywords:
        keyword = keyword.lower()
        print(keyword)
        articlesFromNewsAPI = ArticlesFromNewsAPI(source='news.com.au', topic=keyword, from_date=from_date)
        df1 = articlesFromNewsAPI.get_all_articles_from_last_month()
        if df1 is not None:
            df1['keyword'] = keyword
            df1['date'] = df1['date'].apply(
                lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'))

            df = pd.concat([df, df1])
            print(df1)
        df2 = get_articles(keyword=keyword)
        df2['keyword'] = keyword
        print(df2)
        df = pd.concat([df, df2])

    df.to_csv('/Users/gerar/OneDrive/Escritorio/MDSI/23-04autumn/ANLP/anlp_news_dashboard/src/data_prep_app.csv', encoding='utf-8')








   



