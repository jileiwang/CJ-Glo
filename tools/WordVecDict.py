"""
    Experiment 2
    Use a file of word pairs, to calculate Cross-Lingual Synonym Comparison 
"""

import argparse
import numpy as np
import sys

class WordVecDict(object):
    def __init__(self, vocab_file, vectors_file):
        self.vocab_file = vocab_file
        self.vectors_file = vectors_file
        self.generate()

    def generate(self):
        with open(self.vocab_file, 'r') as f:
            words = [x.rstrip().split(' ')[0] for x in f.readlines()]
        with open(self.vectors_file, 'r') as f:
            vectors = {}
            for line in f:
                vals = line.rstrip().split(' ')
                vectors[vals[0]] = [float(x) for x in vals[1:]]

        vocab_size = len(words)
        vocab = {w: idx for idx, w in enumerate(words)}
        ivocab = {idx: w for idx, w in enumerate(words)}

        vector_dim = len(vectors[ivocab[0]])
        W = np.zeros((vocab_size, vector_dim))
        for word, v in vectors.items():
            if word == '<unk>' or word == '2</s>':
                continue
            W[vocab[word], :] = v

        # normalize each word vector to unit variance
        W_norm = np.zeros(W.shape)
        d = (np.sum(W ** 2, 1) ** (0.5))
        W_norm = (W.T / d).T
        
        self.W = W_norm
        self.vocab = vocab
        self.ivocab = ivocab

    def distance(self, word1, word2, verbose = False):
        if not word1 in self.vocab:
            print('Word: %s  Out of dictionary!\n' % word1)
            return
        if not word2 in self.vocab:
            print('Word: %s  Out of dictionary!\n' % word2)
            return
        vec_result = np.copy(self.W[self.vocab[word1], :])
        
        vec_norm = np.zeros(vec_result.shape)
        d = (np.sum(vec_result ** 2,) ** (0.5))
        vec_norm = (vec_result.T / d).T

        dist = np.dot(self.W, vec_norm.T)

        #for term in input_term.split(' '):
        index = self.vocab[word1]
        dist[index] = -np.Inf

        a = np.argsort(-dist)#[:N]

        idx = 0
        for x in a:
            # in same language
            if self.ivocab[x][0] == word2[0]:
                idx += 1
                if verbose:
                    print idx, self.ivocab[x], dist[x]
                if self.ivocab[x] == word2:
                    return idx, dist[x]
        print("Error: %s -> %s %f" % (word1, word2))
        return -1, -1

    def analogy(self, words, verbose = False):
        """
            words = <w0, w1, w2, w3>
            Find distance of (w1 - w0 + w2) and w3
        """
        v0 = np.copy(self.W[self.vocab[words[0]], :])
        v1 = np.copy(self.W[self.vocab[words[1]], :])
        v2 = np.copy(self.W[self.vocab[words[2]], :])
        v = np.add(v1, v2)
        vec_result = np.subtract(v, v0)

        vec_norm = np.zeros(vec_result.shape)
        d = (np.sum(vec_result ** 2,) ** (0.5))
        vec_norm = (vec_result.T / d).T

        dist = np.dot(self.W, vec_norm.T)

        #for term in input_term.split(' '):
        for i in [0, 1, 2]:
            index = self.vocab[words[i]]
            dist[index] = -np.Inf

        a = np.argsort(-dist)#[:N]

        idx = 0
        for x in a:
            # in same language
            if self.ivocab[x][0] == words[3][0]:
                idx += 1
                if verbose:
                    print idx, self.ivocab[x], dist[x]
                if self.ivocab[x] == words[3]:
                    return idx, dist[x]
        print("Error")
        return -1, -1



    def sentenceVec(self, sentence):
        """
            input sentence = <w0, w1, ...>
            calculate the average data of corresponding <v0, v1, v2>
        """
        sen = []
        for w in sentence:
            if w in self.vocab:
                sen.append(w)

        if len(sen) == 0:
            return None

        tmp = self.W[0, :]
        vec = np.zeros(tmp.shape)
        for w in sen:
            v = np.copy(self.W[self.vocab[w], :])
            vec = np.add(vec, v)
        vec = vec / (len(sen) * 1.0)
        return vec





def readWordPairs():
    path = "experiment/experiment2_data.txt"
    fin = open(path, 'r')
    wordPairList = []
    for line in fin.readlines():
        if len(line) > 2:
            words = line.split()
            w1 = "2" + words[0].strip()
            w2 = "1" + words[1].strip()
            wordPairList.append((w1, w2))
    return wordPairList

if __name__ == "__main__":
    print "reading word embeddings"
    wordVecDict = WordVecDict("output/vocab.cj_001", "output/batch_02/ctrl_s_0.03.vec.txt")
    print "reading word pairs"
    wordPairList = readWordPairs()
    print "calculating distances"

    ja_wc = 22748
    zh_wc = 25219

    result = []
    # ja, zh word pair
    ja_rate = 0
    zh_rate = 0
    cnt = 0
    for word1, word2 in wordPairList:
        cnt += 1
        idx1, dist1 = wordVecDict.distance(word1, word2)
        ja_rate += 1 - idx1 * 1.0 / ja_wc
        idx2, dist2 = wordVecDict.distance(word2, word1)
        zh_rate += 1 - idx2 * 1.0 / zh_wc
        item = (word1, word2, idx1, dist1, idx2, dist2)
        result.append(item)
        print word1, word2, idx1, dist1, idx2, dist2
    ja_rate /= cnt
    zh_rate /= cnt
    print "Total", cnt, "pairs, ja_rate", ja_rate, "zh_rate", zh_rate


