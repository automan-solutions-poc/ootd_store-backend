import pytest
from app.schemas.product import ProductCreate

def test_enterprise_product_schema():
    data = {
        "name": "Enterprise T-Shirt",
        "variants": [
            {"sku": "TSH-RED-S", "price": 25.0, "size": "S", "color": "RED"},
            {"sku": "TSH-RED-M", "price": 25.0, "size": "M", "color": "RED"}
        ]
    }
    p = ProductCreate(**data)
    assert len(p.variants) == 2
    assert p.variants[0].sku == "TSH-RED-S"
