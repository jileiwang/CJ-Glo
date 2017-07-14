"""
    Train CJ-GLO model by different parameters, then test the result.
"""

import os

def fill_glove_command(input_filename, output_filename):
    cmd = "build/glove -save-file " + output_filename
    cmd += " -threads 8"
    cmd += " -input-file " + input_filename
    cmd += " -x-max 10"
    cmd += " -iter 15"
    cmd += " -vector-size 50"
    cmd += " -binary 2"
    cmd += " -vocab-file output/vocab.cj_001"
    cmd += " -verbose 0"
    return cmd

def fill_shuffle_command(input_filename, output_filename):
    cmd = "build/shuffle -memory 4.0 -verbose 0"
    cmd += " < " + input_filename
    cmd += " > " + output_filename
    return cmd

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
            co_output_filename = "exp_sr_" + sentence_rate + "_cj_" + cjglo + ".co"
            co_cmd = fill_bi_cooccur_command(sentence_rate, cjglo, co_output_filename)
            print co_cmd
            os.popen(co_cmd)

            shuf_output_filename = "exp_sr_" + sentence_rate + "_cj_" + cjglo + ".shuf"
            shuf_cmd = fill_shuffle_command(co_output_filename, shuf_output_filename)
            print shuf_cmd
            os.popen(shuf_cmd)
            
            glove_output_filename = "exp_sr_" + sentence_rate + "_cj_" + cjglo + ".vec"
            glove_cmd = fill_glove_command(shuf_output_filename, glove_output_filename)
            print glove_cmd
            os.popen(glove_cmd)

def main():
    sentence_rate_list = ["1"]
    cjglo_list = ["0"]
    run_by_list(sentence_rate_list, cjglo_list)


if __name__ == '__main__':
    main()