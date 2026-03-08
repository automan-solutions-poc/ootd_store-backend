import pytest
from app.schemas.product import ProductCreate
from app.schemas.order import OrderCreate

def test_product_schema_validation():
    # Valid
    p = ProductCreate(name="Test", sku="T1", price=10.0)
    assert p.name == "Test"

    # Invalid price
    with pytest.raises(ValueError):
        ProductCreate(name="Test", sku="T1", price=-1.0)

def test_order_schema_validation():
    # Valid
    o = OrderCreate(items=[{"sku": "S1", "quantity": 2, "price": 5.0}])
    assert len(o.items) == 1
    assert o.items[0].sku == "S1"
