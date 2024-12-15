class RegexEngine:

    def __init__(self, regex, text):
        self.r = regex
        self.s = text

    def period(self, a, b):
        if a == '.' or a == '':
            return True
        return a == b

    def recursive(self):

        r_list = []
        s_list = []
        if len(self.r) > 0:
            r_list = list(self.r)
        if len(self.s) > 0:
            s_list = list(self.s)

        result = True
        if len(r_list) > len(s_list):
            result = False
        else:
            for i in range(len(r_list)):
                #print(r_list[i], s_list[i])
                if not self.period(str(r_list[i]),str(s_list[i])):
                    result = False

        return result

def main():
    string = str(input())
    regex, text = string.split("|")
    regex_engine = RegexEngine(regex, text)
    print(regex_engine.recursive())


if __name__ == "__main__":
    main()
