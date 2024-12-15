class RegexEngine:

    def __init__(self, regex, text):
        self.r = regex
        self.s = text

    def period(self, r, s):
        if r == '.' or r == '':
            return True
        return r == s

    def recursive(self, r, s):

        if len(r) == 0:
            return True
        elif r and not s:
            return False
        elif not self.period(r[0], s[0]):
            return False
        else:
            return self.recursive(r[1:], s[1:])

def main():
    string = str(input())
    regex, text = string.split("|")
    regex_engine = RegexEngine(regex, text)
    print(regex_engine.recursive(regex, text))


if __name__ == "__main__":
    main()
