// Flipping a coin.
// ** @author: fsaad@mit.edu

#include <stdlib.h>

#include "flip.h"

unsigned long NUM_RNG_CALLS = 0;

// RAND_MAX is 2**31-1, so bits are 0,...30
static int k = 31;
static int flip_word = 0;
static int flip_pos = 0;

int flip(void){
    if (flip_pos == 0) {
        NUM_RNG_CALLS++;
        flip_word = rand();
        flip_pos = k;
    }
    --flip_pos;
    return (flip_word >> flip_pos) & 1;
}

int randint(int k) {
    int n = 0;

    for (int i = 0; i < k; i++) {
        int b = flip();
        n <<= 1;
        n += b;
    }

    return n;
}
