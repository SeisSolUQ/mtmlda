import numpy as np


class UninformLogPrior:
    def __init__(self, parameter_intervals):
        self._parameter_intervals = parameter_intervals
        self._log_prior_const = np.log(
            1 / np.prod(parameter_intervals[:, 1] - parameter_intervals[:, 0])
        )

    def evaluate(self, parameter):
        has_support = (
            (parameter >= self._parameter_intervals[:, 0])
            & (parameter <= self._parameter_intervals[:, 1])
        ).all()

        if has_support:
            return self._log_prior_const
        else:
            return -np.inf


class GaussianLogLikelihood:
    def __init__(self, umbridge_pto_map, data, covariance):
        self._umbridge_pto_map = umbridge_pto_map
        self._data = data
        self._precision = np.linalg.inv(covariance)

    def evaluate(self, parameter):
        observables = np.array(self._umbridge_pto_map([parameter.tolist()])[0])
        misfit = self._data - observables
        log_likelihood = -0.5 * misfit.T @ self._precision @ misfit
        return log_likelihood


class LogPosterior:
    def __init__(self, log_prior, log_likelihood):
        self._log_prior = log_prior
        self._log_likelihood = log_likelihood

    def __call__(self, parameter):
        return [[self.evaluate(parameter)]]

    def evaluate(self, parameter):
        log_prior = self._log_prior.evaluate(parameter)
        if np.isneginf(log_prior):
            log_posterior = -np.inf
        else:
            log_likelihood = self._log_likelihood.evaluate(parameter)
            log_posterior = log_prior + log_likelihood

        return log_posterior