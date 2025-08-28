import requests
from bs4 import BeautifulSoup

print('Input the URL:')
url = str(input())

if 'nature.com/articles/' in url:
    try:
        response = requests.get(url,
                                headers={'Accept-Language': 'en-US,en;q=0.5'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').get_text() if soup.find('title') else 'N/A'
            description_meta = soup.find('meta', {'name': 'description'})
            description = description_meta['content'] if description_meta and 'content' in description_meta.attrs else 'N/A'
            print({"title": title, "description": description})
        else:
            print('Invalid page!')
    except requests.exceptions.RequestException:
        print('Invalid page!')
else:
    print('Invalid page!')
