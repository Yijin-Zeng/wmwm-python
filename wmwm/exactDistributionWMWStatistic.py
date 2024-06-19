# Compute the exact distribution of WMW test statistic

import numpy as np
import math

def num_seq(U, n, m):
    '''
    Compute the number sequences rank sum statistics: U, number of samples in x and y: n and m.
    
    Parameters
    ----------
    U : int
        Replace each x by a 0 and each y by a 1. Let U count the number of times a 1 precedes a 0.
    n : int
        Sample size of x.
    m : int
        Sample size of y.
        
    Returns
    -------
    int
        The number of sequences of n O's and m 1's in each of which a 1 precedes a 0 U times.
    
    References
    ----------
    Mann HB, Whitney DR. On a test of whether one of two random variables is stochastically larger than the other. The annals of mathematical statistics. 1947 Mar 1:50-60.

    '''

    if U < 0:
        return 0

    if (n == 0 or m == 0) and U != 0:
        return 0
    
    if (n == 0 or m == 0) and U == 0:
        return 1

    return num_seq(U - m, n - 1, m) + num_seq(U, n, m-1)


def dis_WMW_exact(U,n,m, lower_tail = True):
    '''
    Distribution function for the distribution of the Wilcoxon rank sum statistic 
    obtained from samples with size n and m, respectively

    Parameters
    ----------
    t : TYPE
        DESCRIPTION.
    n : TYPE
        DESCRIPTION.
    m : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    # number of all possible combinations of x and y
    num_all = math.factorial(m + n) / math.factorial(m) / math.factorial(n)    

    # probability of Wilcoxon rank sum statistic smaller or equal than U
    prob = 0
    for k in np.arange(0,U+1): 
    
        num_res = num_seq(k, n, m)

        prob += num_res/num_all
        
    if lower_tail:
        
        return prob
    
    else:
        
        return 1 - prob
       
