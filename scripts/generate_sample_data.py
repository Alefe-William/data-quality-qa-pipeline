"""Gera os CSVs de dados fictícios em data/raw.

Uso:
    python scripts/generate_sample_data.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.load_data import RAW_DATA_DIR  # noqa: E402
from src.ingestion.sample_data import write_sample_csvs  # noqa: E402


def main() -> int:
    """Gera os CSVs e mostra quantas linhas cada um recebeu."""
    counts = write_sample_csvs(RAW_DATA_DIR)

    print(f"CSV files written to: {RAW_DATA_DIR}")
    for table, rows in counts.items():
        print(f"  - {table}.csv: {rows} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
