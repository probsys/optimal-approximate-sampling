// Sample from distribution data structures.
// ** @author: fsaad@mit.edu

#include <stdbool.h>
#include <stdlib.h>

#include "flip.h"
#include "sample.h"
#include "sstructs.h"

int sample_ky_encoding(struct sample_ky_encoding_s *x) {

    if (x->encoding.length == 1) {
        return 1;
    }

    int *enc = x->encoding.a;
    int c = 0;
    while (true) {
        int b = flip();
        c = enc[c+b];
        if (enc[c] < 0) {
            return -enc[c];
        }
    }
}

int sample_ky_matrix(struct sample_ky_matrix_s *x) {
    if (x->P.nrows == 1) {
        return 1;
    }

    int **P = x->P.P;
    int c = 0;
    int d = 0;

    while (true) {
        int b = flip();
        d = 2 * d + (1-b);
        for (int r = 0; r < x->P.nrows; r++) {
            d = d - P[r][c];
            if (d == - 1) {
                return r + 1;
            }
        }
        if (c == x->k - 1) {
            c = x->l;
        } else {
            c = c + 1;
        }
    }
}

int sample_ky_matrix_cached(struct sample_ky_matrix_cached_s *x) {
    if (x->T.nrows == 1) {
        return 1;
    }

    int **T = x->T.P;
    int *h = x->h.a;

    int c = 0;
    int d = 0;

    while (true) {
        int b = flip();
        d = 2 * d + (1-b);
        if (d < h[c]) {
            return T[d][c] + 1;
        }
        d = d - h[c];
        if (c == x->k - 1) {
            c = x->l;
        } else {
            c = c + 1;
        }
    }
}
