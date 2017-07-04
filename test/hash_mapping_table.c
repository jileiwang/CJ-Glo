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





/* Create hash table, initialise ptrs to NULL */
HASHREC **
inithashtable()
{
    int     i;
    HASHREC     **ht;

    ht = (HASHREC **) malloc( sizeof(HASHREC *) * TSIZE );

    for( i=0 ; i<TSIZE ; i++ )
    ht[i] = (HASHREC *) NULL;

    return(ht);
}


/* Search hash table for given string, return record if found, else NULL */
HASHREC *
hashsearch(HASHREC **ht, char *w)
{
    HASHREC *htmp, *hprv;
    unsigned int hval = HASHFN(w, TSIZE, SEED);

    for( hprv = NULL, htmp=ht[hval]
        ; htmp != NULL && scmp(htmp->word, w) != 0
        ; hprv = htmp, htmp = htmp->next )
    {
    ;
    }

    if( hprv!=NULL ) /* move to front on access */
    {
    hprv->next = htmp->next;
    htmp->next = ht[hval];
    ht[hval] = htmp;
    }

    return(htmp);
}


/* Search hash table for given string, insert if not found */
void
hashinsert(HASHREC **ht, char *w)
{
    HASHREC *htmp, *hprv;
    unsigned int hval = HASHFN(w, TSIZE, SEED);

    for( hprv = NULL, htmp=ht[hval]
        ; htmp != NULL && scmp(htmp->word, w) != 0
        ; hprv = htmp, htmp = htmp->next )
    {
    ;
    }

    if( htmp==NULL )
    {
    htmp = (HASHREC *) malloc( sizeof(HASHREC) );
    htmp->word = (char *) malloc( strlen(w) + 1 );
    strcpy(htmp->word, w);
    htmp->next = NULL;
    if( hprv==NULL )
        ht[hval] = htmp;
    else
        hprv->next = htmp;

    /* new records are not moved to front */
    }
    else
    {
    if( hprv!=NULL ) /* move to front on access */
    {
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

void insert_mapping_table_record(MAPTABREC **table, MAPTABREC *record) {

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
MAPTABREC ** ReadMappingTableFromFile(char *filename, int table_size) {
    int i;
    FILE *f;
    char *original, *corresponding;
    MAPTABREC *record;
    MAPTABREC **table;
    table = (MAPTABREC **)malloc( sizeof(MAPTABREC *) * HASH_MAPPING_TABLE_SIZE );

    f = fopen(filename, "rb");
    for (i = 0; i < table_size; i++) {      
        record = (MAPTABREC *)malloc( sizeof(MAPTABREC) );
        get_characters(record->original, f);
        get_characters(record->corresponding, f);
        insert_mapping_table_record(record);
    }
    fclose(f);


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
int BinarySearchTable(MAPTABREC **table, char *ch, int left, int right) {
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

