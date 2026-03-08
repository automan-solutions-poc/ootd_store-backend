import pytest
from app.schemas.product import ProductCreate

def test_product_schema_validation():
    # Valid
    p = ProductCreate(name="Test", variants=[{"sku": "T1", "price": 10.0}])
    assert p.name == "Test"

def test_order_schema_validation():
    from app.schemas.order import OrderCreate
    # Valid
    o = OrderCreate(items=[{"sku": "S1", "quantity": 2}])
    assert len(o.items) == 1
    assert o.items[0].sku == "S1"
