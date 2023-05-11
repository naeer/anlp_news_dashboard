from datetime import datetime, timedelta
from news import ArticlesFromNewsAPI

# Get the current date
current_date = datetime.now()

# Calculate the date one month ago
one_month_ago = current_date - timedelta(days=29)

from_date = one_month_ago

if __name__ == "__main__":
    articlesFromNewsAPI = ArticlesFromNewsAPI(source='news.com.au', topic='Australia', from_date=from_date)
    df = articlesFromNewsAPI.get_all_articles_from_last_month()
    print(df)
