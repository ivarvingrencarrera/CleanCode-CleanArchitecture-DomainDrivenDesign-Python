from datetime import datetime


class Coupon:
    def __init__(self, code: str, percentage: float, expire_date: datetime) -> None:
        self.code = code
        self.percentage = percentage
        self.expire_date = expire_date

    def is_expired(self, today: datetime) -> bool:
        return self.expire_date < today

    def calculate_discount(self, amount: float) -> float:
        return (amount * self.percentage) / 100
