// Loading sampling data structures from disk.
// ** @author: fsaad@mit.edu

#ifndef READIO_H
#define READIO_H

#include <stdio.h>
#include "sstructs.h"

struct matrix_s load_matrix(FILE *fp);
struct array_s load_array(FILE *fp);
struct sample_ky_encoding_s read_sample_ky_encoding(char *fname);
struct sample_ky_matrix_s read_sample_ky_matrix(char *fname);
struct sample_ky_matrix_cached_s read_sample_ky_matrix_cached(char *fname);

void free_matrix_s(struct matrix_s x);
void free_array_s(struct array_s x);
void free_sample_ky_encoding_s(struct sample_ky_encoding_s x);
void free_sample_ky_matrix_s(struct sample_ky_matrix_s x);
void free_sample_ky_matrix_cached_s(struct sample_ky_matrix_cached_s x);

#endif
