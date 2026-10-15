"""Fixtures compartilhadas por todos os testes."""

from collections.abc import Iterator
from pathlib import Path

import duckdb
import pytest

from src.database.connection import get_connection, initialize_schema
from src.ingestion.load_data import load_csv_folder
from src.ingestion.sample_data import write_sample_csvs


@pytest.fixture
def connection() -> Iterator[duckdb.DuckDBPyConnection]:
    """Banco DuckDB em memória, com o schema criado e as tabelas vazias.

    Cada teste recebe um banco novo e isolado, que é descartado no final.
    """
    conn = get_connection(":memory:")
    initialize_schema(conn)
    yield conn
    conn.close()


@pytest.fixture
def sample_connection(
    connection: duckdb.DuckDBPyConnection, tmp_path: Path
) -> duckdb.DuckDBPyConnection:
    """Banco em memória já carregado com a carga correta de exemplo.

    Os CSVs são gerados numa pasta temporária, então os testes não dependem
    dos arquivos de data/raw.
    """
    write_sample_csvs(tmp_path)
    load_csv_folder(connection, tmp_path)
    return connection
