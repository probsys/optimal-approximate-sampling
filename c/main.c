// Main harness for C samplers.
// ** @author: fsaad@mit.edu

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "flip.h"
#include "readio.h"
#include "sample.h"
#include "sstructs.h"

#include "macros.c"

int main(int argc, char **argv) {
    // Read command line arguments.
    if (argc != 5) {
        printf("usage: ./mainc seed steps sampler path\n");
        exit(0);
    }
    int seed = atoi(argv[1]);
    int steps = atoi(argv[2]);
    char *sampler = argv[3];
    char *path = argv[4];

    printf("%d %d %s %s\n", seed, steps, sampler, path);
    srand(seed);

    int x = 0;
    clock_t t;
    READ_SAMPLE_TIME("ky.enc",
        sampler,
        sample_ky_encoding_s,
        read_sample_ky_encoding,
        sample_ky_encoding,
        free_sample_ky_encoding_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("ky.mat",
        sampler,
        sample_ky_matrix_s,
        read_sample_ky_matrix,
        sample_ky_matrix,
        free_sample_ky_matrix_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("ky.matc",
        sampler,
        sample_ky_matrix_cached_s,
        read_sample_ky_matrix_cached,
        sample_ky_matrix_cached,
        free_sample_ky_matrix_cached_s,
        path, steps, t, x)
    else {
        printf("Unknown sampler: %s\n", sampler);
        exit(1);
    }

    double e = ((double)t) / CLOCKS_PER_SEC;
    printf("%s %1.5f %ld\n", sampler, e, NUM_RNG_CALLS);

    return 0;
}
