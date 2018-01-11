Read `ltm::ltm()` code to get a better understanding of how they fit a two parameter model.

# Testing

To run the tests use:

    python -m unittest discover

# Features

Here is a list of features we would like to include:

Classical Test Theory:

Item Analysis (P_value, Discirimination)
Reliability (Alpha, Split Form)
Differential Item Functioning
Examinee Scoring(rowSum) (scored and unscored + linking)
CTT Equating
Standard Setting

Item Response Theory

Model Fitting (1, 2, 3, PCM.... blah blah blah)
Item Parameter estimates
Scoring
DIF
Equating
Standard Setting map onto IRT scale
mIRT
graphs for each item IRT parameters, IRT

Other Features
Computer Adaptive Test ability (CAT)
Automated Essay Scoring Example (NLP)
Ability to simulate data

# Notes

Here are some code snippets for the two parameter model.

Note the ltm package ships with the Gauss Hermite quadrature points and weights pre-computed. That data is stored in ltm/data/gh.rda.

Here is the log likelihood from ltm/R/loglikltm.R:

``` r
loglikltm <-
function (betas, constraint) {
    betas <- betas.ltm(betas, constraint, p, q.)
    pr <- probs(Z %*% t(betas))
    p.xz <- exp(X %*% t(log(pr)) + mX %*% t(log(1-pr)))
    p.x <- rep(c(p.xz %*% GHw), obs)
    -sum(log(p.x))
}

betas.ltm <-
function (betas, constraint, p, q.) {
    if (!is.null(constraint)) {
        betas. <- matrix(0, p, q.)
        betas.[constraint[, 1:2, drop = FALSE]] <- constraint[, 3]
        betas.[-((constraint[, 2] - 1) * p + constraint[, 1])] <- betas
        betas.
    } else {
        matrix(betas, p)
    }
}

probs <-
function (x) {
    pr <- plogis(x)
    if (any(ind <- pr == 1))
        pr[ind] <- 1 - sqrt(.Machine$double.eps)
    if (any(ind <- pr == 0))
        pr[ind] <- sqrt(.Machine$double.eps)
    pr
}
```

Here is the gradient from ltm/R/scoreltm.R:

``` r
scoreltm <-
function (betas, constraint) {
    betas <- betas.ltm(betas, constraint, p, q.)
    pr <- probs(Z %*% t(betas))
    p.xz <- exp(X %*% t(log(pr)) + mX %*% t(log(1 - pr)))
    p.x <- c(p.xz %*% GHw)
    p.zx <- (p.xz / p.x) * obs
    scores <- matrix(0, p, q.)
    for (i in 1:p) {
        ind. <- na.ind[, i]
        Y <- outer(X[, i], pr[, i], "-")
        Y[ind., ] <- 0
        scores[i, ] <- -colSums((p.zx * Y) %*% (Z * GHw))
    }
    if (!is.null(constraint))
        scores[-((constraint[, 2] - 1) * p + constraint[, 1])]
    else
        c(scores)
}
```

X 14x4 (14 student profiles, 4 questions)
Z 7x2 (7 quadrature points)
betas 4x2
na.ind 14x4 (where are there missing observations)
p.x 14x1
p.xz 14x7 (students x quadrature points)
p.zx 14x7
pr 7x4 (quadrature points by questions)
scores 4x2 (this gets unraveled at the end)

Y 14x7

# TODO

We should switch from using numpy matrices to using numpy arrays. The notation of matrix multiplication gets a little dicey. I would vote for requiring Python >= 3.5 so that we can use the `@` operator for multiplication. If we support older versions of Python then we need to use the `np.dot()` function, which I find hard to read.

https://stackoverflow.com/questions/4151128/what-are-the-differences-between-numpy-arrays-and-matrices-which-one-should-i-u

# References

Rizopoulos, D. (2006). ltm: An R package for latent variable modeling and item response theory analyses. Journal of Statistical Software, 17(5), 1–25.

Baker, Frank B., and Seock-Ho Kim, eds. Item response theory: Parameter estimation techniques. CRC Press, 2004.

https://www.stata.com/manuals/irt.pdf

https://stat.ethz.ch/pipermail/r-help/2006-March/102079.html
