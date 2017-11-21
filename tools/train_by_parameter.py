"""
    Train CJ-GLO model by different parameters, then test the result.
"""

import os

vocab_file = "output/vocab.cj_001"

glove_args_2 = {
    "threads": "8",
    "x-max": "10",
    "iter": "15",
    "vector-size": "50",
    "binary": "2",
    "vocab-file": vocab_file,
    "verbose": "0"
}

# used to find a good ctrl parameters
glove_args = {
    "threads": "16",
    "x-max": "100",
    "iter": "15",
    "vector-size": "100",
    "binary": "2",
    "vocab-file": vocab_file,
    "eta": "0.05",
    "verbose": "2",
    "alpha": "0.75"
}

def fill_glove_command(input_filename, output_filename):
    cmd = "build/glove -save-file output/" + output_filename
    cmd += " -input-file output/" + input_filename
    for args in glove_args:
        cmd += " -" + args + " " + glove_args[args]
    return cmd

shuffle_args_old = {
    "memory": "4.0",
    "verbose": "0"
}

shuffle_args = {
    "memory": "8.0",
    "verbose": "2"
}

def fill_shuffle_command(input_filename, output_filename):
    cmd = "build/shuffle"
    for args in shuffle_args:
        cmd += " -" + args + " " + shuffle_args[args]
    cmd += " < output/" + input_filename
    cmd += " > output/" + output_filename
    return cmd

def fill_bi_cooccur_command(window_size, sentence_rate, cjglo, cjglo_rate, output_filename):
    cmd = "build/bi_cooccur -verbose 0"
    cmd += " -corpus-file-1 data/train.zh_parsed"
    cmd += " -corpus-file-2 data/train.ja_parsed"
    cmd += " -window-size " + window_size
    cmd += " -vocab-file " + vocab_file
    cmd += " -sentence-rate " + sentence_rate
    cmd += " -cjglo " + cjglo
    cmd += " -cjglo-rate " + cjglo_rate
    cmd += " > output/" + output_filename
    return cmd

def fill_experiment2_command(word_vec_filename, output_filename):
    cmd = "python tools/experiment2.py --vocab_file " + vocab_file
    cmd += " --vectors_file output/" + word_vec_filename
    cmd += " > output/" + output_filename
    return cmd



def run_once(sentence_rate, cjglo, window_size, cjglo_rate, prefix):
    co_output_filename = prefix + ".co"
    co_cmd = fill_bi_cooccur_command(window_size, sentence_rate, cjglo, cjglo_rate, co_output_filename)
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

    word_vec_filename = prefix + ".vec.txt"
    experiment2_output_filename = prefix + ".exp2.txt"
    experiment2_cmd = fill_experiment2_command(word_vec_filename, experiment2_output_filename)
    print experiment2_cmd
    os.popen(experiment2_cmd)

    # clean tmp files
    print "rm -rf output/" + co_output_filename
    os.popen("rm -rf output/" + co_output_filename)
    print "rm -rf output/" + shuf_output_filename
    os.popen("rm -rf output/" + shuf_output_filename)


def run_control_by_list(prefix, sentence_rate_list):
    for sentence_rate in sentence_rate_list:
        control_prefix = prefix + "ctrl_s_" + sentence_rate
        run_once(sentence_rate, "0", "0", control_prefix)


def run_experiment_by_list(prefix, window_size_list, sentence_rate_list, cjglo_rate_list):
    for sentence_rate in sentence_rate_list:
        for cjglo_rate in cjglo_rate_list:
            for window_size in window_size_list:
                exp_prefix = prefix + "exp_w_" + window_size + "_s_" + sentence_rate + "_c_" + cjglo_rate
                run_once(sentence_rate, "1", window_size, cjglo_rate, exp_prefix)
            

def main():
    prefix = "batch_04/"
    sentence_rate_list = ["0.00", "0.01", "0.02", "0.03", "0.04", "0.05"] # [str(0.1 * x) for x in xrange(1, 11)]
    #sentence_rate_list = ["0.000", "0.001", "0.002", "0.003", "0.004", "0.005", "0.006", "0.007", "0.008", "0.009"]
    cjglo_rate_list = ["0.00", "0.01", "0.02", "0.03", "0.04", "0.05"] # [str(0.1 * x) for x in xrange(1, 11)]
    #cjglo_rate_list = ["0.000", "0.001", "0.002", "0.003", "0.004", "0.005", "0.006", "0.007", "0.008", "0.009"]
    #run_control_by_list(prefix, sentence_rate_list)
    window_size_list = ["5", "10"]
    run_experiment_by_list(prefix, window_size_list, sentence_rate_list, cjglo_rate_list)


if __name__ == '__main__':
    main()