import numpy as np
from statsmodels.base.model import GenericLikelihoodModel
from numpy.polynomial.hermite import hermgauss
from scipy.special import expit

#todo Calibration
#todo item graphs
#todo Information Graphs

DEBUG = False


class Irt(GenericLikelihoodModel):
    '''
    Fit the two-parameter logistic IRT model.
    '''
    def __init__(self, *args, **kwargs):
        self._set_quadrature_points(kwargs.pop('deg', 7))
        super(GenericLikelihoodModel, self).__init__(*args, **kwargs)
        param_names = (
            ['alpha_%d' % i for i in range(self.p)] +
            ['beta_%d' % i for i in range(self.p)]
        )
        self._set_extra_params_names(param_names)
        self.df_model = 2 * self.p
        self.df_resid = np.prod(self.endog.shape) - 2 * self.p
        self._collapse_data()

    def _set_quadrature_points(self, deg):
        self.deg = deg
        # these points and weights are designed for integrating with
        # the following weight function: :math:`f(x) = \exp(-x^2)`
        x, w = hermgauss(deg=deg)
        # the following modification is for integrating with the
        # standard normal distribution
        self.x = np.sqrt(2) * x
        w = w / np.sqrt(np.pi)
        self.w = np.asmatrix(w[:, np.newaxis])

    def _collapse_data(self):
        # this requires numpy version >= 1.13.0
        X, n = np.unique(self.endog, axis=0, return_counts=True)
        self.X = np.asmatrix(X)
        self.n = np.asmatrix(n).T

    @property
    def p(self):
        return self.endog.shape[1]

    def _B(self, params):
        _alphas = params[0:self.p]
        _betas = params[self.p:]
        if DEBUG:
            print((_alphas, -_betas / _alphas))
        B = np.matrix([_alphas, _betas]).transpose()
        return B

    def _Z(self):
        # TODO: are the weights and quadrature points correct?
        Z = np.matrix([self.x, np.ones(self.deg)])
        return Z

    def loglike(self, params):
        B = self._B(params)
        Z = self._Z()
        X = self.X
        w = self.w

        ll = np.log(
            np.exp(
                X * np.log(expit(B * Z)) +
                (1 - X) * np.log(1 - expit(B * Z))
            ) * w
        )
        total = self.n.T * ll
        assert total.shape == (1, 1)
        result = total[0, 0]
        if DEBUG:
            print(result)
        return result

    def score(self, params):
        B = self._B(params)
        Z = self._Z()
        pr = expit(B * Z)

        X = self.X
        w = self.w
        p_xz = np.exp(X * np.log(pr) + (1 - X) * np.log(1 - pr))
        p_x = p_xz * w
        p_zx = np.multiply(p_xz / p_x, self.n)

        scores = np.asmatrix(np.zeros((self.p, 2)))
        # TODO: Let's make sure everything in here is a matrix (not an
        # array).
        for i in range(self.p):
            Y = np.add.outer(X[:, i], -pr[i, :])
            # hack to make the four dimensional array 2-d
            Y = np.asmatrix(Y[:, 0, 0, :])
            scores[i, ] = -col_sums(np.multiply(p_zx, Y)) * np.multiply(w, Z.transpose())

        result = np.asarray(scores).flatten(order='F')
        if DEBUG:
            print(result)
        return -result


def col_sums(x):
    return np.sum(x, axis=0)
