import unittest

from stock.src.domain.entity.stock_entry import StockEntry



class TestEntryCalculator(unittest.TestCase):
    

    def test_must_not_create_negative_input(self) -> None:
        with self.assertRaises(ValueError) as context:
            StockEntry(1, "in", -1)
        self.assertEqual(str(context.exception), "Invalid quantity")

    
    
        

if __name__ == "__main__":
    unittest.main()
