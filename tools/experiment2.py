"""
    Experiment 2
    Use a file of word pairs, to calculate Cross-Lingual Synonym Comparison 
"""

import argparse
import numpy as np
import sys

def generate():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vocab_file', default='vocab.txt', type=str)
    parser.add_argument('--vectors_file', default='vectors.txt', type=str)
    args = parser.parse_args()

    with open(args.vocab_file, 'r') as f:
        words = [x.rstrip().split(' ')[0] for x in f.readlines()]
    with open(args.vectors_file, 'r') as f:
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
        if word == '<unk>':
            continue
        W[vocab[word], :] = v

    # normalize each word vector to unit variance
    W_norm = np.zeros(W.shape)
    d = (np.sum(W ** 2, 1) ** (0.5))
    W_norm = (W.T / d).T
    return (W_norm, vocab, ivocab)


def distance(W, vocab, ivocab, word1, word2):
    if not word1 in vocab:
        print('Word: %s  Out of dictionary!\n' % word1)
        return
    if not word2 in vocab:
        print('Word: %s  Out of dictionary!\n' % word2)
        return
    vec_result = np.copy(W[vocab[word1], :])
    
    vec_norm = np.zeros(vec_result.shape)
    d = (np.sum(vec_result ** 2,) ** (0.5))
    vec_norm = (vec_result.T / d).T

    dist = np.dot(W, vec_norm.T)

    #for term in input_term.split(' '):
    index = vocab[word1]
    dist[index] = -np.Inf

    a = np.argsort(-dist)#[:N]

    #print("\n                               Word       Cosine distance\n")
    #print("---------------------------------------------------------\n")
    #for x in a:
    #    print("%35s\t\t%f" % (ivocab[x], dist[x]))

    idx = 0
    for x in a:
        if ivocab[x][0] == word2[0]:
            idx += 1
            if ivocab[x] == word2:
                #print("%s -> %s %f" % (word1, ivocab[x], dist[x]))
                #break
                return idx, dist[x]
    print("Error: %s -> %s %f" % (word1, word2))
    return -1, -1

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
    N = 20;          # number of closest words that will be shown
    print "reading word embeddings"
    W, vocab, ivocab = generate()
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
        idx1, dist1 = distance(W, vocab, ivocab, word1, word2)
        ja_rate += 1 - idx1 * 1.0 / ja_wc
        idx2, dist2 = distance(W, vocab, ivocab, word2, word1)
        zh_rate += 1 - idx2 * 1.0 / zh_wc
        item = (word1, word2, idx1, dist1, idx2, dist2)
        result.append(item)
        print word1, word2, idx1, dist1, idx2, dist2
    ja_rate /= cnt
    zh_rate /= cnt
    print "Total", cnt, "pairs, ja_rate", ja_rate, "zh_rate", zh_rate


