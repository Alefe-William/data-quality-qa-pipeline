-- Cenário 2: cliente inexistente.
-- A venda 9002 referencia o customer_id 99999, que não existe em dim_customer.
INSERT INTO fact_sales VALUES (9002, 99999, DATE '2026-05-10', 100.00, 'completed');
INSERT INTO fact_sale_items VALUES (90002, 9002, 1, 2, 50.00, 100.00);