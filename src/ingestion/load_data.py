"""Carga dos CSVs e dos cenários de erro no Data Warehouse."""

from pathlib import Path

import duckdb

from src.database.connection import PROJECT_ROOT

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
SCENARIOS_DIR = PROJECT_ROOT / "data" / "scenarios"

# Dimensões antes dos fatos: é a ordem natural de carga em um warehouse.
LOAD_ORDER = ("dim_customer", "dim_product", "fact_sales", "fact_sale_items")


def count_rows(connection: duckdb.DuckDBPyConnection, table: str) -> int:
    """Conta as linhas de uma tabela."""
    row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return int(row[0]) if row else 0


def load_csv_folder(
    connection: duckdb.DuckDBPyConnection, folder: Path = RAW_DATA_DIR
) -> dict[str, int]:
    """Carrega um CSV por tabela (nome do arquivo = nome da tabela).

    Retorna a quantidade de linhas de cada tabela após a carga.

    Raises:
        FileNotFoundError: se algum CSV esperado não existir na pasta.
    """
    missing = [f"{t}.csv" for t in LOAD_ORDER if not (folder / f"{t}.csv").is_file()]
    if missing:
        raise FileNotFoundError(
            f"Missing CSV files in {folder}: {', '.join(missing)}. "
            "Run: python scripts/generate_sample_data.py"
        )

    counts: dict[str, int] = {}
    for table in LOAD_ORDER:
        csv_path = (folder / f"{table}.csv").as_posix().replace("'", "''")
        connection.execute(
            f"INSERT INTO {table} BY NAME "
            f"SELECT * FROM read_csv('{csv_path}', header = true)"
        )
        counts[table] = count_rows(connection, table)
    return counts


def _scenario_name(path: Path) -> str:
    """'01_duplicate_sale.sql' -> 'duplicate_sale'."""
    return path.stem.split("_", 1)[1]


def list_scenarios(directory: Path = SCENARIOS_DIR) -> list[str]:
    """Lista os nomes dos cenários de erro disponíveis, na ordem dos arquivos."""
    return [_scenario_name(path) for path in sorted(directory.glob("*.sql"))]


def apply_scenario(
    connection: duckdb.DuckDBPyConnection,
    name: str,
    directory: Path = SCENARIOS_DIR,
) -> None:
    """Injeta um cenário de dados inválidos sobre a carga atual.

    Raises:
        ValueError: se o nome do cenário não existir.
    """
    for path in sorted(directory.glob("*.sql")):
        if _scenario_name(path) == name:
            connection.execute(path.read_text(encoding="utf-8"))
            return
    available = ", ".join(list_scenarios(directory))
    raise ValueError(f"Unknown scenario '{name}'. Available: {available}")
