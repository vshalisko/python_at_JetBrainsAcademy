import requests
from bs4 import BeautifulSoup

stage = 3

print('Input the URL:')
url = str(input())

if stage == 3:
    from http import HTTPStatus

    try:
        response = requests.get(url)
        if response.status_code == HTTPStatus.OK:
            with open('source.html', 'wb') as f:
                f.write(response.content)
            print('Content saved.')
        else:
            print(f'The URL returned {response.status_code}!')
    except requests.exceptions.RequestException:
        print('Invalid URL or network error.')
