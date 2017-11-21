from collections import defaultdict

"""
    The input file is download from:
      
    http://lotus.kuee.kyoto-u.ac.jp/~chu/pubdb/LREC2012/kanji_mapping_table.txt

    Removed the introduction text in the head, only character triples remained
    in input file.
"""


def check_kanji_length():
    """
        Checked by this function, the first item of each triple is excatly one
        Kanji charachter.
    """
    fin = open('data/kanji_mapping_table_clean.txt', 'r')
    for line in fin:
        triple = line.split()
        kanji = triple[0]
        if len(kanji) != 3:
            print kanji, len(kanji)
            break

def check_duplicated_kanji():
    """
        Checked by this function, No duplicated Kanjis in this mapping table's
        first column
    """
    fin = open('data/kanji_mapping_table_clean.txt', 'r')
    kanji_set = set()
    for line in fin:
        triple = line.split()
        kanji = triple[0]
        if kanji in kanji_set:
            print kanji
            break
        kanji_set.add(kanji)
    print "There are", len(kanji_set), "Kanjis in the mapping table."

def write_tuple_to_file(tuple, filename):
    fout = open(filename, 'w')
    for kanji, simple_chinese in tuple:
        fout.write("%s %s\n" % (kanji, simple_chinese))
    fout.close()

def kanji_2_simple_chinese():
    """
        Result:
        There are 569 N/A, 5205 single corresponding Simple Chinese 
        charachters, 582 mutiple corresponding Simple Chinese charachters,
        in total 6356 lines.
        A Kanji Character is mapping to X Simple Chinese Character:
        {0: 569, 1: 5205, 2: 538, 3: 41, 4: 1, 6: 2}
    """
    fin = open('data/kanji_mapping_table_clean.txt', 'r')
    single_result = []
    mutiple_result = []
    single = 0
    mutiple = 0
    na = 0
    dic = {}
    for line in fin:
        triple = line.split()
        kanji = triple[0]
        simple_chinese = triple[2]
        if simple_chinese == 'N/A':
            na += 1
        elif len(simple_chinese) <= 3:
            single += 1
            single_result.append((kanji, simple_chinese))
        else:
            mutiple += 1
            simple_chinese = ''.join(simple_chinese.split(','))
            mutiple_result.append((kanji, simple_chinese))
            key = len(simple_chinese) / 3
            dic[key] = dic.get(key, 0) + 1

    # write_tuple_to_file(single_result, "output/mapping_table/single_01.txt")
    # write_tuple_to_file(mutiple_result, "output/mapping_table/mutiple_01.txt")

    result = single_result + mutiple_result
    result.sort()
    write_tuple_to_file(result, "output/mapping_table/kanji2simplec.txt")

    print "There are", na, "N/A,", 
    print single, "single corresponding Simple Chinese charachters,",
    print mutiple, "mutiple corresponding Simple Chinese charachters,",
    print "in total", (na + single + mutiple), "lines."

    dic[0] = na
    dic[1] = single
    print "A Kanji Character is mapping to X Simple Chinese Character:"
    print dic

def simple_chinese_2_kanji():
    """
        A Simple Chinese Character is mapping to X Kanji Character:
        {1: 3873, 2: 903, 3: 189, 4: 34, 5: 5, 6: 1, 7: 1}
    """
    fin = open('data/kanji_mapping_table_clean.txt', 'r')
    dic = defaultdict(list)
    for line in fin:
        triple = line.split()
        kanji = triple[0]
        simple_chinese = triple[2]
        if simple_chinese == 'N/A':
            continue
        elif len(simple_chinese) <= 3:
            dic[simple_chinese].append(kanji)
        else:
            for character in simple_chinese.split(','):
                dic[character].append(kanji)

    result = [(x, ''.join(y)) for x, y in dic.items()]
    result.sort()
    write_tuple_to_file(result, "output/mapping_table/simplec2kanji.txt")
    
    dic2 = defaultdict(int)
    for key in dic:
        dic2[len(dic[key])] += 1

    print "A Simple Chinese Character is mapping to X Kanji Character:"
    print dic2

def find_same_shape_character():
    """
        The shape of a common character in 3 categories are sometimes the same, sometimes not.
        Only consider lines without "N/A", there are 5 patterns:
        Type   Kanji           Tranditional    Simple
        0      A               A               A
        1      A               A               B
        2      A               B               A
        3      A               B               B
        4      A               B               C

        This function counts these types, and save to corresponding files.
    """
    fin = open('data/kanji_mapping_table_clean.txt', 'r')
    dic = defaultdict(list)

    type_set = [[] for _ in xrange(6)] # Type 5 is 'N/A'

    for line in fin:
        triple = line.split()
        if 'N/A' in triple:
            type_set[5].append(line)
            continue
        kanji = triple[0]
        tranditional = triple[1]
        simple = triple[2]
        for c_kanji in kanji.split(','):
            for c_tranditional in tranditional.split(','):
                for c_simple in simple.split(','):
                    if c_kanji == c_tranditional and c_kanji == c_simple:
                        type_set[0].append(line)
                    elif c_kanji == c_tranditional:
                        type_set[1].append(line)
                    elif c_kanji == c_simple:
                        type_set[2].append(line)
                    elif c_tranditional == c_simple:
                        type_set[3].append(line)
                    else:
                        type_set[4].append(line)

    for i in xrange(6):
        fout = open("output/mapping_table/character_shape_type_%i.txt" % i, "w")
        for line in type_set[i]:
            fout.write(line)
        fout.close()

def find_same_shape_character_single():
    """
        Same with find_same_shape_character(), but only deal with line that in each type
        there is only 1 character. 
    """
    fin = open('data/kanji_mapping_table_clean.txt', 'r')
    dic = defaultdict(list)

    type_set = [[] for _ in xrange(6)] # Type 5 is line with ','

    for line in fin:
        if ',' in line:
            type_set[5].append(line)
            continue
        triple = line.split()
        if 'N/A' in triple:
            continue
        c_kanji = triple[0]
        c_tranditional = triple[1]
        c_simple = triple[2]
        if c_kanji == c_tranditional and c_kanji == c_simple:
            type_set[0].append(line)
        elif c_kanji == c_tranditional:
            type_set[1].append(line)
        elif c_kanji == c_simple:
            type_set[2].append(line)
        elif c_tranditional == c_simple:
            type_set[3].append(line)
        else:
            type_set[4].append(line)

    for i in xrange(6):
        fout = open("output/mapping_table/character_shape_type_single_%i.txt" % i, "w")
        for line in type_set[i]:
            fout.write(line)
        fout.close()

if __name__ == '__main__':
    # check_kanji_length()
    # check_duplicated_kanji()
    # kanji_2_simple_chinese()
    # simple_chinese_2_kanji()
    # find_same_shape_character()
    find_same_shape_character_single()

