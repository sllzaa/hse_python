import math
from statistics import NormalDist

z = NormalDist().inv_cdf


def n_per_group(sigma: float, mde: float, alpha: float = 0.05,
                power: float = 0.8, comparisons: int = 1) -> int:
    """Количество клиентов на каждую группу."""
    za = z(1 - alpha / (2 * comparisons))
    zb = z(power)

    return math.ceil(2 * (za + zb) ** 2 * sigma ** 2 / mde ** 2)


def mde_for_n(sigma: float, n: int, alpha: float = 0.05,
              power: float = 0.8, comparisons: int = 1) -> float:
    """Минимальный обнаруживаемый эффект при заданном размере группы."""
    za = z(1 - alpha / (2 * comparisons))
    zb = z(power)

    return math.sqrt(2 * (za + zb) ** 2 * sigma ** 2 / n)


def diff_ci(t, c, alpha: float = 0.05) -> dict:
    """Разность средних test − control, доверительный интервал и p-value."""
    d = t.mean() - c.mean()
    se = (t.var() / len(t) + c.var() / len(c)) ** 0.5
    q = NormalDist().inv_cdf(1 - alpha / 2)
    p = 2 * (1 - NormalDist().cdf(abs(d / se)))

    return {
        "diff": d,
        "lo": d - q * se,
        "hi": d + q * se,
        "p": p
    }


def srm_pvalue(sizes) -> float:
    """p-value критерия хи-квадрат для равных долей 2 или 3 групп."""
    n = sum(sizes)
    exp = n / len(sizes)
    chi2 = sum((s - exp) ** 2 / exp for s in sizes)

    if len(sizes) == 2:
        return math.erfc(math.sqrt(chi2 / 2))
    if len(sizes) == 3:
        return math.exp(-chi2 / 2)

    raise ValueError("для 4 и более групп — scipy.stats.chisquare")


def cuped(y, x):
    """Скорректированная метрика CUPED и коэффициент theta."""
    theta = y.cov(x) / x.var()
    return y - theta * (x - x.mean()), theta