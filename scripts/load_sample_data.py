"""Recria o warehouse e carrega os dados de exemplo.

Uso:
    python scripts/load_sample_data.py
    python scripts/load_sample_data.py --scenario duplicate_sale
    python scripts/load_sample_data.py --list-scenarios
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.database.connection import (  # noqa: E402
    get_connection,
    get_warehouse_path,
    initialize_schema,
)
from src.ingestion.load_data import (  # noqa: E402
    apply_scenario,
    list_scenarios,
    load_csv_folder,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Lê os argumentos de linha de comando."""
    parser = argparse.ArgumentParser(description="Load sample data into the warehouse.")
    parser.add_argument(
        "--scenario",
        choices=list_scenarios(),
        help="Inject a data-quality defect on top of the clean data.",
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="Show the available scenarios and exit.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Recria o schema, carrega os CSVs e aplica o cenário, se pedido."""
    args = parse_args(argv)

    if args.list_scenarios:
        for name in list_scenarios():
            print(name)
        return 0

    warehouse_path = get_warehouse_path()
    with get_connection(warehouse_path) as connection:
        initialize_schema(connection)
        try:
            counts = load_csv_folder(connection)
        except FileNotFoundError as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1

        if args.scenario:
            apply_scenario(connection, args.scenario)

    print(f"Database: {warehouse_path}")
    print("Clean data loaded:")
    for table, rows in counts.items():
        print(f"  - {table}: {rows} rows")
    if args.scenario:
        print(f"Scenario applied: {args.scenario}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
