import requests

url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2023-04-20&'
       'sortBy=popularity&'
       'apiKey=6820acc82f88498087cfe9b7d3b9fb17')

response = requests.get(url)

json_response = response.json()
print(json_response)
