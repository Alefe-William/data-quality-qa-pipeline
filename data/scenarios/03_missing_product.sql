-- Cenário 3: produto inexistente.
-- O item 90003 referencia o product_id 99999, que não existe em dim_product.
INSERT INTO fact_sales VALUES (9003, 1, DATE '2026-05-11', 60.00, 'completed');
INSERT INTO fact_sale_items VALUES (90003, 9003, 99999, 2, 30.00, 60.00);