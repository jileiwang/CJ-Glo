

import WordVecDict

if __name__ == '__main__':
    #wordVecDict = WordVecDict.WordVecDict("output/vocab.cj_001", "output/batch_02/ctrl_s_0.03.vec.txt")
    wordVecDict = WordVecDict.WordVecDict("output/vocab.cj_001", "output/batch_02/exp_s_0.05_c_0.05.vec.txt")
    while True:
        print "Input w0 w1 w2 w3:"
        line = raw_input().split()
        print wordVecDict.distance(line[0], line[1], True)