"""Testes do schema do Data Warehouse."""

import duckdb
import pytest

from src.database.connection import initialize_schema, list_tables

EXPECTED_COLUMNS: dict[str, list[str]] = {
    "dim_customer": [
        "customer_id",
        "customer_name",
        "email",
        "city",
        "state",
        "created_at",
    ],
    "dim_product": ["product_id", "product_name", "category", "unit_price"],
    "fact_sales": ["sale_id", "customer_id", "sale_date", "total_amount", "status"],
    "fact_sale_items": [
        "sale_item_id",
        "sale_id",
        "product_id",
        "quantity",
        "unit_price",
        "total_item",
    ],
}


def test_all_expected_tables_exist(connection: duckdb.DuckDBPyConnection) -> None:
    found = set(list_tables(connection))
    expected = set(EXPECTED_COLUMNS)

    assert found == expected, (
        f"Tables mismatch. Missing: {sorted(expected - found)}. "
        f"Unexpected: {sorted(found - expected)}."
    )


@pytest.mark.parametrize(("table", "expected_columns"), EXPECTED_COLUMNS.items())
def test_table_has_expected_columns(
    connection: duckdb.DuckDBPyConnection,
    table: str,
    expected_columns: list[str],
) -> None:
    rows = connection.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'main' AND table_name = ?
        ORDER BY ordinal_position
        """,
        [table],
    ).fetchall()
    found_columns = [row[0] for row in rows]

    assert found_columns == expected_columns, (
        f"Table {table} has unexpected columns.\n"
        f"Expected: {expected_columns}\n"
        f"Found: {found_columns}"
    )


@pytest.mark.parametrize("table", EXPECTED_COLUMNS)
def test_tables_start_empty(connection: duckdb.DuckDBPyConnection, table: str) -> None:
    row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()

    assert row is not None
    assert row[0] == 0, f"Table {table} should start empty, found {row[0]} rows."


def test_schema_can_be_applied_twice(connection: duckdb.DuckDBPyConnection) -> None:
    """Rodar o setup de novo não pode falhar nem duplicar tabelas."""
    initialize_schema(connection)

    assert len(list_tables(connection)) == len(EXPECTED_COLUMNS)


def test_schema_does_not_enforce_keys_on_purpose(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    """Documenta a decisão de design: o banco aceita chaves duplicadas.

    Se este teste falhar, alguém adicionou PRIMARY KEY ao schema e os cenários
    de dados inválidos deixam de poder ser carregados.
    """
    connection.execute(
        """
        INSERT INTO fact_sales VALUES
            (1, 10, DATE '2026-01-01', 100.00, 'completed'),
            (1, 10, DATE '2026-01-01', 100.00, 'completed')
        """
    )
    row = connection.execute("SELECT COUNT(*) FROM fact_sales").fetchone()

    assert row is not None
    assert row[0] == 2, "O schema deveria aceitar sale_id duplicado."
