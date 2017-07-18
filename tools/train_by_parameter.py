"""
    Train CJ-GLO model by different parameters, then test the result.
"""

import os

vocab_file = "output/vocab.cj_001"
vector_size = "50"

def fill_glove_command(input_filename, output_filename):
    cmd = "build/glove -save-file output/" + output_filename
    cmd += " -threads 8"
    cmd += " -input-file output/" + input_filename
    cmd += " -x-max 10"
    cmd += " -iter 15"
    cmd += " -vector-size " + vector_size
    cmd += " -binary 2"
    cmd += " -vocab-file " + vocab_file
    cmd += " -verbose 0"
    return cmd

def fill_shuffle_command(input_filename, output_filename):
    cmd = "build/shuffle -memory 4.0 -verbose 0"
    cmd += " < output/" + input_filename
    cmd += " > output/" + output_filename
    return cmd

def fill_bi_cooccur_command(sentence_rate, cjglo, cjglo_rate, output_filename):
    cmd = "build/bi_cooccur -verbose 0"
    cmd += " -corpus-file-1 data/train.zh_parsed"
    cmd += " -corpus-file-2 data/train.ja_parsed"
    cmd += " -vocab-file " + vocab_file
    cmd += " -sentence-rate " + sentence_rate
    cmd += " -cjglo " + cjglo
    cmd += " -cjglo-rate " + cjglo_rate
    cmd += " > output/" + output_filename
    return cmd

def run_once(sentence_rate, cjglo, cjglo_rate, prefix):
    co_output_filename = prefix + ".co"
    co_cmd = fill_bi_cooccur_command(sentence_rate, cjglo, cjglo_rate, co_output_filename)
    print co_cmd
    os.popen(co_cmd)

    shuf_output_filename = prefix + ".shuf"
    shuf_cmd = fill_shuffle_command(co_output_filename, shuf_output_filename)
    print shuf_cmd
    os.popen(shuf_cmd)

    glove_output_filename = prefix + ".vec"
    glove_cmd = fill_glove_command(shuf_output_filename, glove_output_filename)
    print glove_cmd
    os.popen(glove_cmd)


def run_control_by_list(sentence_rate_list):
    for sentence_rate in sentence_rate_list:
        control_prefix = "ctrl_s_" + sentence_rate
        run_once(sentence_rate, "0", "0", control_prefix)


def run_experiment_by_list(sentence_rate_list, cjglo_rate_list):
    for sentence_rate in sentence_rate_list:
        for cjglo_rate in cjglo_rate_list:
            exp_prefix = "exp_s_" + sentence_rate + "_c_" + cjglo_rate
            run_once(sentence_rate, "1", cjglo_rate, exp_prefix)
            

def main():
    sentence_rate_list = ["0.7"] # [str(0.1 * x) for x in xrange(1, 11)]
    cjglo_rate_list = ["0.7"] # [str(0.1 * x) for x in xrange(1, 11)]
    # run_control_by_list(sentence_rate_list)
    run_experiment_by_list(sentence_rate_list, cjglo_rate_list)


if __name__ == '__main__':
    main()