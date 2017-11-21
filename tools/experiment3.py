


class Token():
    def __init__(self, zh_county, zh_city, ja_county, ja_city):
        self.zh_county = zh_county
        self.zh_city = zh_city
        self.ja_county = ja_county
        self.ja_city = ja_city



def read_analogy():
    fin = open("data/analogy_02/analogy_source.txt", 'r')
    for i in xrange(7):
        fin.readline()
        line = fin.readline()
        tokens = line.split()
                # in data file, 0 - ja, 1 - zh
                for k in xrange(4):
                    if tokens[k] == 0:







if __name__ == "__main__":
