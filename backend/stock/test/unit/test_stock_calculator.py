import unittest

from stock.src.domain.entity.stock_calculator import StockCalculator
from stock.src.domain.entity.stock_entry import StockEntry


class TestStockCalculator(unittest.TestCase):
    

    def test_calculate_stock_for_single_item(self) -> None:
        stock_entries = [
            StockEntry(1, "in", 10),
            StockEntry(1, "out", 5),
            StockEntry(1, "in", 2),
        ]
        total = StockCalculator.calculate(stock_entries)
        self.assertEqual(total, 7)


if __name__ == "__main__":
    unittest.main()
