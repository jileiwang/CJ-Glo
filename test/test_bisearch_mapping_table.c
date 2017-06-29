
#include <stdio.h>
#include "bisearch_mapping_table.h"

/*
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
*/

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