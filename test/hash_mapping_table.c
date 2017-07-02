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



/**
 * Compare 2 mapping table record, used in qsort function.
 * notice the type of a and b are (mapping_table **)
 */
int compare_original(const void *a, const void *b) {
    return strcmp((*(mapping_table **)a)->original, (*(mapping_table **)b)->original);
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
mapping_table ** ReadMappingTableFromFile(char *filename, int table_size) {
    int i;
    FILE *f;
    char *original, *corresponding;
    mapping_table *table_record;
    mapping_table **table;
    table = (mapping_table **)malloc( sizeof(mapping_table *) * table_size );

    f = fopen(filename, "rb");
    for (i = 0; i < table_size; i++) {      
        table[i] = (mapping_table *)malloc( sizeof(mapping_table) );
        get_characters(table[i]->original, f);
        get_characters(table[i]->corresponding, f);
    }
    fclose(f);

    //fprintf(stderr, "ReadMappingTableFromFile - table %p, table[7] %p, table[7]->original %p\n", table, table[7], table[7]->original);
    // fprintf(stderr, "=============== After Reading File ============\n");
    // fprintf(stderr, "&table=%p\n", table);
    // for (i = 0; i < sc2k_size; i++) {
    //     fprintf(stderr, "%d ", i);
    //     fprintf(stderr, "table[i]=%s, &table[i]=%p, &table[i]->original=%p\n", table[i]->original, table[i], table[i]->original);
    // }

    // TODO the bug is because the usage of qsort!!!!!!!===============
    qsort(&table[0], table_size, sizeof(mapping_table*), compare_original);

    // fprintf(stderr, "=============== After QSORT ============\n");
    // fprintf(stderr, "&table=%p\n", table);
    // for (i = 0; i < sc2k_size; i++) {
    //     fprintf(stderr, "%d ", i);
    //     fprintf(stderr, "table[i]=%s, &table[i]=%p, &table[i]->original=%p\n", table[i]->original, table[i], table[i]->original);
    // }

    // fprintf(stderr, "ReadMappingTableFromFile - table %p, table[7] %p, table[7]->original %p\n", table, table[7], table[7]->original);

    // for (i = 0; i < sc2k_size; i += 700) {
    //     fprintf(stderr, "%d ", i);
    //     fprintf(stderr, "%p %p\n", table[i]->original, table[i]->corresponding);//, table[i]->original, table[i]->corresponding);
    // }

    return table;
}

/**
 * Read 2 mapping tables
 */
void ReadMappingTable() {
    sc2k = ReadMappingTableFromFile(sc2k_filename, sc2k_size);
    k2sc = ReadMappingTableFromFile(k2sc_filename, k2sc_size);
}

/**
 * 
 */
int BinarySearchTable(mapping_table **table, char *ch, int left, int right) {
    int mid, cmp;
    if (right < left) {
        return -1;
    }
    mid = left + (right - left) / 2;
    fprintf(stderr, "mid = %d, %s\n", mid, table[mid]->original);
    
    cmp = strcmp(table[mid]->original, ch);

    if (cmp == 0) {
        return mid;
    }
    else if (cmp > 0) {
        return BinarySearchTable(table, ch, left, mid - 1);
    }
    else {
        return BinarySearchTable(table, ch, mid + 1, right);
    }
}

void test_mapping_table_1(index) {
    int result;

    result = BinarySearchTable(sc2k, sc2k[index]->original, 0, sc2k_size - 1);
    fprintf(stderr, "result = %d\n", result);

    result = BinarySearchTable(k2sc, k2sc[index]->original, 0, k2sc_size - 1);
    fprintf(stderr, "result = %d\n", result);
}

void test_mapping_table_2() {
    int result;

    result = BinarySearchTable(sc2k, sc2k[sc2k_size - 1]->original, 0, sc2k_size - 1);
    fprintf(stderr, "result = %d (%d)\n", result, sc2k_size - 1);

    result = BinarySearchTable(k2sc, k2sc[k2sc_size - 1]->original, 0, k2sc_size - 1);
    fprintf(stderr, "result = %d (%d)\n", result, k2sc_size - 1);
}

void test() {
    test_mapping_table_1(0);
    test_mapping_table_1(7);
    test_mapping_table_1(77);
    test_mapping_table_1(777);
    test_mapping_table_1(5000);
    test_mapping_table_2();
}

int main(int argc, char **argv) {
    ReadMappingTable();
    test();
}

