from datetime import datetime

from app.core import settings

HFP = settings.HALFLIFE


def rating_calculation(rows: list[datetime, int]) -> float:
    rows = [(1 * 2 ** -(abs((datetime.utcnow() - i[0]).days / HFP)), i[1]) for i in rows]  # weight, rating
    rating = sum(i[0] * i[1] for i in rows) / sum(i[0] for i in rows)
    return int(rating)
