"""Cria (ou recria) o Data Warehouse com as tabelas vazias.

Uso:
    python scripts/setup_database.py
"""

import sys
from pathlib import Path

# Permite executar o script diretamente: coloca a raiz do projeto no caminho
# de imports para que "from src..." funcione.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.database.connection import (  # noqa: E402
    get_connection,
    get_warehouse_path,
    initialize_schema,
    list_tables,
)


def main() -> int:
    """Cria o schema e mostra as tabelas criadas. Retorna o código de saída."""
    warehouse_path = get_warehouse_path()

    with get_connection(warehouse_path) as connection:
        initialize_schema(connection)
        tables = list_tables(connection)

    print(f"Database: {warehouse_path}")
    print(f"Tables created ({len(tables)}):")
    for table in tables:
        print(f"  - {table}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
