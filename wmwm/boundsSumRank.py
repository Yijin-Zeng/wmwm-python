import numpy as np
from scipy.stats import rankdata

def bounds_sum_rank(X, Y, ties, lower_boundary, upper_boundary):
    
    # Sample size
    n = len(X)
    m = len(Y)

    # Observed samples in X and Y, respectively
    X_prime = X[~np.isnan(X)]
    Y_prime = Y[~np.isnan(Y)]

    # All observed samples
    Z_prime = np.concatenate((X_prime, Y_prime))

    # Observed sample size
    n_prime = len(X_prime)
    m_prime = len(Y_prime)

    # Sum of ranks of X_prime in Z_prime
    rankSumX_prime = np.sum(rankdata(Z_prime, method = 'average')[:n_prime])

    # Bounds of sum of ranks of X in Z without ties
    lowerBoundSumRank = (rankSumX_prime + 
                         (n - n_prime) * (n + n_prime + 1) / 2)
    
    upperBoundSumRank = (rankSumX_prime +
                         (n * (n + 2 * m + 1) - n_prime * 
                          (n_prime + 2 * m_prime + 1)) / 2)

    # Bounds of sum of ranks of X in Z with ties
    if ties:
        # If ties are allowed, tighter bounds may exist
        min_observed = np.min(Z_prime)
        max_observed = np.max(Z_prime)

        if lower_boundary <= min_observed:
            a = lower_boundary
        else:
            print('lower_boundary must be smaller or equal than the minimum of all observed data. lower_boundary is set to -Inf')
            a = -np.inf

        if upper_boundary >= max_observed:
            b = upper_boundary
        else:
            print('upper_boundary must be larger or equal than the maximum of all observed data. upper_boundary is set to Inf')
            b = np.inf

        lowerBoundSumRank += (np.sum(np.array(Y_prime) == a) * (n - n_prime) \
                              + np.sum(np.array(X_prime) == b) \
                              * (m - m_prime)) / 2

        upperBoundSumRank -= (np.sum(np.array(X_prime) == a) * (m - m_prime) \
                              + np.sum(np.array(Y_prime) == b) \
                              * (n - n_prime)) / 2

    return np.array([lowerBoundSumRank, upperBoundSumRank])

# Example usage:
# X = np.array([1, 2, np.nan, 4, 5])
# Y = np.array([3, np.nan, 6, 7])
# ties = True
# lower_boundary = -np.inf
# upper_boundary = np.inf

# result = bounds_sum_rank(X, Y, ties, lower_boundary, upper_boundary)
# print("Lower bound:", result[0])
# print("Upper bound:", result[1])


