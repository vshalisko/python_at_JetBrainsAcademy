def plain():
    txt = input('Text: ')
    return txt

def header():
    min_level = 1
    max_level = 6
    while (level := int(input('Level: '))) not in range(min_level, max_level + 1):
        print(f'The level should be within the range of {min_level} to {max_level}')

    txt = input('Text: ')
    return '#' * level + ' ' + txt + '\n'

def link():
    label = input('Label: ')
    url = input('URL: ')
    return f'[{label}]({url})'

def new_line():
    return '\n'

def inline_code():
    txt = input('Text: ')
    return f'`{txt}`'

def bold():
    txt = input('Text: ')
    return f'**{txt}**'

def italic():
    txt = input('Text: ')
    return f'*{txt}*'

def ordered_list():
    return ''

def unordered_list():
    return ''


formatters = {'plain': plain,
              'header': header,
             'link': link,
             'new-line': new_line,
             'inline-code': inline_code,
             'bold': bold,
             'italic': italic,
             'ordered-list': ordered_list,
             'unordered-list': unordered_list
              }

special = ['!help', '!done']

output = ""
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
        out = formatters[command]()
        if output:
            output += str(out)
        else:
            output = out
        print(output)
