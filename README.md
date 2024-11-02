
<!-- README.md is generated from README.Rmd. Please edit that file -->

# wmwm

<!-- badges: start -->
<!-- badges: end -->

This package performs the two-sample hypothesis test method proposed in 
(Zeng et al., 2024) for univariate data when data are not fully observed. 
This method is a theoretical extension of Wilcoxon-Mann-Whitney test in 
the presence of missing data, which controls the Type I error regardless 
of values of missing data.

Bounds of the Wilcoxon-Mann-Whitne test statistic and its p-value will be 
computed in the presence of missing data. The p-value of the test method 
proposed in (Zeng et al., 2024) is then returned as the maximum possible 
p-value of the Wilcoxon-Mann-Whitney test.

## Installation

``` sh
pip install wmwm
```

## Example

This is a basic example which shows you how to perform the test with
missing data:

``` python
import numpy as np
from wmwm import wmwm_test

#### Assume all samples are distinct.
X = np.array([6.2, 3.5, np.nan, 7.6, 9.2])
Y = np.array([0.2, 1.3, -0.5, -1.7])
## By default, when the sample sizes of both X and Y are smaller than 50,
## exact distribution will be used.
wmwm_test(X, Y, ties = False, alternative = 'two.sided')


## using normality approximation with continuity correction:
wmwm_test(X, Y, ties = False, alternative = 'two.sided', exact = False, correct = True)


#### Assume samples can be tied.
X = np.array([6, 9, np.nan, 7, 9])
Y = np.array([0, 1, 0, -1])
## When the samples can be tied, normality approximation will be used.
## By default, lower_boundary = -Inf, upper_boundary = Inf.
wmwm_test(X, Y, ties = True, alternative = 'two.sided')


## specifying lower_boundary and upper_boundary:
wmwm_test(X, Y, ties = True, alternative = 'two.sided', lower_boundary = -1, upper_boundary = 9)


```

## References

Zeng Y, Adams NM, Bodenham DA. On two-sample testing for data with
arbitrarily missing values. arXiv preprint arXiv:2403.15327. 2024 Mar
22.

Mann, Henry B., and Donald R. Whitney. “On a test of whether one of two
random variables is stochastically larger than the other.” The annals of
mathematical statistics (1947): 50-60.
