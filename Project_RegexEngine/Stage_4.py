class RegexEngine:

    def __init__(self, regex, text):
        self.start = False
        self.end = False
        self.s = text
        preregex = regex
        if not regex == '' and regex[0] == '^':
            preregex = preregex[1:]
            self.start = True
        if not regex == '' and regex[-1] == '$':
            preregex = preregex[:-1]
            self.end = True
        self.r = preregex

    def period(self, r, s):
        if r == '.' or r == '':
            return True
        return r == s

    def recursive(self, r, s):
        if len(r) == 0 and not self.end:
            return True
        if len(r) == 0 and len(s) == 0 and self.end:
            return True
        if len(r) == 0 and len(s) > 0 and self.end:
            return False
        elif len(r) > 0 and len(s) == 0 and self.end:
            return False
        elif len(r) > 0 and len(s) == 0 and not self.end:
            return True
        elif len(r) > 0 and len(s) > 0 and not self.period(r[0], s[0]):
            return False
        elif len(r) > 0:
            return self.recursive(r[1:], s[1:])

    def sequential(self):
        result = False
        if self.r == '':
            result = True
        if self.start:
            if self.recursive(self.r, self.s):
                result = True
        else:
            for i in range(len(self.s)):
                if self.recursive(self.r, self.s[i:]):
                    result = True
                    break
        return result

def main():
    string = str(input())
    regex, text = string.split("|")
    regex_engine = RegexEngine(regex, text)
    print(regex_engine.sequential())


if __name__ == "__main__":
    main()
