import datetime
import enum
import typing as tp  # noqa


class GranularityEnum(enum.Enum):
    """
    Enum for describing granularity
    """
    DAY = datetime.timedelta(days=1, hours=0, minutes=0)
    TWELVE_HOURS = datetime.timedelta(hours=12, minutes=0)
    HOUR = datetime.timedelta(hours=1, minutes=0)
    THIRTY_MIN = datetime.timedelta(minutes=30)
    FIVE_MIN = datetime.timedelta(minutes=5)


def truncate_to_granularity(dt: datetime.datetime, gtd: GranularityEnum) -> datetime.datetime:
    """
    :param dt: datetime to truncate
    :param gtd: granularity
    :return: resulted datetime
    """
    if gtd == GranularityEnum.DAY:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    if gtd == GranularityEnum.TWELVE_HOURS:
        return dt.replace(hour=(dt.hour - dt.hour % 12), minute=0, second=0, microsecond=0)
    if gtd == GranularityEnum.HOUR:
        return dt.replace(minute=0, second=0, microsecond=0)
    if gtd == GranularityEnum.THIRTY_MIN:
        return dt.replace(minute=(dt.minute - dt.minute % 30), second=0, microsecond=0)
    if gtd == GranularityEnum.FIVE_MIN:
        return dt.replace(minute=(dt.minute - dt.minute % 5), second=0, microsecond=0)
    assert False, "Unreachable"


class DtRange:
    def __init__(
            self,
            before: int,
            after: int,
            shift: int,
            gtd: GranularityEnum
    ) -> None:
        """
        :param before: number of datetimes should take before `given datetime`
        :param after: number of datetimes should take after `given datetime`
        :param shift: shift of `given datetime`
        :param gtd: granularity
        """
        self._before = before
        self._after = after
        self._shift = shift
        self._gtd = gtd

    def __call__(self, dt: datetime.datetime) -> list[datetime.datetime]:
        """
        :param dt: given datetime
        :return: list of datetimes in range
        """
        dt = truncate_to_granularity(dt, self._gtd)
        range_for_deltas = range(-self._before + self._shift, self._after + self._shift + 1)
        time_deltas = [self._gtd.value * i for i in range_for_deltas]
        return [dt + td for td in time_deltas]


def get_interval(
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        gtd: GranularityEnum
) -> list[datetime.datetime]:
    """
    :param start_time: start of interval
    :param end_time: end of interval
    :param gtd: granularity
    :return: list of datetimes according to granularity
    """
    left = truncate_to_granularity(start_time, gtd)
    if start_time - left > datetime.timedelta(0):
        left += gtd.value
    last_in_result = truncate_to_granularity(end_time, gtd)
    result = []
    while left <= last_in_result:
        result.append(left)
        left += gtd.value
    return result
