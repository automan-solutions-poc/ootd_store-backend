# Database Documentation

## Setup Queries

### 1. Create Database
```sql
CREATE DATABASE ecommerce;
```

### 2. Create Enums
```sql
CREATE TYPE userrole AS ENUM ('ADMIN', 'CUSTOMER');
CREATE TYPE orderstatus AS ENUM ('PENDING', 'CONFIRMED', 'FAILED', 'CANCELLED');
```

### 3. Create Tables
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role userrole NOT NULL DEFAULT 'CUSTOMER',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sku VARCHAR(100) UNIQUE NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    print_type_id VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    status orderstatus NOT NULL DEFAULT 'PENDING',
    qikink_order_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE NOT NULL,
    sku VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);
```

### 4. Create Indexes
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);
```

## Sample Inserts

```sql
-- Create an admin (password: admin123)
INSERT INTO users (id, email, password_hash, role)
VALUES ('550e8400-e29b-41d4-a716-446655440000', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/ZfG9fG7.E6.pI.G6q', 'ADMIN');

-- Create a product
INSERT INTO products (id, name, sku, price)
VALUES ('550e8400-e29b-41d4-a716-446655440001', 'Classic T-Shirt', 'TSHIRT-001', 19.99);
```

## Analytics Queries

### Total Revenue
```sql
SELECT SUM(total_amount) FROM orders WHERE status = 'CONFIRMED';
```

### Top Selling SKUs
```sql
SELECT sku, SUM(quantity) as total_sold
FROM order_items
GROUP BY sku
ORDER BY total_sold DESC
LIMIT 10;
```

### Orders per Customer
```sql
SELECT u.email, COUNT(o.id) as order_count
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.email
ORDER BY order_count DESC;
```

## ER Diagram Explanation
- **Users**: Central entity for authentication. Has a one-to-many relationship with Orders.
- **Products**: Contains catalog items. Linked to Order Items by SKU.
- **Orders**: Tracks customer purchases. Has a many-to-one relationship with Users.
- **Order Items**: Line items for each order. Has a many-to-one relationship with Orders (ON DELETE CASCADE).

## Migration Instructions
1. Configure `DATABASE_URL` in `.env`.
2. Run `alembic upgrade head`.
