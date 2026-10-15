-- Cenário 10: pedido sem itens.
-- A venda 9014 existe, mas não há nenhum registro em fact_sale_items para ela.
INSERT INTO fact_sales VALUES (9014, 1, DATE '2026-05-18', 75.00, 'completed');