-- Cenário 7: total da venda incorreto.
-- Itens: 50.00 + 30.00 + 20.00 = 100.00, mas total_amount = 120.00.
INSERT INTO fact_sales VALUES (9008, 1, DATE '2026-05-15', 120.00, 'completed');
INSERT INTO fact_sale_items VALUES (90081, 9008, 1, 1, 50.00, 50.00);
INSERT INTO fact_sale_items VALUES (90082, 9008, 2, 1, 30.00, 30.00);
INSERT INTO fact_sale_items VALUES (90083, 9008, 3, 1, 20.00, 20.00);