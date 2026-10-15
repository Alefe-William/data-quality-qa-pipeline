-- Cenário 9: data inválida.
-- Venda 9012 no futuro (2030) e venda 9013 muito antiga (1999),
-- ambas fora do período esperado.
INSERT INTO fact_sales VALUES (9012, 1, DATE '2030-01-01', 40.00, 'completed');
INSERT INTO fact_sale_items VALUES (90012, 9012, 1, 1, 40.00, 40.00);

INSERT INTO fact_sales VALUES (9013, 1, DATE '1999-12-31', 40.00, 'completed');
INSERT INTO fact_sale_items VALUES (90013, 9013, 1, 1, 40.00, 40.00);