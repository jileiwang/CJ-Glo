

from WordVecDict import WordVecDict
from AnalogyData import AnalogyData

data = AnalogyData()
ja_wc = 22748
zh_wc = 25219

def calculateRate(idx, word):
    if word[0] == '1':
        return 1 - idx * 1.0 / zh_wc
    else:
        return 1 - idx * 1.0 / ja_wc

def batchCtrl():
    for b in xrange(1, 6):
        inputFile = "output/batch_02/ctrl_s_0.0%i.vec.txt" % b
        wordVecDict = WordVecDict("output/vocab.cj_001", inputFile)
        for zhCount in xrange(5):
            outputFile = "output/batch_02/analogy_01/ctrl_s_0.0%i_zh_%i.csv" % (b, zhCount)
            print "Writing to", outputFile, '... ... ... ...'
            fout = open(outputFile, 'w')
            records = data.getByZhCount(zhCount)
            for record in records:
                idx, _ = wordVecDict.analogy(record)
                rate = calculateRate(idx, record[3])
                line = ','.join(record)
                line += ',%i,%f\n' % (idx, rate)
                fout.write(line)
            fout.close()


def batchExp():
    for s in xrange(1, 6):
        for c in xrange(1, 6):
            inputFile = "output/batch_02/exp_s_0.0%i_c_0.0%i.vec.txt" % (s, c)
            wordVecDict = WordVecDict("output/vocab.cj_001", inputFile)
            for zhCount in xrange(5):
                outputFile = "output/batch_02/analogy_01/exp_s_0.0%i_c_0.0%i_zh_%i.csv" % (s, c, zhCount)
                print "Writing to", outputFile, '... ... ... ...'
                fout = open(outputFile, 'w')
                records = data.getByZhCount(zhCount)
                for record in records:
                    idx, _ = wordVecDict.analogy(record)
                    rate = calculateRate(idx, record[3])
                    line = ','.join(record)
                    line += ',%i,%f\n' % (idx, rate)
                    fout.write(line)
                fout.close()

if __name__ == '__main__':
    #batchCtrl()
    batchExp()