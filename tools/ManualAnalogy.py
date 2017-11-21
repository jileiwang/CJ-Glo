

import WordVecDict

if __name__ == '__main__':
    #vecFile = "output/batch_02/exp_s_0.05_c_0.05.vec.txt"
    vecFile = "cjboc_output/batch_01/exp_s_0.05_c_0.05.cjboc.txt"
    #wordVecDict = WordVecDict.WordVecDict("output/vocab.cj_001", "output/batch_02/ctrl_s_0.03.vec.txt")
    wordVecDict = WordVecDict.WordVecDict("output/vocab.cj_001", )
    while True:
        print "Input w0 w1:"
        line = raw_input()
        print wordVecDict.analogy(line.split(), True)