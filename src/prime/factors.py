import math

import matplotlib.pyplot as plt
import pandas as pd


def chain(n0, p0, n1, p1):
    """Цепные подстановки для R = N × P: сначала количество, потом цена."""
    by_count = (n1 - n0) * p0
    by_price = n1 * (p1 - p0)
    assert abs(
        by_count + by_price - (n1 * p1 - n0 * p0)
    ) < 0.01, "сумма влияний не равна изменению"
    return round(by_count), round(by_price)


def contrib(x0: dict, x1: dict, order: list[str]) -> dict:
    """Влияние каждого фактора: меняем их по одному в порядке order."""
    cur, out = dict(x0), {}
    for f in order:
        before = math.prod(cur.values())
        cur[f] = x1[f]
        out[f] = math.prod(cur.values()) - before
    total = math.prod(x1.values()) - math.prod(x0.values())
    assert abs(sum(out.values()) - total) < 0.01, "сумма влияний не равна изменению"
    return out


def waterfall(deltas: pd.Series, title: str) -> plt.Axes:
    """Каскад изменений: по столбику на фактор и «итого» в конце."""
    before = deltas.cumsum() - deltas
    colors = ["#C1272D" if v < 0 else "#2A9D8F" for v in deltas]
    fig, ax = plt.subplots(figsize=(9, 4.6), layout="constrained")
    bars = ax.bar(
        deltas.index,
        deltas,
        bottom=before,
        color=colors,
        zorder=2,
    )
    total = ax.bar("итого", deltas.sum(), color="#6B7280", zorder=2)
    for group in (bars, total):
        ax.bar_label(
            group,
            fmt=lambda v: f"{v:+,.0f}".replace(",", " ").replace("-", "−"),
            padding=3,
        )
    ax.axhline(0, color="#111827", linewidth=0.8)
    ax.set_title(title, loc="left")
    ax.set_ylabel("тыс. ₽")
    ax.use_sticky_edges = False
    ax.margins(y=0.15)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E5E7EB")
    return ax