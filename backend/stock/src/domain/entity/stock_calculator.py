from stock.src.domain.entity.stock_entry import StockEntry


class StockCalculator:

    @staticmethod
    def calculate(stock_entries: list[StockEntry]):
        total = 0
        for stock_entry in stock_entries:
            if stock_entry.operation == "in":
                total += stock_entry.quantity
            elif stock_entry.operation == "out":
                total -= stock_entry.quantity
        return total
