"""
    Count the sentence lenth of a parsed (after word segmentation) corpus.
"""
import argparse

def count_length():
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus_file', default='train.js_parsed', type=str)
    args = parser.parse_args()
    fin = open(args.corpus_file)
    dic = {}
    for line in fin:
        length = len(line.split())
        dic[length] = dic.get(length, 0) + 1
    return dic

if __name__ == '__main__':
    dic = count_length()
    print dic