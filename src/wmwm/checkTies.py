import numpy as np
from scipy.stats import rankdata


def check_ties(X, Y, ties):
    Z = np.concatenate((X, Y))

    # Observed samples in X and Y, respectively
    X_prime = X[~np.isnan(X)]
    Y_prime = Y[~np.isnan(Y)]

    # All observed samples
    Z_prime = np.concatenate((X_prime, Y_prime))
    r = rankdata(Z_prime)

    # Check ties
    if ties is None:
        # If ties is not specified, decide ties according to observed samples
        ties = len(r) != len(np.unique(r))
    else:
        # If ties is specified, consider false cases
        if not ties and len(r) != len(np.unique(r)):
            print("observed samples are tied, you may want to specify ties = True")

        if ties and len(r) == len(np.unique(r)) and len(Z) == len(Z_prime):
            print("all samples are observed distinct numbers, ties can only be False")
            ties = False

        if not ties and len(r) != len(np.unique(r)) and len(Z) == len(Z_prime):
            print("all samples are observed with tied observations, ties can only be True")
            ties = True

    return ties
