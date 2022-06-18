from datetime import datetime
import dateutil.tz

DEFAULT_TZ_NAME = "Europe/Moscow"


def _replace_tz(dt: datetime) -> datetime:
    tz = dateutil.tz.gettz(DEFAULT_TZ_NAME)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)
    else:
        return dt.astimezone(tz)


def now() -> datetime:
    """Return now in default timezone"""
    tz = dateutil.tz.gettz(DEFAULT_TZ_NAME)
    return datetime.now(tz)


def strftime(dt: datetime, fmt: str) -> str:
    """Return dt converted to string according to format in default timezone"""
    return _replace_tz(dt).strftime(fmt)


def strptime(dt_str: str, fmt: str) -> datetime:
    """Return dt parsed from string according to format in default timezone"""
    dt = datetime.strptime(dt_str, fmt)
    return _replace_tz(dt)


def diff(first_dt: datetime, second_dt: datetime) -> int:
    """Return seconds between two datetimes rounded down to closest int"""
    return int((_replace_tz(second_dt) - _replace_tz(first_dt)).total_seconds())


def timestamp(dt: datetime) -> int:
    """Return timestamp for given datetime rounded down to closest int"""
    return int(_replace_tz(dt).timestamp())


def from_timestamp(ts: float) -> datetime:
    """Return datetime from given timestamp"""
    tz = dateutil.tz.gettz(DEFAULT_TZ_NAME)
    return datetime.fromtimestamp(ts, tz)
