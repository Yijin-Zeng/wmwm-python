
<!-- README.md is generated from README.Rmd. Please edit that file -->

# wmwm

<!-- badges: start -->
<!-- badges: end -->

This package includes one function `wilcoxonMissing()`, which performs
the two-sample hypothesis test method proposed in (Zeng et al., 2024)
for univariate data when data are not fully observed. Its method is a
theoretical extension of Wilcoxon-Mann-Whitney test in the presence of
missing data, which controls the Type I error regardless of values of
missing data.

Bounds of the Wilcoxon-Mann-Whitne test statistic and its p-value will
be computed in the presence of missing data. The p-value of the test
method proposed in (Zeng et al., 2024) is then returned as the maximum
possible p-value of the Wilcoxon-Mann-Whitney test.

## Installation

You can install the development version of wmwm from
[GitHub](https://github.com/) with:

``` sh
pip install wmwm
```

## Example

This is a basic example which shows you how to perform the test with
missing data:

``` python
from wmwm import wmwm_test
import numpy as np

X = np.array([1, 2, np.nan, 4, 5])
Y = np.array([3, np.nan, 6, 7])
result = wmwm_test(X, Y)
print(result['p_value'])
#> 1.0
```

## References

Zeng Y, Adams NM, Bodenham DA. On two-sample testing for data with
arbitrarily missing values. arXiv preprint arXiv:2403.15327. 2024 Mar
22.

Mann, Henry B., and Donald R. Whitney. “On a test of whether one of two
random variables is stochastically larger than the other.” The annals of
mathematical statistics (1947): 50-60.
