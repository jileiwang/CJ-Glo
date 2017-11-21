


vocab_file = "output/vocab.cj_001"


def getVocab():
    vocab = set()
    for line in open(vocab_file):
        if len(line) >= 3:
            vocab.add(line.split()[0])
    return vocab

def count(vocab, filename, lang):
    dic = {}
    for line in open(filename):
        cnt = 0
        for w in line.split():
            v = lang + w
            if v in vocab:
                cnt += 1
        dic[cnt] = dic.get(cnt, 0) + 1
    return dic

if __name__ == "__main__":
    vocab = getVocab()
    zh = count(vocab, 'data/train.zh_parsed', '1')
    ja = count(vocab, 'data/train.ja_parsed', '2')
    zhLine = ""
    jaLine = ""
    for i in xrange(331):
        zhLine += "%i," % zh.get(i, 0)
        jaLine += "%i," % ja.get(i, 0)
    print zhLine[:-1]
    print jaLine[:-1]
