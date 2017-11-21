

from WordVecDict import WordVecDict
import numpy as np


def readTestDataFile(filename, prefix):
    data = []
    for line in open(filename, 'r').readlines():
        if len(line) == 0:
            continue
        sentence = []
        for w in line.split():
            sentence.append(prefix + w)
        data.append(sentence)
    return data

def readTestData():
    zhData = readTestDataFile("data/test.zh_parsed", "1")
    jaData = readTestDataFile("data/test.ja_parsed", "2")
    return zhData, jaData

def calculateAcc(vecFile):
    wordVecDict = WordVecDict("output/vocab.cj_001", vecFile)
    zhData, jaData = readTestData()
    n = len(zhData)
    zhVec = []
    jaVec = []
    for i in xrange(n):
        zhVec.append(wordVecDict.sentenceVec(zhData[i]))
        jaVec.append(wordVecDict.sentenceVec(jaData[i]))
    
    matrix = []
    for i in xrange(n):
        line = []
        for j in xrange(n):
            line.append(np.dot(zhVec[i], jaVec[j]))
        matrix.append(line)


    dic = {}
    acc = 0
    for i in xrange(n):
        order = [(matrix[i][j], j) for j in xrange(n)]
        order.sort()
        for j in xrange(n):
            if order[j][1] == i:
                #print "Zh", i, "matches Ja", i, "at position", n - j
                k = n - j # oerder is from small to big, so k == 1 is the best match
                dic[k] = dic.get(k, 0) + 1
                acc += 1.0 - (k - 1.0) / n 
                break

    acc = acc * 1.0 / n
    return acc


def batch():
    for s in xrange(1, 6):
        for c in xrange(1, 6):
            inputFile = "output/batch_02/exp_s_0.0%i_c_0.0%i.vec.txt" % (s, c)
            print calculateAcc(inputFile), 
        print ""


if __name__ == "__main__":
    #print calculateAcc("output/batch_02/ctrl_s_0.03.vec.txt")
    batch()




