import enum
from collections import OrderedDict
from operator import attrgetter
from typing import Optional, List, Dict

from .exceptions import OrderBookException


class Order(object):
    def __init__(self, timestamp: int, identifier: int, cost: float) -> None:
        self.timestamp = timestamp
        self.identifier = identifier
        self.cost = cost

    def __str__(self):
        return f'Order: {self.identifier}'


class OrderBook(object):
    def __init__(self):
        self._current_max_cost: Optional[float] = None
        self._orders: Dict[int, Order] = OrderedDict()

    def add_order(self, order: Order) -> None:
        """
        Add order to order book
        :param order: Order to be added
        :return: None
        :raise OrderBookException: if an order with the same id already exists
        """
        if order.identifier in self._orders:
            raise OrderBookException(f'"{order}" already exist')

        self._orders[order.identifier] = order

        if (self._current_max_cost is None
                or order.cost > self._current_max_cost):
            self._current_max_cost = order.cost

    def remove_order(self, order_id: int) -> Order:
        """
        Remove order from order book by identifier
        :param order_id: identifier of order to be removed
        :return: removed order
        :raise OrderBookException: if an order does not exist
        """
        if order_id not in self._orders:
            error_message = f'Order with id={order_id} does not exist'
            raise OrderBookException(error_message)

        removed_order = self._orders.pop(order_id)

        if removed_order.cost == self._current_max_cost:
            self._current_max_cost = max(map(attrgetter('cost'),
                                             self._orders.values()),
                                         default=None)

        return removed_order

    def get_current_max_cost(self) -> Optional[float]:
        """
        Return current maximum cost of added (and not deleted) orders
        :return: current maximum cost or None if there are no orders
        """
        return self._current_max_cost

    def get_orders(self) -> List[Order]:
        """
        Return list of added (and not deleted) orders
        :return: list of orders
        """
        return list(self._orders.values())

    def __len__(self):
        return len(self._orders)


class MaxCostRecord(object):
    def __init__(self, timestamp: int, max_cost: Optional[float]) -> None:
        self.timestamp = timestamp
        self.max_cost = max_cost


class MaxCostInterval(object):
    def __init__(self,
                 timestamp_start: int,
                 timestamp_end: int,
                 max_cost: Optional[float]) -> None:
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.max_cost = max_cost

    @staticmethod
    def from_records(start_record: MaxCostRecord, end_record: MaxCostRecord):
        return MaxCostInterval(timestamp_start=start_record.timestamp,
                               timestamp_end=end_record.timestamp,
                               max_cost=start_record.max_cost)

    @property
    def duration(self):
        return self.timestamp_end - self.timestamp_start


class OperationKind(enum.Enum):
    INSERT = 'I'
    DELETE = 'E'


class Operation(object):
    def __init__(self,
                 timestamp: int,
                 kind: OperationKind,
                 order_id: int,
                 cost: Optional[float] = None) -> None:
        self.timestamp = timestamp
        self.kind = kind
        self.order_id = order_id
        self.cost = cost
