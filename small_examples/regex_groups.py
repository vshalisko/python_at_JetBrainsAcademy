##  consider a template for a string containing a date. Let's agree to accept the following formats of date:
## D(D)/M(M)/YYYY
## D(D).M(M).YYYY
## DD and MM can consist either of two or one digits, YYYY is always a four-digit expression. The digits should be separated either by a slash character / or by a dot . . One date can contain only slashes or only dots as separators.
## After writing the template, take a string from the input, and compare it against the template. If there's a match (the result of match() is not None), output the year mentioned in the string. If there's no match, output None.
## Examples of valid dates: 02.12.1997, 02/03/1965, 1.01.2000.
## Examples of invalid dates: 10.100.2105, 15.03.19114.

import re

# put your regex in the variable template
template = r"^(((\d\d?)/(\d\d?)/)|((\d\d?)\.(\d\d?)\.))(\d{4})$"
string = input() # do not output an input message
# compare the string and the template
m = re.match(template, string)
if m:
    print(m.group(8))
else:
    print(None)
