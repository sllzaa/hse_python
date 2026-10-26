"""Метрики подписки ПРАЙМ.

Пока всё на чистом Python: pandas начинается с темы 03. Функции здесь
принимают список словарей — ровно то, что отдаёт база через fetchall()
и что приходит из внешнего API.
"""

import pandas as pd


def revenue(payments: list[dict]) -> float:
    """Выручка: сумма списаний."""
    return sum(p["amount"] for p in payments)

def local_time(df: pd.DataFrame, moment: str = "paid_at", zone: str = "time_zone") -> pd.Series:
    """Время на часах клиента: у каждой строки свой пояс."""
    parts = []
    for tz, g in df.groupby(zone):
        parts.append(g[moment].dt.tz_convert(tz).dt.tz_localize(None))
    return pd.concat(parts).sort_index()


def churn_rate(subs: pd.DataFrame, start: str, end: str) -> float:
    """Отток за период: доля подписок, активных на start, которые закончились до end."""
    start, end = pd.Timestamp(start, tz="UTC"), pd.Timestamp(end, tz="UTC")
    active = subs[
        (subs["started_at"] < start)
        & (subs["ended_at"].isna() | (subs["ended_at"] >= start))
    ]
    return (active["ended_at"] < end).sum() / len(active)