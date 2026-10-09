"""Fixtures compartilhadas por todos os testes."""

from collections.abc import Iterator

import duckdb
import pytest

from src.database.connection import get_connection, initialize_schema


@pytest.fixture
def connection() -> Iterator[duckdb.DuckDBPyConnection]:
    """Banco DuckDB em memória, com o schema criado e as tabelas vazias.

    Cada teste recebe um banco novo e isolado, que é descartado no final.
    """
    conn = get_connection(":memory:")
    initialize_schema(conn)
    yield conn
    conn.close()
