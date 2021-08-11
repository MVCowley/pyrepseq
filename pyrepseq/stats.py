import numpy as np
import pandas as pd
import scipy.optimize
import scipy.special

def powerlaw(size=1, xmin=1.0, alpha=2.0):
    """ Draw samples from a discrete power-law.

    Uses an approximate transformation technique, see Eq. D6 in Clauset et al. arXiv 0706.1062v2 for details.
    """
    r = np.random.rand(int(size))
    return np.floor((xmin - 0.5)*(1.0-r)**(-1.0/(alpha-1.0)) + 0.5)

def mle_alpha(c, cmin=1.0, continuitycorrection=True):
    """Maximum likelihood estimate of the power-law exponent.
    
    see Eq. B17 in Clauset et al. arXiv 0706.1062v2
    """
    c = np.asarray(c)
    c = c[c>=cmin]
    if continuitycorrection:
        return 1.0 + len(c)/np.sum(np.log(c/(cmin-0.5)))
    return 1.0 + len(c)/np.sum(np.log(c/cmin))

def _discrete_loglikelihood(x, alpha, xmin):
    "Power-law loglikelihood"
    x = x[x>=xmin]
    n = len(x)
    return -n*np.log(scipy.special.zeta(alpha, xmin)) - alpha*np.sum(np.log(x))

def mle_alpha_discrete(c, cmin=1.0, **kwargs):
    """Maximum likelihood estimate of the power-law exponent for discrete data.

    Numerically maximizes the discrete loglikelihood.

    kwargs are passed to scipy.optimize.minimize_scalar.
    Default kwargs: bounds=[1.5, 4.5], method='bounded'
    """
    optkwargs = dict(bounds=[1.5, 4.5], method='bounded')
    optkwargs.update(kwargs)
    c = np.asarray(c)
    c = c[c>=cmin]
    result = scipy.optimize.minimize_scalar(lambda alpha: -_discrete_loglikelihood(c, alpha, cmin), **optkwargs)
    if not result.success:
        raise Exception('fitting failed')
    return result.x

def halfsample_sd(data, statistic, bootnum=1000):
    """
    Calculate an empirical estimate of the standard deviation of a statistic by sampling random halves of the data.
    """
    halfsampled = [statistic(np.random.choice(data,
                                            size=int(len(data)//2),
                                            replace=False))
                    for i in range(bootnum)]
    return np.std(halfsampled)/2**.5


def coincidence_probability(array):
    """
    Calculates probability that two distinct elements of a list are the same.

    Note: this is also known as the Simpson or Hunter-Gaston index
    """
    array = np.asarray(array)
    _, counts = np.unique(array, return_counts=True)
    # 2*(n choose 2) = n * (n-1)
    return np.sum(counts*(counts-1))/(array.shape[0]*(array.shape[0]-1))
