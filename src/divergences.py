# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

from math import log2
from math import sqrt

from collections import OrderedDict

try:
    import mpmath
    mpf = mpmath.mpf
    mplog2 = lambda x: mpmath.log(x, b=2)
    mpsqrt = mpmath.sqrt
except ImportError:
    mpf = float
    mplog = log2
    mpsqrt = sqrt

# ============================================================================
# Various f-divergences from the following sources
#   https://arxiv.org/pdf/math/0505238.pdf
#   https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7552457
#   https://arxiv.org/pdf/1309.3029.pdf

LABELS = OrderedDict([
    ('tv'         , 'Total Variation'),
    ('hellinger'  , 'Hellinger Divergence'),
    ('pchi2'      , 'Pearson Chi-Square'),
    ('nchi2'      , 'Neyman Chi-Square'),
    ('td'         , 'Triangular Discrimination'),
    ('kl'         , 'Relative Entropy'),
    ('reverse_kl' , 'Reverse Relative Entropy'),
    ('js'         , 'Jensen-Shannon'),
    ('jf'         , 'Jeffrey (Symmetric KL)'),
    ('mt'         , 'Matern'),
    ('alpha'      , 'Alpha Divergence'),
    ('x2'         , 'Quadratic'),
])


# Kernels expressed in direct form.

def kernel_tv(a, b):
    return 1/2 * abs(a-b)

def kernel_hellinger(a, b):
    return (sqrt(a) - sqrt(b))**2

def kernel_pchi2(a, b):
    if a == 0:
        return float('inf')
    if b == 0:
        return a
    ax = mpf(float(a))
    bx = mpf(float(b))
    r = (ax - bx)**2 / ax
    return float(r)

def kernel_nchi2(a, b):
    return kernel_pchi2(b, a)

def kernel_td(a, b):
    if a + b == 0:
        return 0
    ax = mpf(float(a))
    bx = mpf(float(b))
    return float((ax - bx)**2 / (ax + bx))

def kernel_kl(a, b):
    if a == 0:
        return 0
    if b == 0:
        return float('inf')
    return a * (log2(a) - log2(b))

def kernel_reverse_kl(a, b):
    return kernel_kl(b, a)

def kernel_js(a, b):
    m = (a + b)/2
    return kernel_kl(a, m) + kernel_kl(b, m)

def kernel_jf(a, b):
    raise NotImplementedError()

def kernel_mt(a, b):
    raise NotImplementedError()

def kernel_alpha(a, b):
    raise NotImplementedError()

def kernel_x2(a, b):
    raise NotImplementedError()

KERNELS = OrderedDict([
    ('tv'         , kernel_tv),
    ('hellinger'  , kernel_hellinger),
    ('pchi2'      , kernel_pchi2),
    ('nchi2'      , kernel_nchi2),
    ('td'         , kernel_td),
    ('kl'         , kernel_kl),
    ('reverse_kl' , kernel_reverse_kl),
    ('js'         , kernel_js),
    ('jf'         , kernel_x2),
    ('alpha'      , kernel_alpha),
    ('x2'         , kernel_x2),
])

# Kernels expressed in generator form.

g_tv         = lambda t: .5 * abs(t-1)
g_hellinger  = lambda t: (sqrt(t)-1)**2
g_pchi2      = lambda t: (t-1)**2
g_nchi2      = lambda t: (1-t)**2/t if t > 0 else float('inf')
g_td         = lambda t: (t-1)**2/(t+1)
g_kl         = lambda t: -log2(t) if t > 0 else float('inf')
g_reverse_kl = lambda t: t*log2(t) if t > 0 else 0
g_js         = lambda t: g_reverse_kl(t) - (1+t)*log2((1+t)/2)
g_jf         = lambda t: g_kl(t) + g_reverse_kl(t)
g_mt         = lambda t: (t-1)**2 * (t < 1)
g_alpha      = lambda t: 4/(1-.3**2) * (1 - t**((1+.3)/2))
g_x2         = lambda t: t**2 - 1

GENERATORS = OrderedDict([
    ('tv'           , g_tv),
    ('hellinger'    , g_hellinger),
    ('pchi2'        , g_pchi2),
    ('nchi2'        , g_nchi2),
    ('td'           , g_td),
    ('kl'           , g_kl),
    ('reverse_kl'   , g_reverse_kl),
    ('js'           , g_js),
    ('jf'           , g_jf),
    ('mt'           , g_mt),
    ('alpha'        , g_alpha),
    ('x2'           , g_x2),
])

# Kernels expressed in generator form using mpmath for stability.

def make_stable(f):
    def f_stable(p, q):
        px = mpf(float(p))
        qx = mpf(float(q))
        t = qx/px
        return float(f(t))
    return f_stable

sg_tv         = g_tv
sg_hellinger  = lambda t: (mpsqrt(t)-1)**2
sg_pchi2      = g_pchi2
sg_nchi2      = g_nchi2
sg_td         = g_td
sg_kl         = lambda t: 0 if t == 0 else -mplog2(t)
sg_reverse_kl = lambda t: 0 if t == 0 else t*mplog2(t)
sg_js         = lambda t: sg_reverse_kl(t) - (1+t)*mplog2((1+t)/2)
sg_jf         = lambda t: sg_kl(t) + sg_reverse_kl(t)
sg_mt         = g_mt
sg_alpha      = g_alpha
sg_x2         = g_x2

GENERATORS_STABLE = OrderedDict([
    ('tv'           , make_stable(sg_tv)),
    ('hellinger'    , make_stable(sg_hellinger)),
    ('pchi2'        , make_stable(sg_pchi2)),
    ('nchi2'        , make_stable(sg_nchi2)),
    ('td'           , make_stable(sg_td)),
    ('kl'           , make_stable(sg_kl)),
    ('reverse_kl'   , make_stable(sg_reverse_kl)),
    ('js'           , make_stable(sg_js)),
    ('jf'           , make_stable(sg_jf)),
    ('mt'           , make_stable(sg_mt)),
    ('alpha'        , make_stable(sg_alpha)),
    ('x2'           , make_stable(sg_x2)),
])

def compute_divergence_kernel(p, q, kernel):
    # assert allclose(float(sum(p)), 1)
    # assert allclose(float(sum(q)), 1)
    #
    # TODO: Handle f-divergences with no direct kernel.
    # ['alpha', 'patho', 'x2', 'jf']:
    terms = [kernel(a, b) for (a, b) in zip(p, q) if a > 0]
    return sum(terms)

def compute_divergence_generator(p, q, g):
    # assert allclose(float(sum(p)), 1)
    # assert allclose(float(sum(q)), 1)
    ratios = [b/a if a > 0 else float('inf') for a, b in zip(p, q)]
    terms = [a*g(t) for (a, t) in zip(p, ratios) if a > 0]
    return sum(terms)
