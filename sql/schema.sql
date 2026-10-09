-- Schema do Data Warehouse ShopData.
--
-- Chaves primárias (PK) e estrangeiras (FK) estão apenas DOCUMENTADAS aqui.
-- Elas não são impostas pelo banco de propósito: o objetivo do projeto é
-- detectar violações com testes de qualidade, e para isso precisamos conseguir
-- carregar dados inválidos.

-- Ordem de remoção: primeiro as tabelas que dependem de outras (fatos),
-- depois as dimensões. Isso torna o script reexecutável.
DROP TABLE IF EXISTS fact_sale_items;
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_customer;

-- Quem compra.
CREATE TABLE dim_customer (
    customer_id    INTEGER,        -- PK
    customer_name  VARCHAR,
    email          VARCHAR,
    city           VARCHAR,
    state          VARCHAR,
    created_at     DATE
);

-- O que é vendido.
CREATE TABLE dim_product (
    product_id    INTEGER,         -- PK
    product_name  VARCHAR,
    category      VARCHAR,
    unit_price    DECIMAL(10, 2)
);

-- Cada venda (cabeçalho do pedido).
CREATE TABLE fact_sales (
    sale_id       INTEGER,         -- PK
    customer_id   INTEGER,         -- FK -> dim_customer.customer_id
    sale_date     DATE,
    total_amount  DECIMAL(12, 2),
    status        VARCHAR
);

-- Cada item dentro de uma venda.
CREATE TABLE fact_sale_items (
    sale_item_id  INTEGER,         -- PK
    sale_id       INTEGER,         -- FK -> fact_sales.sale_id
    product_id    INTEGER,         -- FK -> dim_product.product_id
    quantity      INTEGER,
    unit_price    DECIMAL(10, 2),
    total_item    DECIMAL(12, 2)
);