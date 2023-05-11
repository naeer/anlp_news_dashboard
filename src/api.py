# Import packages

import nltk
import pandas as pd
import requests as r
from dateutil import parser
import sys
import datetime


def create_df(art_response):
    guardian_api_key = '231ce917-65b5-4019-b365-c79f213379d1'
    art_title = []
    for article in art_response["response"]["results"]:
        extract_title = article['webTitle']
        art_title.append(extract_title)

    # Creating a loop to extract article content.
    art_body = []
    for article in art_response["response"]["results"]:
        url = f'{article["apiUrl"]}?api-key={guardian_api_key}&show-fields=bodyText'
        article_content = r.get(url).json()
        body_text = article_content["response"]['content']['fields']['bodyText']
        art_body.append(body_text)

    # Creating a loop to extract article date.
    art_dates = []
    for article in art_response["response"]["results"]:
        extract_dates = article['webPublicationDate']
        extract_dates = parser.parse(extract_dates)
        extract_dates = extract_dates.date()
        art_dates.append(extract_dates)

    # Creating a loop to extract article section.
    art_section = []
    for article in art_response["response"]["results"]:
        extract_sect = article['sectionName']
        art_section.append(extract_sect)

    # Creating a loop to extract url.
    art_url = []
    for article in art_response["response"]["results"]:
        extract_url = article['webUrl']
        art_url.append(extract_url)

    # Create dataframe

    art_body_date = pd.DataFrame(
        {'source': 'Guardian',
         'date': art_dates,
         'headline': art_title,
         'article': art_body,
         # 'section': art_section,
         'url': art_url
         })

    # art_body_date['year_month'] = pd.to_datetime(art_body_date['date']).dt.to_period('M')

    # print(art_body_date)

    return art_body_date


def set_parameters(keyword):
    guardian_api_key = '231ce917-65b5-4019-b365-c79f213379d1'
    query_keywords = f'"{keyword}"'
    query_fields = 'headline'
    delta = datetime.timedelta(days=29)
    from_datetime = datetime.datetime.now() - delta
    from_date = from_datetime.strftime("%Y-%m-%d")
    to_date = datetime.datetime.now().strftime("%Y-%m-%d")
    page = '1'  # page#, can only do one page at a time
    page_size = '100'  # up to 200
    prod_off = 'aus'
    order_by = 'newest'

    # Call API and generate response with articles

    response = r.get(f'https://content.guardianapis.com/search?q={query_keywords}'
                     f'&query-fields={query_fields}'
                     f'&from-date={from_date}'
                     f'&to-date={to_date}'
                     f'&page={page}'
                     f'&page-size={page_size}'
                     f'&production-office={prod_off}'
                     f'&order-by={order_by}'
                     f'&api-key={guardian_api_key}')
    art_response = response.json()
    # print(art_response)

    return art_response


def main():
    if len(sys.argv) == 2:
        keyword = sys.argv[1]
        print(keyword)
    else:
        keyword = 'Australia'
        print(keyword)

    param = set_parameters(keyword)
    df = create_df(param)
    print(df)
    # print(df.columns)


if __name__ == "__main__":
    main()
