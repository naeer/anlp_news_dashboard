import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

class ArticlesFromNewsAPI():

       def __init__(self, source, topic, from_date) -> None:
              self.source = source
              self.topic = topic
              self.from_date = from_date

       def call_everything_endpoint_of_news_api(self):
              """
              Method to call the everything endpoint of NewsAPI 
              Returns a json response from the endpoint
              """
              url = ('https://newsapi.org/v2/everything?'
              'domains=' + self.source + '&'
              'q=' + self.topic + '&'
              'from=' + str(self.from_date) + '&'
              'sortBy=popularity&'
              'apiKey=6820acc82f88498087cfe9b7d3b9fb17')
              response = requests.get(url)
              json_response = response.json()
              return json_response

       def get_articles_from_json_response(self, response):
              """
              Method to retrieve information about articles in the form of a dataframe
              """
              articles = response['articles']
              df = pd.DataFrame(articles)
              return df

       def get_list_article_urls(self, article_df):
              """
              Method to retrieve a list of article urls from article_df
              """
              article_urls = article_df['url'].tolist()
              return article_urls
              
       def get_html_content(self, url):
              """
              Method to get the html content of the webpage using BeautifulSoup
              """
              page = requests.get(url)
              soup = BeautifulSoup(page.content, "html.parser")
              return soup

       def get_article_content(self, html_content):
              """
              Method to get the main content of the article
              """
              results = html_content.find(id = 'story-primary')
              if results:
                     paragraphs = results.find_all("p")
                     if paragraphs:
                            paras_list = []
                            for para in paragraphs:
                                   paras_list.append(para.text)
                            story = "\n".join(paras_list)
                            return story
              return " "

       def get_article_contents_for_all_articles(self, list_article_urls):
              """
              Method to get the article content for all articles from their urls
              """
              article_stories = []
              for article_url in list_article_urls:
                     html_content = self.get_html_content(url=article_url)
                     story_content = self.get_article_content(html_content=html_content)
                     article_stories.append(story_content)
              return article_stories

       def get_all_articles_from_last_month(self):
              """
              Method to get the source, date, headline, article content and url of articles from the last month
              """
              resp = self.call_everything_endpoint_of_news_api()
              article_df = self.get_articles_from_json_response(response=resp)
              if article_df is not None:
                     article_urls = self.get_list_article_urls(article_df=article_df)
                     article_stories = self.get_article_contents_for_all_articles(list_article_urls=article_urls)
                     article_df['full_content'] = article_stories
                     article_df['source'] = 'news.com.au'

                     final_article_df = pd.DataFrame({
                            'source': article_df['source'],
                            'date': article_df['publishedAt'],
                            'headline': article_df['title'],
                            'article': article_df['full_content'],
                            'url': article_df['url']
                     })
                     return final_article_df
              return None

# if __name__ == "__main__":
#        resp = call_everything_endpoint_of_news_api(source=source, topic=topic, from_date=from_date)
#        article_df = get_articles_from_json_response(response=resp)
#        article_urls = get_list_article_urls(article_df=article_df)
#        # print(article_urls)
#        # print(len(article_urls))
#        # print(article_urls[1])

#        article_stories = get_article_contents_for_all_articles(list_article_urls=article_urls)
#        print(article_stories)
#        article_df['full_content'] = article_stories
#        print(article_df.columns)
#        article_df['source'] = 'news.com.au'

#        final_article_df = pd.DataFrame({
#               'source': article_df['source'],
#               'date': article_df['publishedAt'],
#               'headline': article_df['title'],
#               'article': article_df['full_content'],
#               'url': article_df['url']
#        })
#        final_article_df.to_csv('/Users/naeeramin/Documents/UTS - 4th semester/ANLP/AT2/output5.csv')



# print(json.dumps(json_response, indent=4))

# print(json_response.status())

# keys = json_response.keys()

# print(keys)





# print(df.head(3))

# df.to_csv('/Users/naeeramin/Documents/UTS - 4th semester/ANLP/AT2/output2.csv')