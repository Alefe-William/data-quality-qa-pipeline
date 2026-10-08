"""Teste de fumaça: confirma que o ambiente está configurado corretamente."""

import duckdb
import pandas as pd


def test_duckdb_runs_in_memory_query() -> None:
    """DuckDB deve executar uma consulta SQL simples em memória."""
    connection = duckdb.connect(":memory:")
    result = connection.execute("SELECT 1 + 1 AS total").fetchone()

    assert result is not None, "A consulta não retornou nenhuma linha."
    assert result[0] == 2, f"Esperado 2, encontrado {result[0]}."


def test_duckdb_reads_pandas_dataframe() -> None:
    """DuckDB deve conseguir consultar um DataFrame do Pandas diretamente."""
    sales = pd.DataFrame({"sale_id": [1, 2, 3], "total_amount": [10.0, 20.0, 30.0]})
    connection = duckdb.connect(":memory:")

    total = connection.execute("SELECT SUM(total_amount) FROM sales").fetchone()

    assert total is not None
    assert total[0] == 60.0, f"Esperado 60.0, encontrado {total[0]}."
