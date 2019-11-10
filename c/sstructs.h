// Defining structs for samplers..
// ** @author: fsaad@mit.edu

#ifndef SSTRUCTS_H
#define SSTRUCTS_H

#include <stdlib.h>
#include <stdio.h>

// matrix
struct matrix_s {
    int nrows;
    int ncols;
    int **P;
};

// array
struct array_s {
    int length;
    int *a;
};


// sample_ky_encoding
struct sample_ky_encoding_s {
    int n;
    int k;
    struct array_s encoding;
};

// sample_ky_matrix
struct sample_ky_matrix_s {
    int k;
    int l;
    struct matrix_s P;
};

// sample_ky_matrix_cached
struct sample_ky_matrix_cached_s {
    int k;
    int l;
    struct array_s h;
    struct matrix_s T;
};

#endif
