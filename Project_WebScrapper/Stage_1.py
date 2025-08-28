import requests

print('Input the URL:')
url = str(input())

try:
    response = requests.get(url, headers={'Accept': 'application/json'})
    if response.status_code == 200:
        data = response.json()
        if 'joke' in data:
            print(data['joke'])
        else:
            print('Invalid resource!')
    else:
        print('Invalid resource!')
except requests.exceptions.RequestException:
    print('Invalid resource!')
