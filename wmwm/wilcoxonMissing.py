import numpy as np
from wmwm.checkTies import check_ties
from wmwm.boundsPValueWithTies import bounds_p_value_with_ties
from wmwm.boundsPValueNoTies import bounds_p_value_no_ties


def wmwm_test(X, Y, alternative='two.sided', ties=None,
              lower_boundary=-np.inf, upper_boundary=np.inf, exact=None, 
              correct=True):
    '''
    Performs the two-sample Wilcoxon-Mann-Whitney test in the presence of missing data, which controls the Type I error regardless of the values of missing data. For more details, see the reference (Zeng et al., 2024).
    
    Parameters
    ----------
    X,Y : numeric vectors of data values with potential missing data.
    alternative : a character string specifying the alternative hypothesis, must be one of "two.sided" (default), "greater" or "less".
    ties : a logical indicating whether samples could be tied. If observed samples contain tied samples, ties defaults to True. If observed samples do not contain tied samples, ties defaults to False.
    lower_boundary: (when ties is True) a number specifying the lower bound of the data set, must be smaller or equal than the minimum of all observed data.
    upper_boundary: (when ties is True) a number specifying the upper bound of the data set, must be larger or equal than the maximum of all observed data.
    exact: a logical indicating whether the bounds should be of an exact p-value.
    correct: a logical indicating whether the bounds should be of a p-value applying continuity correction in the normal approximation.

    Details
    -------
    wmwm_test performs the two-sample hypothesis test method proposed in (Zeng et al., 2024) for univariate data when not all data are observed. Bounds of the Wilcoxon-Mann-Whitney test statistic and its p-value will be computed in the presence of missing data. The p-value of the test method proposed in (Zeng et al., 2024) is then returned as the maximum possible p-value of the Wilcoxon-Mann-Whitney test.

    By default (if exact is not specified), this function returns bounds of an exact p-value if the X and Y both contain less than 50 samples and there are no ties. Otherwise, bounds of a p-value calculated using normal approximation with continuity correction will be returned.

        
    Returns
    -------
    p_value: the p-value for the test.
    bounds_statistic: bounds of the value of the Wilcoxon-Mann-Whitney test statistic.
    bounds_pvalue: bounds of the p-value of the Wilcoxon-Mann-Whitney test.
    alternative: a character string describing the alternative hypothesis.
    ties_method: a character string describing whether samples are considered tied.
    description_bounds: a character string describing the bounds of the p-value.

    
    Reference
    ----------
    [1] Mann HB, Whitney DR. On a test of whether one of two random variables is stochastically larger than the other. The annals of mathematical statistics. 1947 Mar 1:50-60.
    [2] Zeng Y, Adams NM, Bodenham DA. On two-sample testing for data with arbitrarily missing values. arXiv preprint arXiv:2403.15327. 2024 Mar 22.

    '''
    
    if alternative not in ('two.sided', 'less', 'greater'):
        
        raise ValueError("alternative must be one of 'two.sided', 'less', or 'greater'.")

    
    # Remove all infinite and NaN values
    X = X[np.isfinite(X) | np.isnan(X)]
    Y = Y[np.isfinite(Y) | np.isnan(Y)]

    # Check input
    if len(X) == 0 or len(Y) == 0:
        # Either X or Y does not contain any observed sample
        warning_msg = "either 'X' or 'Y' does not contain any observed sample"
        print(warning_msg)
        
        # Broadest bounds only
        BOUNDSWMW = np.array([0, len(X) * len(Y)])
        BOUNDSPVALUE = np.array([0, 1])
        DESCRIPTIONBOUNDS = "either 'X' or 'Y' does not contain any observed sample."
        
    else:
        # Both X and Y contain at least one observed sample
        ties = check_ties(X, Y, ties)
        
        # Compute bounds
        if ties:
            # Compute bounds of p-values with ties
            BOUNDS = bounds_p_value_with_ties(X, Y, alternative=alternative,
                                          lower_boundary=lower_boundary,
                                          upper_boundary=upper_boundary,
                                          exact=exact, correct=correct)
        else:
            # Compute bounds of p-values without ties
            BOUNDS = bounds_p_value_no_ties(X, Y, alternative=alternative,
                                        exact=exact, correct=correct)
        
        BOUNDSWMW = BOUNDS[:2]
        BOUNDSPVALUE = BOUNDS[2:4]
        exact = BOUNDS[4]
        
        # Description of bounds
        if exact:
            DESCRIPTIONBOUNDS = 'bounds_pvalue: bounds of the exact p-value'
        else:
            if correct:
                DESCRIPTIONBOUNDS = 'bounds_pvalue: bounds of the p-value obtained using normal approximation with continuity correction'
            else:
                DESCRIPTIONBOUNDS = 'bounds_pvalue: bounds of the p-value obtained using normal approximation without continuity correction'
    
    # Construct result dictionary
    RES = {
        'p_value': BOUNDSPVALUE[1],
        'bounds_statistic': BOUNDSWMW,
        'bounds_pvalue': BOUNDSPVALUE,
        'alternative': alternative,
        'ties_method': ties,
        'description_bounds': DESCRIPTIONBOUNDS
    }
    
    return RES
