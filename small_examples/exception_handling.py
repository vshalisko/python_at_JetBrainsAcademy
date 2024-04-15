## Example 1
import re

class WordError(Exception):
    pass

def check_w_letter(word):
    if not re.findall(r'w', word):
        return word
    else:
        raise WordError

  ## Example 2
  def check_integer(num):
    if num >= 45 and num <= 67:
        return num
    else:
        raise NotInBoundsError

def error_handling(num):
    try:
        result = check_integer(num)
        print(result)
    except NotInBoundsError as err:
        print(err)
