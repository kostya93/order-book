import argparse

from .models import OrderBook, Order, MaxCostRecord, OperationKind, Operation
from .utils import (get_max_cost_intervals,
                    get_time_weighted_average_maximum_cost)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file',
                        type=argparse.FileType('r'),
                        help='file with list of operations with orders')
    return parser.parse_args()


def parse_operation_params(line: str) -> Operation:
    operation_params = line.split()

    timestamp = int(operation_params[0])
    kind = OperationKind(operation_params[1])
    order_id = int(operation_params[2])
    cost = float(operation_params[3]) if kind == OperationKind.INSERT else None

    return Operation(timestamp, kind, order_id, cost)


def main():
    order_book = OrderBook()
    max_cost_records = []

    for line in get_args().file:
        operation = parse_operation_params(line)

        if operation.kind == OperationKind.INSERT:
            order_book.add_order(Order(timestamp=operation.timestamp,
                                       identifier=operation.order_id,
                                       cost=operation.cost))
        else:
            order_book.remove_order(operation.order_id)

        max_cost_records.append(
            MaxCostRecord(timestamp=operation.timestamp,
                          max_cost=order_book.get_current_max_cost())
        )

    max_cost_intervals = get_max_cost_intervals(max_cost_records)
    print(get_time_weighted_average_maximum_cost(max_cost_intervals))
