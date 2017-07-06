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
#include "hash_mapping_table.h"

MAPTABREC **k2sc, **sc2k;

/* Create hash table, initialise ptrs to NULL */
MAPTABREC ** init_hash_mapping_table() {
    int i;
    MAPTABREC **ht;
    ht = (MAPTABREC **) malloc( sizeof(MAPTABREC *) * M_SIZE );
    for(i = 0; i < M_SIZE; i++) {
        ht[i] = (MAPTABREC *) NULL;
    }
    return(ht);
}

/* Search hash table for given string, return record if found, else NULL */
MAPTABREC * hash_search_mapping_table(MAPTABREC **ht, char *w) {
    MAPTABREC *htmp, *hprv;
    unsigned int hval = M_HASHFN(w, M_SIZE, M_SEED);

    for( hprv = NULL, htmp=ht[hval]
        ; htmp != NULL && scmp(htmp->original, w) != 0
        ; hprv = htmp, htmp = htmp->next )
    {
    ;
    }

    if( hprv!=NULL ) {
        /* move to front on access */
        hprv->next = htmp->next;
        htmp->next = ht[hval];
        ht[hval] = htmp;
    }

    return(htmp);
}


/* Search hash table for given string, insert if not found */
void hash_insert_mapping_table(MAPTABREC **ht, char *original, char *corresponding) {
    MAPTABREC *htmp, *hprv;
    unsigned int hval = M_HASHFN(original, M_SIZE, M_SEED);

    for( hprv = NULL, htmp=ht[hval]
        ; htmp != NULL && scmp(htmp->original, original) != 0
        ; hprv = htmp, htmp = htmp->next ) 
    {
    ;
    }

    if(htmp == NULL) {
        htmp = (MAPTABREC *) malloc( sizeof(MAPTABREC) );
        //htmp->word = (char *) malloc( strlen(w) + 1 );
        strcpy(htmp->original, original);
        strcpy(htmp->corresponding, corresponding);
        htmp->next = NULL;
        if(hprv == NULL) {
            ht[hval] = htmp;
        }
        else {
            hprv->next = htmp;
        }
        /* new records are not moved to front */
    }
    else {
        if(hprv != NULL) {
            /* move to front on access */
            hprv->next = htmp->next;
            htmp->next = ht[hval];
            ht[hval] = htmp;
        }
    }
    return;
}

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
    char original[4], corresponding[22];
    // MAPTABREC *record;
    MAPTABREC **table;
    table = init_hash_mapping_table();

    f = fopen(filename, "rb");
    for (i = 0; i < table_size; i++) {      
        // record = (MAPTABREC *)malloc( sizeof(MAPTABREC) );
        get_characters(original, f);
        get_characters(corresponding, f);
        hash_insert_mapping_table(table, original, corresponding);
    }
    fclose(f);


    return table;
}

/**
 * Read 2 mapping tables
 */
void load_mapping_tables() {
    sc2k = load_one_mapping_table(SC2K_FILENAME, SC2K_SIZE);
    k2sc = load_one_mapping_table(K2SC_FILENAME, K2SC_SIZE);
}

// void test_mapping_table_1(index) {
//     int result;

//     result = BinarySearchTable(sc2k, sc2k[index]->original, 0, sc2k_size - 1);
//     fprintf(stderr, "result = %d\n", result);

//     result = BinarySearchTable(k2sc, k2sc[index]->original, 0, k2sc_size - 1);
//     fprintf(stderr, "result = %d\n", result);
// }

// void test_mapping_table_2() {
//     int result;

//     result = BinarySearchTable(sc2k, sc2k[sc2k_size - 1]->original, 0, sc2k_size - 1);
//     fprintf(stderr, "result = %d (%d)\n", result, sc2k_size - 1);

//     result = BinarySearchTable(k2sc, k2sc[k2sc_size - 1]->original, 0, k2sc_size - 1);
//     fprintf(stderr, "result = %d (%d)\n", result, k2sc_size - 1);
// }

// void test() {
//     test_mapping_table_1(0);
//     test_mapping_table_1(7);
//     test_mapping_table_1(77);
//     test_mapping_table_1(777);
//     test_mapping_table_1(5000);
//     test_mapping_table_2();
// }

int main(int argc, char **argv) {
    load_mapping_tables();
    // test();
}

