import numpy as np
from .checkTies import check_ties
from .boundsPValueWithTies import bounds_p_value_with_ties
from .boundsPValueNoTies import bounds_p_value_no_ties


def wmwm_test(X, Y, alternative='two.sided', ties=None,
              lower_boundary=-np.inf, upper_boundary=np.inf, exact=None, 
              correct=True):
    
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
            DESCRIPTIONBOUNDS = 'bounds_pvalue is the bounds of the exact p-value'
        else:
            if correct:
                DESCRIPTIONBOUNDS = 'bounds_pvalue is the bounds of the p-value obtained using normal approximation with continuity correction'
            else:
                DESCRIPTIONBOUNDS = 'bounds_pvalue is the bounds of the p-value obtained using normal approximation'
    
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

# Example
# X = np.array([1, 2, np.nan, 4, 5])
# Y = np.array([3, np.nan, 6, 7])
# result = wmwm_test(X, Y)
