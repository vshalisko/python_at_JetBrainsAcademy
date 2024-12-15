class RegexEngine:

    def __init__(self, regex, text):
        self.r = regex
        self.s = text

    def period(self):
        if self.r == '.' or self.r == '':
            return True
        return self.r == self.s


def main():
    string = str(input())
    regex, text = string.split("|")
    regex_engine = RegexEngine(regex, text)
    print(regex_engine.period())


if __name__ == "__main__":
    main()
