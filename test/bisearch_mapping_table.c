//  Tool to calculate word-word cooccurrence statistics for sentence aligned
//  corpus of 2 languages.
//
//  Copyright (c) 2014 The Board of Trustees of
//  The Leland Stanford Junior University. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//
//
//  For more information, bug reports, fixes, contact:
//    Jilei Wang (wangjileiRUC@gmail.com)


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


typedef struct mapping_table_record {
  char original[4];
  // at most 7 corresponding characters
  char corresponding[22];
} MAPTABREC;

MAPTABREC **k2sc, **sc2k;


char *sc2k_filename = "../data/simplec2kanji.txt";
char *k2sc_filename = "../data/kanji2simplec.txt";

int sc2k_size = 5006;
int k2sc_size = 5787;



/**
 * Compare 2 mapping table record, used in qsort function.
 * notice the type of a and b are (MAPTABREC **)
 */
int compare_original(const void *a, const void *b) {
    return strcmp((*(MAPTABREC **)a)->original, (*(MAPTABREC **)b)->original);
}

/**
 * Read one or several Kanji or Hanzi from text file
 */
int get_characters(char *word, FILE *fin) {
    int i = 0, ch;
    while (!feof(fin)) {
        ch = fgetc(fin);
        if ((ch == ' ') || (ch == '\t') || (ch == '\n')) {
            break;
        }
        word[i++] = ch;
    }
    word[i] = 0;
    return i;
}

/**
 * Read mapping table from file, and sort it
 */
MAPTABREC ** load_one_mapping_table(char *filename, int table_size) {
    int i;
    FILE *f;
    char *original, *corresponding;
    MAPTABREC *table_record;
    MAPTABREC **table;
    table = (MAPTABREC **)malloc( sizeof(MAPTABREC *) * table_size );

    f = fopen(filename, "rb");
    for (i = 0; i < table_size; i++) {      
        table[i] = (MAPTABREC *)malloc( sizeof(MAPTABREC) );
        get_characters(table[i]->original, f);
        get_characters(table[i]->corresponding, f);
    }
    fclose(f);

    qsort(&table[0], table_size, sizeof(MAPTABREC*), compare_original);

    return table;
}

/**
 * Read 2 mapping tables
 */
void load_mapping_tables() {
    sc2k = load_one_mapping_table(sc2k_filename, sc2k_size);
    k2sc = load_one_mapping_table(k2sc_filename, k2sc_size);
}

/**
 * Binary Search a character from the mapping table
 */
int bisearch_table(MAPTABREC **table, char *ch, int left, int right) {
    int mid, cmp;
    if (right < left) {
        return -1;
    }
    mid = left + (right - left) / 2;
    
    cmp = strcmp(table[mid]->original, ch);

    if (cmp == 0) {
        return mid;
    }
    else if (cmp > 0) {
        return bisearch_table(table, ch, left, mid - 1);
    }
    else {
        return bisearch_table(table, ch, mid + 1, right);
    }
}

int compare_characters(char *corresponding, char *word2) {
  int len1, len2, i, j;
  len1 = strlen(corresponding);
  len2 = strlen(word2);
  for (i = 0; i < len1; i+= 3) {
    for (j = 0; j < len2; j += 3) {
      if (word2[j] == corresponding[i] && word2[j+1] == corresponding[i+1] && word2[j+2] == corresponding[i+2]) {
        //if (verbose > 2) fprintf(stderr, "source_ch %s, target_ch %s, j %d, word2 %s\n", source_ch, target_ch, j, word2);
        return 1;
      }
    }
  }
  return 0;
}

/**
 * return 1 if the 2 words has a common character.
 */
int has_common_character(char *word1, char *word2, int lang_id) {
  char source_ch[4], target_ch[4];
  int len1, len2;
  int i, j, pos, table_size;
  int parallel = 1 - lang_id;
  MAPTABREC **table;

  if (lang_id == 1) {
    table = sc2k;
    table_size = sc2k_size;
  }
  else {
    table = k2sc;
    table_size = k2sc_size;
  }

  len1 = strlen(word1);
  len2 = strlen(word2);
  if (len1 % 3 != 0 || len2 % 3 != 0) {
    return 0;
  }
  // if (verbose > 2) fprintf(stderr, "CJWordMatch : %s - %s - %d\n", word1, word2, lang_id);
  source_ch[3] = 0;
  target_ch[3] = 0;
  for (i = 0; i < len1; i += 3) {
    // get a character from word1
    for (j = 0; j < 3; j++) {
      source_ch[j] = word1[i + j];
    }
    pos = bisearch_table(table, source_ch, 0, table_size - 1);
    if (pos >= 0) {
        if (compare_characters(table[pos]->corresponding, word2) > 0) {
            return 1;
        }
    }
  }
  return 0;
}

void test_mapping_table_1(index) {
    int result;

    result = bisearch_table(sc2k, sc2k[index]->original, 0, sc2k_size - 1);
    fprintf(stderr, "result = %d\n", result);

    result = bisearch_table(k2sc, k2sc[index]->original, 0, k2sc_size - 1);
    fprintf(stderr, "result = %d\n", result);
}

void test_mapping_table_2() {
    int result;

    result = bisearch_table(sc2k, sc2k[sc2k_size - 1]->original, 0, sc2k_size - 1);
    fprintf(stderr, "result = %d (%d)\n", result, sc2k_size - 1);

    result = bisearch_table(k2sc, k2sc[k2sc_size - 1]->original, 0, k2sc_size - 1);
    fprintf(stderr, "result = %d (%d)\n", result, k2sc_size - 1);
}

void test_search() {
    test_mapping_table_1(0);
    test_mapping_table_1(7);
    test_mapping_table_1(77);
    test_mapping_table_1(777);
    test_mapping_table_1(5000);
    test_mapping_table_2();
}

void test_mapping() {

    int result;

    result = has_common_character("樱花", "桜がさく", 1);
    fprintf(stderr, "樱花 - 桜がさく, result = %d\n", result);

    result = has_common_character("桜がさく", "樱花", 2);
    fprintf(stderr, "桜がさく - 樱花, result = %d\n", result);

    result = has_common_character("国家", "桜がさく", 1);
    fprintf(stderr, "国家 - 桜がさく, result = %d\n", result);

    result = has_common_character("国家", "王国", 2);
    fprintf(stderr, "国家 - 王国, result = %d\n", result);
}

int main(int argc, char **argv) {
    load_mapping_tables();
    test_mapping();
}

