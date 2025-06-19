class PaymentFailedException(Exception):
    def __init__(self, message="Оплата не прошла. Повторите попытку или используйте другой способ оплаты."):
        self.message = message
        super().__init__(self.message)
