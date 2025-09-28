formatters = {'plain': 'plain',
              'header': 'header',
             'link': 'link',
             'new-line': 'new_line',
             'inline-code': 'inline_code',
             'bold': 'bold',
             'italic': 'italic',
             'ordered-list': 'ordered_list',
             'unordered-list': 'unordered_list'
              }

special = ['!help', '!done']

while True:
    command = input('Choose a formatter: ')
    if command == '!done':
        break
    if command == '!help':
        print(f'Available formatters: {" ".join(formatters)}')
        print(f'Special commands: {" ".join(special)}')
    elif command not in formatters and command not in special:
        print('Unknown formatting type or command')
    else:
        continue
