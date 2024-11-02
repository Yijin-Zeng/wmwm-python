import numpy as np
from .boundsSumRank import bounds_sum_rank


def bounds_wmw_statistic(X, Y, ties, lower_boundary, upper_boundary):
    # Sample size
    n = len(X)

    # Compute bounds of sum of ranks using bounds_sum_rank function
    Bounds = bounds_sum_rank(X, Y, ties, lower_boundary, upper_boundary)
    lowerBoundSumRank = Bounds[0]
    upperBoundSumRank = Bounds[1]

    # Compute bounds of WMW test statistic
    lowerBoundWMWStatistic = lowerBoundSumRank - n * (n + 1) / 2
    upperBoundWMWStatistic = upperBoundSumRank - n * (n + 1) / 2

    return np.array([lowerBoundWMWStatistic, upperBoundWMWStatistic])
