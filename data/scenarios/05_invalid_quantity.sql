-- Cenário 5: quantidade inválida.
-- Venda 9005: quantity = 0. Venda 9006: quantity = -2.
-- Obs.: a venda 9006 também tem totais negativos, o que é consequência natural
-- de uma quantidade negativa.
INSERT INTO fact_sales VALUES (9005, 1, DATE '2026-05-12', 0.00, 'completed');
INSERT INTO fact_sale_items VALUES (90005, 9005, 1, 0, 50.00, 0.00);

INSERT INTO fact_sales VALUES (9006, 1, DATE '2026-05-13', -100.00, 'completed');
INSERT INTO fact_sale_items VALUES (90006, 9006, 1, -2, 50.00, -100.00);