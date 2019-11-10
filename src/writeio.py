# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

def write_array(array, f):
    n = len(array)
    f.write('%d ' % (n,))
    f.write(' '.join(map(str, array)))
    f.write('\n')

def write_matrix(matrix, f):
    nrow = len(matrix)
    ncol = len(matrix[0])
    f.write('%d %d\n' % (nrow, ncol))
    for row in matrix:
        f.write(' '.join(map(str, row)))
        f.write('\n')

def write_sample_ky_encoding(enc, n, k, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (n, k))
        write_array(enc, f)

def write_sample_ky_matrix(P, k, l, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (k, l))
        write_matrix(P, f)

def write_sample_ky_matrix_cached(k, l, h, T, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (k, l))
        write_array(h, f)
        write_matrix(T, f)
