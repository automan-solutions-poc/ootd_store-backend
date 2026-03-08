class ExternalStubs:
    @staticmethod
    async def calculate_tax(amount: float, country: str):
        return amount * 0.1 # 10% tax stub

    @staticmethod
    async def get_shipping_rates(weight: float, destination: str):
        return [{"service": "Standard", "rate": 5.99}, {"service": "Express", "rate": 15.99}]

    @staticmethod
    async def create_payment_intent(amount: float, currency: str = "USD"):
        return {"payment_intent_id": "pi_stub_123", "client_secret": "secret_stub_123"}

    @staticmethod
    async def validate_address(address_data: dict):
        return {"valid": True, "standardized_address": address_data}

    @staticmethod
    async def detect_fraud(order_data: dict):
        return {"score": 0.0, "risk_level": "LOW"}

    @staticmethod
    async def convert_currency(amount: float, from_curr: str, to_curr: str):
        return amount * 1.0 # 1:1 stub

    @staticmethod
    async def get_geolocation(ip_address: str):
        return {"country": "US", "city": "New York"}
