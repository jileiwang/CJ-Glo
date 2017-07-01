from collections import defaultdict
import codecs

def count(corpus, output_file):
    debug = False
    dic = defaultdict(int)
    other = set()
    fout = codecs.open(output_file, 'w', 'utf8')
    for line in open(corpus, 'r'):
        words = line.split()
        for word in words:
            if len(word) % 3 == 0:
                for i in xrange(len(word) / 3):
                    dic[word[i:i+3]] += 1
            else:
                other.add(word)
    fout.write('%i %i\n' % (len(dic), len(other)))
    
    record_list = [(y, x) for x, y in dic.items()]
    record_list.sort()
    record_list.reverse()
    i = 0
    for x, y in record_list:
        #print y.decode('utf8'), x
        try:
            yy = y.decode('GBK')
        except:
            print y
            yy = 'N/A'
        fout.write('%s %i\n' % (yy, x))
        i += 1
        if i > 10 and debug:
            break

    other_list = list(other)
    other_list.sort()
    for item in other_list:
        #print item.decode('utf8')
        item2 = item.decode('utf8')
        fout.write(item2)
        fout.write('\n')
        i += 1
        if i > 20 and debug:
            break
    fout.close()

if __name__ =='__main__':
    count('data/train.zh_parsed', 'output/count.zh')
    count('data/train.ja_parsed', 'output/count.ja')
