import unittest

from .exceptions import OrderBookException
from .models import OrderBook, Order, MaxCostRecord, MaxCostInterval
from .utils import (get_max_cost_intervals,
                    get_time_weighted_average_maximum_cost)


class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.order_book = OrderBook()
        self.order = Order(1, 1, 42.0)

    def test_add_order(self):
        self.order_book.add_order(self.order)
        self.assertEqual(len(self.order_book), 1)

    def test_add_already_exist_order(self):
        with self.assertRaises(OrderBookException) as raises_context_manager:
            self.order_book.add_order(self.order)
            self.order_book.add_order(self.order)

        self.assertIn('already exist', str(raises_context_manager.exception))

    def test_remove_order(self):
        self.order_book.add_order(self.order)
        removed_order = self.order_book.remove_order(self.order.identifier)
        self.assertEqual(removed_order, self.order)
        self.assertEqual(len(self.order_book), 0)

    def test_remove_does_not_exist_order(self):
        with self.assertRaises(OrderBookException) as raises_context_manager:
            self.order_book.remove_order(self.order.identifier)

        self.assertIn('does not exist', str(raises_context_manager.exception))

    def test_current_maximum_cost(self):
        self.assertIsNone(self.order_book.get_current_max_cost())
        self.order_book.add_order(self.order)
        self.assertEqual(self.order_book.get_current_max_cost(),
                         self.order.cost)
        self.order_book.remove_order(self.order.identifier)
        self.assertIsNone(self.order_book.get_current_max_cost())


class TestGetMaxCostIntervals(unittest.TestCase):
    def test_not_enough_records(self):
        intervals = list(get_max_cost_intervals([]))
        self.assertListEqual(intervals, [])

        intervals = list(get_max_cost_intervals([MaxCostRecord(1, 42.0)]))
        self.assertListEqual(intervals, [])

    def test_one_interval_from_two_records(self):
        first_record = MaxCostRecord(1, 42.0)
        second_record = MaxCostRecord(2, 1.0)

        intervals = list(get_max_cost_intervals([first_record, second_record]))

        self.assertEqual(len(intervals), 1)
        self.assertEqual(intervals[0].timestamp_start, first_record.timestamp)
        self.assertEqual(intervals[0].timestamp_end, second_record.timestamp)
        self.assertEqual(intervals[0].max_cost, first_record.max_cost)

    def test_one_interval_from_many_records(self):
        timestamp_start, timestamp_end = 1, 5
        cost = 42.0
        records = [MaxCostRecord(ts, cost)
                   for ts in range(timestamp_start, timestamp_end + 1)]

        intervals = list(get_max_cost_intervals(records))

        self.assertEqual(len(intervals), 1)
        self.assertEqual(intervals[0].timestamp_start, timestamp_start)
        self.assertEqual(intervals[0].timestamp_end, timestamp_end)
        self.assertEqual(intervals[0].max_cost, cost)

    def test_many_intervals_from_many_records(self):
        timestamp_start, timestamp_end = 1, 5
        start_cost = 42.0
        records = [MaxCostRecord(ts, start_cost * ts)
                   for ts in range(timestamp_start, timestamp_end + 1)]

        intervals = list(get_max_cost_intervals(records))

        self.assertEqual(len(intervals), len(records) - 1)
        for record_start, interval in zip(records, intervals):
            self.assertEqual(interval.max_cost, record_start.max_cost)
            self.assertEqual(interval.timestamp_start, record_start.timestamp)

        self.assertEqual(intervals[-1].timestamp_end, records[-1].timestamp)


class TestGetTimeWeightedAverageMaximumCost(unittest.TestCase):
    def test_empty_intervals(self):
        self.assertIsNone(get_time_weighted_average_maximum_cost([]))

    def test_one_interval(self):
        interval = MaxCostInterval(1, 2, 42.0)
        average_cost = get_time_weighted_average_maximum_cost([interval])
        self.assertAlmostEqual(average_cost, interval.max_cost)

    def test_many_intervals(self):
        intervals = [
            MaxCostInterval(1000, 2000, 10.0),
            MaxCostInterval(2000, 2500, 13.0),
            MaxCostInterval(2500, 4000, 10.0)
        ]
        average_cost = get_time_weighted_average_maximum_cost(intervals)
        self.assertAlmostEqual(average_cost, 10.5)

    def test_intervals_with_none_max_cost(self):
        intervals = [
            MaxCostInterval(1000, 2000, 13.0),
            MaxCostInterval(2000, 2500, None),
            MaxCostInterval(2500, 4000, 10.0)
        ]
        average_cost = get_time_weighted_average_maximum_cost(intervals)
        self.assertAlmostEqual(average_cost, 11.2)


if __name__ == '__main__':
    unittest.main()
