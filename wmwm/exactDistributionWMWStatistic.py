# Compute the exact distribution of WMW test statistic

import numpy as np
import math

def num_seq(U, n, m):
    '''
    Given the sample sizes n, m of x and y, return the number of sequences such that the values of x precedes the values of y U times. For more details, see the reference provided.
    
    Parameters
    ----------
    U : int
        Value for which the number is computed.
    n : int
        Sample size of x.
    m : int
        Sample size of y.
        
    Returns
    -------
    int
        The number of sequences such that the values from x precedes the values from y U times
    
    Reference
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
    Distribution function of the Wilcoxon rank sum statistic obtained from x, y with size n and m, respectively.

    Parameters
    ----------
    U : int
        Value of the Wilcoxon rank sum statistic for which the probability is calculated.
    n : int
        Sample size of x.
    m : int
        Sample size of y.

    Returns
    -------
    float
        Probability of Wilcoxon rank sum statistic smaller or equal than U

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
       
