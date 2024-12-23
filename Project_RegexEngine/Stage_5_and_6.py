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
        """Basic one character check"""
        if r == '.' or r == '':
            return True
        return r == s

    def check_question(self, r, s):
        """Question mark case"""
        if self.period(r[0], s[0:1]) and self.recursive(r[2:], s[1:]):
            return True
        return self.recursive(r[2:], s)

    def check_star(self, r, s):
        """Star mark case"""
        if self.period(r[0], s[0:1]) and self.recursive(r, s[1:]):
            return True
        return self.recursive(r[2:], s)

    def check_plus(self, r, s):
        """Plus mark case"""
        if self.period(r[0], s[0:1]):
            return self.recursive(r, s[1:]) or self.recursive(r[2:], s[1:])
        return False

    def recursive(self, r, s):
        """Recursive pattern check"""
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
                if r[0] == '\\':                      # This line is required for stage 6
                    return self.recursive(r[1:], s)   # This line is required for stage 6
                elif r[1:2] == '?':
                    return self.check_question(r, s)
                elif r[1:2] == '*':
                    return self.check_star(r, s)
                elif r[1:2] == '+':
                    return self.check_plus(r, s)
                elif self.period(r[0], s[0]):
                    return self.recursive(r[1:], s[1:])
                else:
                    return False

    def sequential(self):
        """Test string in a sequential way except start case"""
        result = False
        if not self.r:
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
