

class AnalogyData():
    def __init__(self):
        self.read_analogy()
        self.translationPairs = None
        self.crossZh = None
        self.crossJa = None
        self.cross2Zh2Ja = None
        self.cross1Zh3Ja = None
        self.cross3Zh1Ja = None

    def read_analogy(self):
        self.records = []
        fin = open("data/analogy_02/analogy_source.txt", 'r')
        for i in xrange(7):
            line = fin.readline()
            words = line.split()
            # in cjboc data file, 0 - ja, 1 - zh
            # in cjglo data file, 1 - zh, 2 - ja
            zh_county = '1' + words[0]
            zh_city = '1' + words[1]
            ja_county = '2' + words[2]
            ja_city = '2' + words[3]
            record = [[zh_county, zh_city], [ja_county, ja_city]]
            self.records.append(record)

    # in the translation pairs
    def generateTranslationPairs(self):
        self.translationPairs = []
        for record in self.records:
            # self.translationPairs.append((token.zh_county, token.zh_city, token.ja_county, token.ja_city))
            # self.translationPairs.append((token.zh_city, token.zh_county, token.ja_city, token.ja_county))
            # self.translationPairs.append((token.ja_county, token.ja_city, token.zh_county, token.zh_city))
            # self.translationPairs.append((token.ja_city, token.ja_county, token.zh_city, token.zh_county))
            for lang in [0, 1]:
                for c in [0, 1]:
                    self.translationPairs.append(record[lang][c], record[lang][1-c], record[1-lang][c], record[1-lang][1-c])

    def getTranslationPairs(self):
        if not self.translationPairs:
            self.generateTranslationPairs() 



    def generateCrossSingleLang(self, lang):
        result = []
        for record1 in self.records:
            for record2 in self.records:
                if record1 == record2:
                    continue
                for c in [0, 1]:
                    result.append((record1[lang][c], record1[lang][1-c], record2[lang][c], record2[lang][1-c]))
        return result



    def generateCrossZh(self):
        self.crossZh = self.generateCrossSingleLang(0)

    def getCrossZh(self):
        if not self.crossZh:
            self.generateCrossZh()
        return self.crossZh


        
    def generateCrossJa(self):
        self.crossJa = self.generateCrossSingleLang(1)

    def getCrossJa(self):
        if not self.crossJa:
            self.generateCrossJa()
        return self.crossJa



    def generateCross2Zh2Ja(self):
        self.cross2Zh2Ja = []
        for record1 in self.records:
            for record2 in self.records:
                if record1 == record2:
                    continue
                for c in [0, 1]:
                    self.cross2Zh2Ja.append((record1[0][c], record1[0][1-c], record2[1][c], record2[1][1-c]))
                    self.cross2Zh2Ja.append((record1[0][c], record1[1][1-c], record2[0][c], record2[1][1-c]))
                    self.cross2Zh2Ja.append((record1[0][c], record1[1][1-c], record2[1][c], record2[0][1-c]))
                    self.cross2Zh2Ja.append((record1[1][c], record1[0][1-c], record2[0][c], record2[1][1-c]))
                    self.cross2Zh2Ja.append((record1[1][c], record1[0][1-c], record2[1][c], record2[0][1-c]))
                    self.cross2Zh2Ja.append((record1[1][c], record1[1][1-c], record2[0][c], record2[0][1-c]))

    def getCross2Zh2Ja(self):
        if not self.cross2Zh2Ja:
            self.generateCross2Zh2Ja()
        return self.cross2Zh2Ja


    def generateCross1vs3(self, lang):
        # lang has 1 token
        result = []
        for record1 in self.records:
            for record2 in self.records:
                if record1 == record2:
                    continue
                for c in [0, 1]:
                    result.append((record1[lang][c], record1[1-lang][1-c], record2[1-lang][c], record2[1-lang][1-c]))
                    result.append((record1[1-lang][c], record1[lang][1-c], record2[1-lang][c], record2[1-lang][1-c]))
                    result.append((record1[1-lang][c], record1[1-lang][1-c], record2[lang][c], record2[1-lang][1-c]))
                    result.append((record1[1-lang][c], record1[1-lang][1-c], record2[1-lang][c], record2[lang][1-c]))
        return result



    def generateCross1Zh3Ja(self):
        self.cross1Zh3Ja = self.generateCross1vs3(0)

    def getCross1Zh3Ja(self):
        if not self.cross1Zh3Ja:
            self.generateCross1Zh3Ja()
        return self.cross1Zh3Ja



    def generateCross3Zh1Ja(self):
        self.cross3Zh1Ja = self.generateCross1vs3(1)

    def getCross3Zh1Ja(self):
        if not self.cross3Zh1Ja:
            self.generateCross3Zh1Ja()
        return self.cross3Zh1Ja



    def getByZhCount(self, zhCount):
        if zhCount == 0:
            return self.getCrossJa()
        elif zhCount == 1:
            return self.getCross1Zh3Ja()
        elif zhCount == 2:
            return self.getCross2Zh2Ja()
        elif zhCount == 3:
            return self.getCross3Zh1Ja()
        else:
            return self.getCrossZh()




if __name__ == '__main__':
    data = AnalogyData()
    #for t in data.getCross3Zh1Ja():
    #for t in data.getCross1Zh3Ja():
    #for t in data.getCross2Zh2Ja():
    for t in data.getCrossZh():
        print t[0], t[1], t[2], t[3]


