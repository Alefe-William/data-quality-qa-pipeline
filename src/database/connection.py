"""Conexão com o Data Warehouse DuckDB e criação do schema."""

import os
from pathlib import Path

import duckdb
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_FILE = PROJECT_ROOT / "sql" / "schema.sql"
DEFAULT_WAREHOUSE_PATH = "database/warehouse.duckdb"
IN_MEMORY = ":memory:"


def get_warehouse_path() -> Path:
    """Retorna o caminho do arquivo do warehouse.

    Lê WAREHOUSE_PATH do arquivo .env (ou do ambiente). Caminhos relativos são
    resolvidos a partir da raiz do projeto, então funcionam em qualquer pasta
    de onde o comando for executado, no Windows e no Linux.
    """
    load_dotenv(PROJECT_ROOT / ".env")
    raw_path = Path(os.getenv("WAREHOUSE_PATH", DEFAULT_WAREHOUSE_PATH))
    return raw_path if raw_path.is_absolute() else PROJECT_ROOT / raw_path


def get_connection(
    database: str | Path | None = None, read_only: bool = False
) -> duckdb.DuckDBPyConnection:
    """Abre uma conexão com o DuckDB.

    Args:
        database: caminho do arquivo, ou ":memory:" para um banco temporário
            em memória. Se omitido, usa o caminho configurado no .env.
        read_only: abre o arquivo apenas para leitura (útil nos testes de
            qualidade, que nunca devem alterar os dados).
    """
    if database is None:
        database = get_warehouse_path()

    if str(database) == IN_MEMORY:
        return duckdb.connect(IN_MEMORY)

    path = Path(database)
    if not read_only:
        path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(path), read_only=read_only)


def initialize_schema(
    connection: duckdb.DuckDBPyConnection, schema_file: Path = SCHEMA_FILE
) -> None:
    """Executa o schema.sql, (re)criando todas as tabelas vazias."""
    connection.execute(schema_file.read_text(encoding="utf-8"))


def list_tables(connection: duckdb.DuckDBPyConnection) -> list[str]:
    """Lista os nomes das tabelas existentes, em ordem alfabética."""
    rows = connection.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main'
        ORDER BY table_name
        """
    ).fetchall()
    return [row[0] for row in rows]
