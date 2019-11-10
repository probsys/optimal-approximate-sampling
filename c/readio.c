// Loading sampling data structures from disk.
// ** @author: fsaad@mit.edu

#include <stdlib.h>

#include "readio.h"
#include "sstructs.h"

// Load matrix from file.
struct matrix_s load_matrix(FILE *fp) {

    struct matrix_s mat;
    fscanf(fp, "%d %d", &(mat.nrows), &(mat.ncols));

    mat.P = (int **) calloc(mat.nrows, sizeof(int **));
    for(int r = 0; r < mat.nrows; ++r) {
        mat.P[r] = (int *) calloc(mat.ncols, sizeof(int));
        for (int c = 0; c < mat.ncols; ++c){
            fscanf(fp, "%d", &(mat.P[r][c]));
        }
    }

    return mat;
}

void free_matrix_s (struct matrix_s x) {
    for (int i = 0; i < x.nrows; i++) {
        free(x.P[i]);
    }
    free(x.P);
}

// Load matrix from file.
struct array_s load_array(FILE *fp) {

    struct array_s arr;
    fscanf(fp, "%d", &(arr.length));

    arr.a = (int *) calloc(arr.length, sizeof(int));
    for (int i = 0; i < arr.length; i++) {
        fscanf(fp, "%d", &arr.a[i]);
    }

    return arr;
}

void free_array_s (struct array_s x) {
    free(x.a);
}

// Load sample_ky_encoding data structure from file path.
struct sample_ky_encoding_s read_sample_ky_encoding(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_ky_encoding_s x;
    fscanf(fp, "%d %d", &(x.n), &(x.k));
    x.encoding = load_array(fp);

    fclose(fp);
    return x;
}

void free_sample_ky_encoding_s (struct sample_ky_encoding_s x) {
    free_array_s(x.encoding);
}

// Load sample_ky_matrix data structure from file path.
struct sample_ky_matrix_s read_sample_ky_matrix(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_ky_matrix_s x;
    fscanf(fp, "%d %d", &(x.k), &(x.l));
    x.P = load_matrix(fp);

    fclose(fp);
    return x;
}

void free_sample_ky_matrix_s (struct sample_ky_matrix_s x) {
    free_matrix_s(x.P);
}

// Load sample_ky_matrix_cached data structure from file path.
struct sample_ky_matrix_cached_s read_sample_ky_matrix_cached(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_ky_matrix_cached_s x;
    fscanf(fp, "%d %d", &(x.k), &(x.l));
    x.h = load_array(fp);
    x.T = load_matrix(fp);

    fclose(fp);
    return x;
}

void free_sample_ky_matrix_cached_s (struct sample_ky_matrix_cached_s x) {
    free_array_s(x.h);
    free_matrix_s(x.T);
}
