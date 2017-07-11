"""
    Train CJ-GLO model by different parameters, then test the result.
"""

import os

def fill_bi_cooccur_command(sentence_rate, cjglo, output_filename):
    cmd = "build/bi_cooccur -verbose 0"
    cmd += " -corpus-file-1 data/train.zh_parsed"
    cmd += " -corpus-file-2 data/train.ja_parsed"
    cmd += " -vocab-file output/vocab.cj_001"
    cmd += " -sentence-rate " + sentence_rate
    cmd += " -cjglo " + cjglo
    cmd += " > output/" + output_filename
    return cmd

def run_by_list(sentence_rate_list, cjglo_list):
    for sentence_rate in sentence_rate_list:
        for cjglo in cjglo_list:
            output_filename = "exp_sr_" + sentence_rate + "_cj_" + cjglo
            cmd = fill_bi_cooccur_command(sentence_rate, cjglo, output_filename)
            print cmd

def main():
    sentence_rate_list = ["1"]
    cjglo_list = ["0"]
    run_by_list(sentence_rate_list, cjglo_list)


if __name__ == '__main__':
    main()