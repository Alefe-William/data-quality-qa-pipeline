-- Cenário 8: campos obrigatórios nulos.
-- Venda 9009 sem customer_id, 9010 sem sale_date, 9011 sem total_amount.
INSERT INTO fact_sales VALUES (9009, NULL, DATE '2026-05-16', 40.00, 'completed');
INSERT INTO fact_sale_items VALUES (90009, 9009, 1, 1, 40.00, 40.00);

INSERT INTO fact_sales VALUES (9010, 1, NULL, 40.00, 'completed');
INSERT INTO fact_sale_items VALUES (90010, 9010, 1, 1, 40.00, 40.00);

INSERT INTO fact_sales VALUES (9011, 1, DATE '2026-05-17', NULL, 'completed');
INSERT INTO fact_sale_items VALUES (90011, 9011, 1, 1, 40.00, 40.00);