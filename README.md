# Clothing E-commerce API

Clean, scalable, production-ready FastAPI backend with layered architecture and RBAC.

## Features
- Enterprise Layered Architecture (API -> Service -> DB)
- Role-Based Access Control (Admin vs Customer)
- Async SQLAlchemy 2.0 with PostgreSQL
- JWT Authentication & Session Management
- Multi-Level Product Categories
- Product Variants (Sizes, Colors, Stock)
- Integrated Cart & Wishlist System
- Review & Rating System
- Advanced Search, Filtering, and Sorting
- Promo Code & Discount Engine
- RMA/Return Management
- Internal Fulfillment Service
- Address Management
- Email System with Background Tasks
- Webhook Event System
- Structured Logging & Monitoring
- Rate Limiting (Conceptual)
- Fraud Detection & Tax Calculation (Conceptual stubs)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Sample CURL Commands

### 1. Customer Registration
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "customer@example.com", "password": "password123", "role": "CUSTOMER"}'
```

### 2. Admin Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "admin123"}'
```

### 3. Admin: Create Product
```bash
curl -X POST "http://localhost:8000/api/v1/admin/products/" \
     -H "Authorization: Bearer <ADMIN_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"name": "Blue Hoodie", "sku": "HOODIE-BLUE", "price": 49.99, "description": "Comfortable blue hoodie"}'
```

### 4. Customer: Create Order
```bash
curl -X POST "http://localhost:8000/api/v1/customer/orders/" \
     -H "Authorization: Bearer <CUSTOMER_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"items": [{"sku": "HOODIE-BLUE", "quantity": 1}]}'
```

### 5. Admin: View Analytics
```bash
curl -X GET "http://localhost:8000/api/v1/admin/analytics/" \
     -H "Authorization: Bearer <ADMIN_TOKEN>"
```

### 6. Admin: Bulk Update Pricing
```bash
curl -X POST "http://localhost:8000/api/v1/admin/products/bulk-update-pricing?percentage_change=10" \
     -H "Authorization: Bearer <ADMIN_TOKEN>"
```
