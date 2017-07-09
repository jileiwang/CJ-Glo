
#include <stdio.h>
#include "hash_mapping_table.h"

void test_mapping_table_1() {
    int result;

    result = has_common_character("国王", "国家", 0);
    fprintf(stderr, "result = %d\n", result);

    result = has_common_character("国王", "国家", 1);
    fprintf(stderr, "result = %d\n", result);

}

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
    test_mapping_table_1();
}