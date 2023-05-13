from datetime import datetime, timedelta
from news import ArticlesFromNewsAPI
from api import *
#import openai
import pandas as pd

# Get the current date
current_date = datetime.datetime.now()

# Calculate the date one month ago
one_month_ago = current_date - timedelta(days=29)

from_date = one_month_ago


# openai.api_key = "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"

# # Define a function to generate summaries using OpenAI's GPT-3 API
# def generate_summary(text):
#     prompt = (f"Please summarize the following text:\n\n'{text}'")
#     response = openai.Completion.create(
#     engine="text-davinci-002",
#     prompt=prompt,
#     temperature=0.5,
#     max_tokens=200,
#     n = 1,
#     stop=None,
#     timeout=10,
#     )
#     print(response)
#     summary = response.choices[0].text.strip()
#     return summary

if __name__ == "__main__":
    # if len(sys.argv) == 2:
    #     keyword = sys.argv[1]
    #     print(keyword)
    # else:
    #     keyword = 'Australia'
    #     print(keyword)

    keywords = ['facebook','snapchat','instagram','tiktok','twitter']
    # , 'Sydney', 'Melbourne', 'Brisbane', 'NATO', 'Formula1',
    #             'Police', 'Death', 'China', 'USA']

    df = pd.DataFrame(columns=['source', 'date', 'headline', 'article', 'url'])
    for keyword in keywords:
        keyword = keyword.lower()
        print(keyword)
        articlesFromNewsAPI = ArticlesFromNewsAPI(source='news.com.au', topic=keyword, from_date=from_date)
        df1 = articlesFromNewsAPI.get_all_articles_from_last_month()
        if df1 is not None:
            df = pd.concat([df, df1])
            print(df1)
        df2 = get_articles(keyword=keyword)
        print(df2)
        df = pd.concat([df, df2])

        #df.to_csv('/Users/gerar/OneDrive/Escritorio/MDSI/23-04autumn/ANLP/output.csv')




    # new_df = df.head(2)

    # # Apply the generate_summary function to each row in the DataFrame
    # new_df['summary'] = new_df['article'].apply(generate_summary)

    # # Print the resulting DataFrame with a summary for each article
    # print(new_df)





   


    #df.to_csv('/Users/naeeramin/Documents/UTS - 4th semester/ANLP/AT2/output30.csv')

