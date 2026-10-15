"""Testes da geração de dados, da carga dos CSVs e dos cenários de erro."""

from pathlib import Path

import duckdb
import pytest

from src.ingestion.load_data import (
    LOAD_ORDER,
    apply_scenario,
    count_rows,
    list_scenarios,
    load_csv_folder,
)
from src.ingestion.sample_data import (
    CUSTOMER_COUNT,
    PRODUCTS,
    SALE_COUNT,
    write_sample_csvs,
)

EXPECTED_SCENARIO_COUNT = 10


def total_rows(connection: duckdb.DuckDBPyConnection) -> int:
    return sum(count_rows(connection, table) for table in LOAD_ORDER)


def test_sample_data_generation_is_deterministic(tmp_path: Path) -> None:
    first_run = tmp_path / "first"
    second_run = tmp_path / "second"
    write_sample_csvs(first_run)
    write_sample_csvs(second_run)

    for table in LOAD_ORDER:
        first = (first_run / f"{table}.csv").read_bytes()
        second = (second_run / f"{table}.csv").read_bytes()
        assert first == second, f"{table}.csv differs between two generations."


def test_clean_data_loads_expected_row_counts(
    sample_connection: duckdb.DuckDBPyConnection,
) -> None:
    assert count_rows(sample_connection, "dim_customer") == CUSTOMER_COUNT
    assert count_rows(sample_connection, "dim_product") == len(PRODUCTS)
    assert count_rows(sample_connection, "fact_sales") == SALE_COUNT
    assert count_rows(sample_connection, "fact_sale_items") >= SALE_COUNT, (
        "Every sale should have at least one item."
    )


def test_load_fails_with_clear_message_when_csv_is_missing(
    connection: duckdb.DuckDBPyConnection, tmp_path: Path
) -> None:
    with pytest.raises(FileNotFoundError, match="generate_sample_data"):
        load_csv_folder(connection, tmp_path)


def test_ten_scenarios_are_available() -> None:
    scenarios = list_scenarios()

    assert len(scenarios) == EXPECTED_SCENARIO_COUNT, (
        f"Expected {EXPECTED_SCENARIO_COUNT} scenarios, found {scenarios}."
    )


@pytest.mark.parametrize("scenario", list_scenarios())
def test_scenario_injects_rows(
    sample_connection: duckdb.DuckDBPyConnection, scenario: str
) -> None:
    rows_before = total_rows(sample_connection)

    apply_scenario(sample_connection, scenario)

    rows_after = total_rows(sample_connection)
    assert rows_after > rows_before, (
        f"Scenario '{scenario}' did not add any rows "
        f"(before: {rows_before}, after: {rows_after})."
    )


def test_unknown_scenario_raises_value_error(
    sample_connection: duckdb.DuckDBPyConnection,
) -> None:
    with pytest.raises(ValueError, match="Unknown scenario"):
        apply_scenario(sample_connection, "does_not_exist")
