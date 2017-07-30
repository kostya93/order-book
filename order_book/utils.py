from operator import attrgetter
from typing import List, Iterable, Optional

from .models import MaxCostRecord, MaxCostInterval


def get_max_cost_intervals(
        max_cost_records: List[MaxCostRecord]) -> Iterable[MaxCostInterval]:

    if len(max_cost_records) <= 1:
        return

    start_record = max_cost_records[0]
    for cur_record in max_cost_records:
        if cur_record.max_cost != start_record.max_cost:
            yield MaxCostInterval.from_records(start_record=start_record,
                                               end_record=cur_record)
            start_record = cur_record

    last_record = max_cost_records[-1]
    if start_record != last_record:
        yield MaxCostInterval.from_records(start_record=start_record,
                                           end_record=last_record)


def get_time_weighted_average_maximum_cost(
        max_cost_intervals: Iterable[MaxCostInterval]) -> Optional[float]:

    max_cost_intervals = list(
        filter(lambda interval: interval.max_cost is not None,
               max_cost_intervals)
    )

    time_weighted_sum = sum(
        map(lambda interval: interval.max_cost * interval.duration,
            max_cost_intervals)
    )

    duration_sum = sum(map(attrgetter('duration'), max_cost_intervals))

    return time_weighted_sum / duration_sum if duration_sum else None
