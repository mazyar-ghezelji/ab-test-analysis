import numpy as np
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def required_sample_size(baseline_rate, mde, alpha=0.05, power=0.8):
    """
    How many users per group you'd need to detect `mde` (absolute
    difference in proportion) with the given alpha/power, starting
    from `baseline_rate`. Use this BEFORE running a test.
    """
    effect_size = proportion_effectsize(baseline_rate, baseline_rate + mde)
    analysis = NormalIndPower()
    n = analysis.solve_power(effect_size=effect_size, alpha=alpha,
                              power=power, ratio=1.0)
    return int(np.ceil(n))


def achieved_power(n_per_group, baseline_rate, mde, alpha=0.05):
    """
    Given a sample size you already have, what power did you actually
    achieve to detect `mde`? Use this AFTER data collection (our case —
    Cookie Cats data already exists).
    """
    effect_size = proportion_effectsize(baseline_rate, baseline_rate + mde)
    analysis = NormalIndPower()
    power = analysis.solve_power(effect_size=effect_size, nobs1=n_per_group,
                                  alpha=alpha, ratio=1.0)
    return power


def minimum_detectable_effect(n_per_group, baseline_rate, alpha=0.05, power=0.8):
    """
    Inverse of the above: given the sample size we actually have, what's
    the smallest effect we could have reliably detected? This is the
    number that goes in the README power-analysis table.
    """
    analysis = NormalIndPower()
    effect_size = analysis.solve_power(nobs1=n_per_group, alpha=alpha,
                                        power=power, ratio=1.0)
    # convert effect size back to an absolute proportion difference
    # via binary search since proportion_effectsize isn't directly invertible
    lo, hi = 0.0, 1.0 - baseline_rate
    for _ in range(100):
        mid = (lo + hi) / 2
        es = proportion_effectsize(baseline_rate, baseline_rate + mid)
        if es < effect_size:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sample_ratio_mismatch_test(n_control, n_treatment, expected_ratio=0.5):
    """
    Chi-square goodness-of-fit test: is the observed control/treatment
    split consistent with the expected randomization ratio? Run this
    FIRST, before trusting any downstream result.
    Returns (chi2_stat, p_value).
    """
    total = n_control + n_treatment
    expected_control = total * expected_ratio
    expected_treatment = total * (1 - expected_ratio)
    chi2, p = stats.chisquare(
        f_obs=[n_control, n_treatment],
        f_exp=[expected_control, expected_treatment]
    )
    return chi2, pimport numpy as np
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def required_sample_size(baseline_rate, mde, alpha=0.05, power=0.8):
    """
    How many users per group you'd need to detect `mde` (absolute
    difference in proportion) with the given alpha/power, starting
    from `baseline_rate`. Use this BEFORE running a test.
    """
    effect_size = proportion_effectsize(baseline_rate, baseline_rate + mde)
    analysis = NormalIndPower()
    n = analysis.solve_power(effect_size=effect_size, alpha=alpha,
                              power=power, ratio=1.0)
    return int(np.ceil(n))


def achieved_power(n_per_group, baseline_rate, mde, alpha=0.05):
    """
    Given a sample size you already have, what power did you actually
    achieve to detect `mde`? Use this AFTER data collection (our case —
    Cookie Cats data already exists).
    """
    effect_size = proportion_effectsize(baseline_rate, baseline_rate + mde)
    analysis = NormalIndPower()
    power = analysis.solve_power(effect_size=effect_size, nobs1=n_per_group,
                                  alpha=alpha, ratio=1.0)
    return power


def minimum_detectable_effect(n_per_group, baseline_rate, alpha=0.05, power=0.8):
    """
    Inverse of the above: given the sample size we actually have, what's
    the smallest effect we could have reliably detected? This is the
    number that goes in the README power-analysis table.
    """
    analysis = NormalIndPower()
    effect_size = analysis.solve_power(nobs1=n_per_group, alpha=alpha,
                                        power=power, ratio=1.0)
    # convert effect size back to an absolute proportion difference
    # via binary search since proportion_effectsize isn't directly invertible
    lo, hi = 0.0, 1.0 - baseline_rate
    for _ in range(100):
        mid = (lo + hi) / 2
        es = proportion_effectsize(baseline_rate, baseline_rate + mid)
        if es < effect_size:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sample_ratio_mismatch_test(n_control, n_treatment, expected_ratio=0.5):
    """
    Chi-square goodness-of-fit test: is the observed control/treatment
    split consistent with the expected randomization ratio? Run this
    FIRST, before trusting any downstream result.
    Returns (chi2_stat, p_value).
    """
    total = n_control + n_treatment
    expected_control = total * expected_ratio
    expected_treatment = total * (1 - expected_ratio)
    chi2, p = stats.chisquare(
        f_obs=[n_control, n_treatment],
        f_exp=[expected_control, expected_treatment]
    )
    return chi2, p