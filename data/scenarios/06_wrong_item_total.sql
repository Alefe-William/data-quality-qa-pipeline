-- Cenário 6: total do item incorreto.
-- 2 x 50.00 deveria ser 100.00, mas total_item = 80.00.
-- O total da venda foi mantido igual ao item, para isolar só este defeito.
INSERT INTO fact_sales VALUES (9007, 1, DATE '2026-05-14', 80.00, 'completed');
INSERT INTO fact_sale_items VALUES (90007, 9007, 1, 2, 50.00, 80.00);