import numpy as np
from scipy.stats import norm, rankdata
from .boundsWMWStatistic import bounds_wmw_statistic


def bounds_p_value_with_ties(X, Y, alternative, lower_boundary, upper_boundary, exact=None, correct=False):
    # Sample size
    n = len(X)
    m = len(Y)
    
    # Observed samples in X and Y, respectively
    X_prime = X[~np.isnan(X)]
    Y_prime = Y[~np.isnan(Y)]
    Z_prime = np.concatenate((X_prime, Y_prime))
    r = rankdata(Z_prime)
    
    # Observed sample size
    n_prime = len(X_prime)
    m_prime = len(Y_prime)
    
    # Compute bounds of WMWS statistic using boundsWMWStatistic function
    Bounds = bounds_wmw_statistic(X, Y, ties=True, lower_boundary=lower_boundary, upper_boundary=upper_boundary)
    lowerBoundWMWStatistic = Bounds[0]
    upperBoundWMWStatistic = Bounds[1]
    
    # Decide if exact
    if exact is None:
        exact = (n < 50) and (m < 50)
    
    if exact:
        print("Warning: cannot bound exact p-value with ties")
        exact = 0
    
    # Using normal approximation
    correct_lower = 0
    correct_upper = 0
    if correct:
        if alternative == 'two.sided':
            correct_lower = np.sign((lowerBoundWMWStatistic - n * m / 2)) * 0.5
            correct_upper = np.sign((upperBoundWMWStatistic - n * m / 2)) * 0.5
        elif alternative == 'greater':
            correct_lower = 0.5
            correct_upper = 0.5
        elif alternative == 'less':
            correct_lower = -0.5
            correct_upper = -0.5
    
    _, nties = np.unique(r, return_counts = True)
    
    mu = n * m / 2
    
    sigmaSquareMax = (n * m * (n + m + 1) / 12 -
                      n * m * np.sum(nties ** 3 - nties) / (12 * (n + m) * (n + m - 1)))
    
    nties[np.argmax(nties)] += n + m - n_prime - m_prime
    
    sigmaSquareMin = (n * m * (n + m + 1) / 12 -
                      n * m * np.sum(nties ** 3 - nties) / (12 * (n + m) * (n + m - 1)))
    
    if sigmaSquareMax == 0 or sigmaSquareMin == 0:
        raise ValueError("Cannot compute valid p-value")
    
    Z_1 = (lowerBoundWMWStatistic - correct_lower - mu) / np.sqrt(sigmaSquareMin)
    Z_2 = (upperBoundWMWStatistic - correct_upper - mu) / np.sqrt(sigmaSquareMax)
    Z_3 = (upperBoundWMWStatistic - correct_upper - mu) / np.sqrt(sigmaSquareMin)
    Z_4 = (lowerBoundWMWStatistic - correct_lower - mu) / np.sqrt(sigmaSquareMax)
    
    # Compute p-values
    if alternative == 'two.sided':
        p_1 = 2 * (1 - norm.cdf(np.abs(Z_1)))
        p_2 = 2 * (1 - norm.cdf(np.abs(Z_2)))
        p_3 = 2 * (1 - norm.cdf(np.abs(Z_3)))
        p_4 = 2 * (1 - norm.cdf(np.abs(Z_4)))
    elif alternative == 'greater':
        p_1 = 1 - norm.cdf(Z_1)
        p_2 = 1 - norm.cdf(Z_2)
        p_3 = 1 - norm.cdf(Z_3)
        p_4 = 1 - norm.cdf(Z_4)
    elif alternative == 'less':
        p_1 = norm.cdf(Z_1)
        p_2 = norm.cdf(Z_2)
        p_3 = norm.cdf(Z_3)
        p_4 = norm.cdf(Z_4)
    else:
        raise ValueError("Unknown alternative hypothesis")
    
    # Decide bounds of p-value
    if alternative == 'two.sided':
        if (lowerBoundWMWStatistic - n * m / 2 < 0) and (upperBoundWMWStatistic - n * m / 2 < 0):
            lowerBoundPValue = p_1
            upperBoundPValue = p_2
        elif (lowerBoundWMWStatistic - n * m / 2 < 0) and (upperBoundWMWStatistic - n * m / 2 >= 0):
            lowerBoundPValue = min(p_1, p_3)
            upperBoundPValue = 1
        else:
            lowerBoundPValue = p_3
            upperBoundPValue = p_4
    elif alternative == 'greater':
        if (lowerBoundWMWStatistic - n * m / 2 < 0) and (upperBoundWMWStatistic - n * m / 2 < 0):
            lowerBoundPValue = p_2
            upperBoundPValue = p_1
        elif (lowerBoundWMWStatistic - n * m / 2 < 0) and (upperBoundWMWStatistic - n * m / 2 >= 0):
            lowerBoundPValue = p_3
            upperBoundPValue = p_1
        else:
            lowerBoundPValue = p_3
            upperBoundPValue = p_4
    elif alternative == 'less':
        if (lowerBoundWMWStatistic - n * m / 2 < 0) and (upperBoundWMWStatistic - n * m / 2 < 0):
            lowerBoundPValue = p_1
            upperBoundPValue = p_2
        elif (lowerBoundWMWStatistic - n * m / 2 < 0) and (upperBoundWMWStatistic - n * m / 2 >= 0):
            lowerBoundPValue = p_1
            upperBoundPValue = p_3
        else:
            lowerBoundPValue = p_4
            upperBoundPValue = p_3
    else:
        raise ValueError("Unknown alternative hypothesis")
    
    return [lowerBoundWMWStatistic, upperBoundWMWStatistic, lowerBoundPValue, upperBoundPValue, exact]


# Example usage:
# X = np.array([1, 1, np.nan, 4, 5])
# Y = np.array([3, np.nan, 6, 7])
# alternative = 'two.sided'
# exact = None
# correct = True
# result = bounds_p_value_with_ties(X, Y, alternative, lower_boundary= 1, upper_boundary= np.inf, exact = exact, correct = correct)
# print("Lower bound of WMW Statistic:", result[0])
# print("Upper bound of WMW Statistic:", result[1])
# print("Lower bound of p-value:", result[2])
# print("Upper bound of p-value:", result[3])
# print("Exact:", result[4])
