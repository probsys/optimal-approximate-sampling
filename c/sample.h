// Loading sampling data structures from disk.
// ** @author: fsaad@mit.edu

#ifndef SAMPLE_H
#define SAMPLE_H

#include "sstructs.h"

int sample_ky_encoding(struct sample_ky_encoding_s *x);
int sample_ky_matrix(struct sample_ky_matrix_s *x);
int sample_ky_matrix_cached(struct sample_ky_matrix_cached_s *x);
#endif
