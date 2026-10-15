-- Cenário 1: venda duplicada.
-- Copia a venda 1001 inteira: o sale_id passa a existir duas vezes.
INSERT INTO fact_sales SELECT * FROM fact_sales WHERE sale_id = 1001;