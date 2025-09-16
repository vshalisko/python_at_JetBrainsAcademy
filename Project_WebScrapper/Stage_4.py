import requests
from bs4 import BeautifulSoup

stage = 4

#print('Input the URL:')
#url = str(input())

if stage == 2:
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

if stage == 4:
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    article_tags = soup.find_all('article')
    news_article_urls = []

    for article in article_tags:
        article_type_tag = article.find('span', {'data-test': 'article.type'})
        if article_type_tag and article_type_tag.get_text(strip=True) == 'News':
            article_link_tag = article.find('a', {'data-track-action': 'view article'})
            if article_link_tag and 'href' in article_link_tag.attrs:
                news_article_urls.append("https://www.nature.com" + article_link_tag['href'])

    #print(f"Found {len(news_article_urls)} news article URLs.")
    #print(news_article_urls)

    parsed_articles = []

    for url in news_article_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                parsed_articles.append({"url": url, "soup": soup})
            else:
                print(f"Failed to retrieve the page {url}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while processing {url}: {e}")

    #print(f"Successfully parsed {len(parsed_articles)} news articles.")

    for article in parsed_articles:
        soup = article['soup']
        body_tag = soup.find('p', {"class": "article__teaser"})
        if body_tag:
            article['body'] = body_tag.get_text(strip=True)
        else:
            article['body'] = 'Body not found'

    #for article in parsed_articles:
        #print(f"URL: {article['url']}")
        #print(f"Body: {article['body']}")
        #print("-" * 20)

    import re

    filenames = []
    for article in parsed_articles:
        soup = article['soup']
        title_tag = soup.find('title')
        title = title_tag.get_text() if title_tag else 'Untitled'
        formatted_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')
        filename = f"{formatted_title}.txt"
        filenames.append(filename)
        body = article['body']

        try:
            with open(filename, 'wb') as f:
                f.write(body.encode('utf-8'))
            #print(f"Content saved to {filename}")
        except IOError as e:
            print(f"Error saving content to {filename}: {e}")

    print('Saved articles:')
    print(filenames)
