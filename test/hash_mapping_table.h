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
 * notice the type of a and b are (mapping_table **)
 */
int compare_original(const void *a, const void *b);

/**
 * Read one or several Kanji or Hanzi from text file
 */
int get_characters(char *word, FILE *fin);

/**
 * Read mapping table from file, and sort it
 */
MAPTABREC ** ReadMappingTableFromFile(char *filename, int table_size);

/**
 * Read 2 mapping tables from file
 */
void ReadMappingTable();

