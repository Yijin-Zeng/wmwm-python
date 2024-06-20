import numpy as np
from scipy.stats import norm
from .boundsWMWStatistic import bounds_wmw_statistic
from .exactDistributionWMWStatistic import dis_WMW_exact


def bounds_p_value_no_ties(X, Y, alternative, exact=None, correct=False):
    # Sample size
    n = len(X)
    m = len(Y)

    # Compute bounds of WMWS statistic using bounds_wmw_statistic function
    Bounds = bounds_wmw_statistic(X, Y, ties=False, lower_boundary=-np.inf, upper_boundary=np.inf)
    lowerBoundWMWStatistic = Bounds[0]
    upperBoundWMWStatistic = Bounds[1]

    # Decide if exact 
    if exact is None:
        exact = (n < 50) and (m < 50)

    # Compute p_1, p_2 -- the p-values corresponding to the minimum and maximum WMW test statistics, respectively
    if exact:
        # compute p_1
        if alternative == 'two.sided':
            if lowerBoundWMWStatistic > (n * m / 2):
                p = dis_WMW_exact(lowerBoundWMWStatistic-1, n, m, lower_tail=False)
            else:
                p = dis_WMW_exact(lowerBoundWMWStatistic, n, m)
            p_1 = min(2 * p, 1)
        elif alternative == 'greater':
            p_1 = dis_WMW_exact(lowerBoundWMWStatistic-1, n, m, lower_tail=False)
        elif alternative == 'less':
            p_1 = dis_WMW_exact(lowerBoundWMWStatistic, n, m)
        
        # compute p_2
        if alternative == 'two.sided':
            if lowerBoundWMWStatistic > (n * m / 2):
                p = dis_WMW_exact(upperBoundWMWStatistic-1, n, m, lower_tail=False)
            else:
                p = dis_WMW_exact(upperBoundWMWStatistic, n, m)
            p_2 = min(2 * p, 1)
        elif alternative == 'greater':
            p_2 = dis_WMW_exact(upperBoundWMWStatistic-1, n, m, lower_tail=False)
        elif alternative == 'less':
            p_2 = dis_WMW_exact(upperBoundWMWStatistic, n, m)
            
    else:
        # if not exact, using normal approximation
        correct_lower = 0
        correct_upper = 0

        if correct:
            # using continuity correction
            if alternative == "two.sided":
                correct_lower = np.sign(lowerBoundWMWStatistic - n * m / 2) * 0.5
                correct_upper = np.sign(upperBoundWMWStatistic - n * m / 2) * 0.5
            elif alternative == "greater":
                correct_lower = 0.5
                correct_upper = 0.5
            elif alternative == "less":
                correct_lower = -0.5
                correct_upper = -0.5

        mu = n * m / 2
        sigma = np.sqrt(n * m * (n + m + 1) / 12)

        lowerBoundZ = (lowerBoundWMWStatistic - correct_lower - mu) / sigma
        upperBoundZ = (upperBoundWMWStatistic - correct_upper - mu) / sigma

        if alternative == 'two.sided':
            if lowerBoundZ < 0:
                p = norm.cdf(lowerBoundZ)
            else:
                p = 1 - norm.cdf(lowerBoundZ)
            p_1 = 2 * p
        elif alternative == 'greater':
            p_1 = norm.sf(lowerBoundZ)
        elif alternative == 'less':
            p_1 = norm.cdf(lowerBoundZ)

        if alternative == 'two.sided':
            if upperBoundZ < 0:
                p = norm.cdf(upperBoundZ)
            else:
                p = 1 - norm.cdf(upperBoundZ)
            p_2 = 2 * p
        elif alternative == 'greater':
            p_2 = norm.sf(upperBoundZ)
        elif alternative == 'less':
            p_2 = norm.cdf(upperBoundZ)

    # Compute bounds of p-values
    lowerBoundPValue = min(p_1, p_2)

    if alternative == 'two.sided':
        if ((lowerBoundWMWStatistic - n * m / 2) * (upperBoundWMWStatistic - n * m / 2)) > 0:
            upperBoundPValue = max(p_1, p_2)
        else:
            upperBoundPValue = 1
    elif alternative == 'greater':
        upperBoundPValue = p_1
    elif alternative == 'less':
        upperBoundPValue = p_2

    return np.array([lowerBoundWMWStatistic, upperBoundWMWStatistic, lowerBoundPValue, upperBoundPValue, exact])

# Example usage:
# X = np.array([1, 2, np.nan, 4, 5])
# Y = np.array([3, np.nan, 6, 7])
# alternative = 'two.sided'
# exact = None
# correct = False
# result = bounds_p_value_no_ties(X, Y, alternative, exact, correct)
# print("Lower bound of WMW Statistic:", result[0])
# print("Upper bound of WMW Statistic:", result[1])
# print("Lower bound of p-value:", result[2])
# print("Upper bound of p-value:", result[3])
# print("Exact:", result[4])
