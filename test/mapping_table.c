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


typedef struct mapping_table {
  //char *original;
  char original[4];
  // at most 7 corresponding characters
  //char *corresponding;//
  char corresponding[22];
} mapping_table;

mapping_table **k2sc, **sc2k;


char *sc2k_filename = "../data/simplec2kanji.txt";
char *k2sc_filename = "../data/kanji2simplec.txt";

int sc2k_size = 5006;
int k2sc_size = 5787;

int debug_counter = 0;



int compare_original_2(const void *a, const void *b) {
    int t = strcmp(((mapping_table *)a)->original, ((mapping_table *)b)->original);
    fprintf(stderr, "%s %s %d\n", ((mapping_table *)a)->original, ((mapping_table *)b)->original, t);
    scanf("%d", &t);
    return strcmp(((mapping_table *)a)->original, ((mapping_table *)b)->original);
}

int compare_original(mapping_table *a, mapping_table *b) {
    int t;
    if (debug_counter < 7) {
        t = strcmp(a->original, b->original);
        fprintf(stderr, "%s %s %x %x %d\n", a->original, b->original, a, b, t);
        scanf("%d", &t);
        debug_counter++;
    }
    return strcmp(a->original, b->original);
}

int get_characters(char *word, FILE *fin) {
    int i = 0, ch;
    while (!feof(fin)) {
        ch = fgetc(fin);
        //if (ch == 13) continue;
        if ((ch == ' ') || (ch == '\t') || (ch == '\n')) {
            break;
        }
        word[i++] = ch;
        //if (i >= MAX_STRING_LENGTH - 1) i--;   // truncate words that exceed max length
    }
    word[i] = 0;
    return i;
}


mapping_table ** ReadMappingTableFromFile(char *filename, int table_size) {
    int i;
    FILE *f;
    char *original, *corresponding;
    mapping_table *table_record;
    mapping_table **table;
    table = (mapping_table **)malloc( sizeof(mapping_table *) * table_size );

    f = fopen(filename, "rb");
    for (i = 0; i < table_size; i++) {
// for char * original.
        // table_record = (mapping_table *)malloc( sizeof(mapping_table));
        // table_record->original = (char *)malloc( sizeof(char) * 30);
        // if (i % 700 == 0) fprintf(stderr, "table_record->original %p\n", table_record->original);
        // table_record->corresponding = (char *)malloc( sizeof(char) * 50);
        // get_characters(table_record->original, f);
        // get_characters(table_record->corresponding, f);
        // //table_record->original = original;
        // //table_record->corresponding = corresponding;
        // table[i] = table_record;
        // if (i % 700 == 0) fprintf(stderr, "%d %s %s %p %p %p\n", i, table[i]->original, table[i]->corresponding, table[i]->original, table[i]->corresponding, table[i]);
// for char original[4]         
        table_record = (mapping_table *)malloc( sizeof(mapping_table) );
        get_characters(table_record->original, f);
        get_characters(table_record->corresponding, f);
        //table_record->original = original;
        //table_record->corresponding = corresponding;
        table[i] = table_record;
        if (i % 700 == 0) fprintf(stderr, "%d %s %s %p %p %p\n", i, table[i]->original, table[i]->corresponding, table[i]->original, table[i]->corresponding, table[i]);

    }
    fclose(f);

    fprintf(stderr, "ReadMappingTableFromFile - table %p, table[7] %p, table[7]->original %p\n", table, table[7], table[7]->original);

    for (i = 0; i < sc2k_size; i += 700) {
        fprintf(stderr, "%d ", i);
        fprintf(stderr, "%p %p\n", table[i]->original, table[i]->corresponding);//, table[i]->original, table[i]->corresponding);
    }

    fprintf(stderr, "---  %p %p %p %p %p\n", table, &table[0], table[0], table[1], table[2]);
    
    // TODO the bug is because the usage of qsort!!!!!!!===============
    qsort(&table[0], table_size, sizeof(mapping_table*), compare_original);

    fprintf(stderr, "ReadMappingTableFromFile - table %p, table[7] %p, table[7]->original %p\n", table, table[7], table[7]->original);

    for (i = 0; i < sc2k_size; i += 700) {
        fprintf(stderr, "%d ", i);
        fprintf(stderr, "%p %p\n", table[i]->original, table[i]->corresponding);//, table[i]->original, table[i]->corresponding);
    }

    return table;
}



void ReadMappingTable() {
    sc2k = ReadMappingTableFromFile(sc2k_filename, sc2k_size);
    k2sc = ReadMappingTableFromFile(k2sc_filename, k2sc_size);
}


int BinarySearchTable(mapping_table **table, char *ch, int left, int right) {
    int mid, cmp;
    if (right < left) {
        return -1;
    }
    mid = left + (right - left) / 2;
    fprintf(stderr, "mid = %d, %s\n", mid, table[mid]->original);
    
    //cmp = strcmp(ch, table[mid]->original);
    
    cmp = strcmp(table[mid]->original, ch);


//int compare_original(const void *a, const void *b) {
//    return strcmp(((struct mapping_table *)a)->original, ((struct mapping_table *)b)->original);
//}
    if (cmp == 0) {
        return mid;
    }
    else if (cmp < 0) {
        return BinarySearchTable(table, ch, left, mid - 1);
    }
    else {
        return BinarySearchTable(table, ch, mid + 1, right);
    }
}



int test_mapping_table_1() {
    int i, result;
    fprintf(stderr, "test_mapping_table_1\n");
    sc2k = ReadMappingTableFromFile(sc2k_filename, sc2k_size);
    fprintf(stderr, "After ReadMappingTableFromFile\n");
    //fprintf(stderr, "%p\n", sc2k);
    fprintf(stderr, "table %p, table[7] %p, table[7]->original %p\n", sc2k, sc2k[7], sc2k[7]->original);
    for (i = 0; i < sc2k_size; i++) {
        if (i % 700 == 0) fprintf(stderr, "%d ", i);
        if (i % 700 == 0) fprintf(stderr, "%p %p\n", sc2k[i]->original, sc2k[i]->corresponding);
        printf("%s %s %p %p %p\n", sc2k[i]->original, sc2k[i]->corresponding, sc2k[i]->original, sc2k[i]->corresponding, sc2k[i]);
    }
    result = BinarySearchTable(sc2k, sc2k[7]->original, 0, sc2k_size - 1);
    fprintf(stderr, "result = %d\n", result);

}



int main(int argc, char **argv) {
    test_mapping_table_1();
}

