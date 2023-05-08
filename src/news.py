import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

source = "news.com.au"
topic = "Australia"
from_date = "2023-04-10"

def call_everything_endpoint_of_news_api(source, topic, from_date):
       """
       Method to call the everything endpoint of NewsAPI 
       Returns a json response from the endpoint
       """
       url = ('https://newsapi.org/v2/everything?'
       'domains=' + source + '&'
       'q=' + topic + '&'
       'from=' + from_date + '&'
       'sortBy=popularity&'
       'apiKey=6820acc82f88498087cfe9b7d3b9fb17')
       response = requests.get(url)
       json_response = response.json()
       return json_response

def get_articles_from_json_response(response):
       """
       Method to retrieve information about articles in the form of a dataframe
       """
       articles = response['articles']
       df = pd.DataFrame(articles)
       return df

def get_list_article_urls(article_df):
       """
       Method to retrieve a list of article urls from article_df
       """
       article_urls = article_df['url'].tolist()
       return article_urls
       
def get_html_content(url):
       """
       Method to get the html content of the webpage using BeautifulSoup
       """
       page = requests.get(url)
       soup = BeautifulSoup(page.content, "html.parser")
       return soup

def get_article_content(html_content):
       """
       Method to get the main content of the article
       """
       results = html_content.find(id = 'story-primary')
       paragraphs = results.find_all("p")
       paras_list = []
       for para in paragraphs:
              paras_list.append(para.text)
       story = "\n".join(paras_list)
       return story

if __name__ == "__main__":
       resp = call_everything_endpoint_of_news_api(source=source, topic=topic, from_date=from_date)
       article_df = get_articles_from_json_response(response=resp)
       article_urls = get_list_article_urls(article_df=article_df)
       # print(article_urls)
       # print(len(article_urls))
       # print(article_urls[1])

       article_stories = []
       for article_url in article_urls:
              html_content = get_html_content(url=article_url)
              story_content = get_article_content(html_content=html_content)
              article_stories.append(story_content)
       print(article_stories)
       article_df['full_content'] = article_stories

# print(json.dumps(json_response, indent=4))

# print(json_response.status())

# keys = json_response.keys()

# print(keys)





# print(df.head(3))

# df.to_csv('/Users/naeeramin/Documents/UTS - 4th semester/ANLP/AT2/output2.csv')