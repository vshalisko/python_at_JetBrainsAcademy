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

        if len(r) == 0:
            if self.end:
                if len(s) == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            if len(s) == 0:
                if self.end:
                    return False
                else:
                    return True
            else:
                if self.period(r[0], s[0]):
                    return self.recursive(r[1:], s[1:])
                else:
                    return False

    def sequential(self):
        result = False
        if not self.r:
            result = True
        if self.start:
            if self.recursive(self.r, self.s):
                result = True
        else:
            for i in range(len(self.s)):
                #print("Here", str(i))
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
