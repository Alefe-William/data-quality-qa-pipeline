"""Geração determinística dos dados fictícios da ShopData.

Com a mesma seed, os dados gerados são sempre idênticos. Isso torna os testes
reproduzíveis e permite versionar os CSVs no Git.
"""

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

SEED = 42
CUSTOMER_COUNT = 30
SALE_COUNT = 150
FIRST_SALE_ID = 1001
PERIOD_START = date(2026, 1, 1)
PERIOD_END = date(2026, 9, 30)

FIRST_NAMES = [
    "Ana", "Bruno", "Carla", "Diego", "Elisa", "Felipe", "Gabriela", "Hugo",
    "Igor", "Julia", "Lucas", "Marina", "Nicolas", "Olivia", "Paulo", "Rafael",
    "Sofia", "Tiago", "Vitor",
]  # fmt: skip
LAST_NAMES = [
    "Almeida", "Barbosa", "Cardoso", "Dias", "Esteves", "Ferreira", "Gomes",
    "Lima", "Martins", "Nunes", "Oliveira", "Pereira", "Ramos", "Santos",
    "Silva", "Soares", "Teixeira",
]  # fmt: skip
LOCATIONS = [
    ("São Paulo", "SP"),
    ("Rio de Janeiro", "RJ"),
    ("Belo Horizonte", "MG"),
    ("Curitiba", "PR"),
    ("Porto Alegre", "RS"),
    ("Salvador", "BA"),
    ("Recife", "PE"),
    ("Fortaleza", "CE"),
    ("Goiânia", "GO"),
    ("Brasília", "DF"),
]

# (nome, categoria, preço em centavos). O product_id é a posição na lista (1..20).
PRODUCTS = [
    ("Teclado Mecânico", "Periféricos", 24990),
    ("Mouse Sem Fio", "Periféricos", 8990),
    ("Mouse Gamer", "Periféricos", 15990),
    ("Webcam Full HD", "Periféricos", 19990),
    ("Headset USB", "Periféricos", 17990),
    ("Monitor 24 polegadas", "Monitores", 84990),
    ("Monitor 27 polegadas", "Monitores", 129990),
    ("Suporte para Monitor", "Monitores", 12990),
    ("SSD 480GB", "Armazenamento", 27990),
    ("SSD 1TB", "Armazenamento", 49990),
    ("HD Externo 1TB", "Armazenamento", 37990),
    ("Pen Drive 64GB", "Armazenamento", 4990),
    ("Mousepad Grande", "Acessórios", 5990),
    ("Hub USB-C", "Acessórios", 14990),
    ("Cabo HDMI 2m", "Acessórios", 3990),
    ("Carregador 65W", "Acessórios", 11990),
    ("Cadeira Ergonômica", "Mobiliário", 119990),
    ("Mesa Home Office", "Mobiliário", 89990),
    ("Luminária de Mesa", "Mobiliário", 6990),
    ("Apoio para Notebook", "Mobiliário", 7990),
]  # fmt: skip

STATUSES = ["completed", "pending", "cancelled"]
STATUS_WEIGHTS = [80, 12, 8]


def format_cents(cents: int) -> str:
    """Converte centavos inteiros em texto com 2 casas (24990 -> '249.90').

    Usar inteiros evita erros de arredondamento de ponto flutuante.
    """
    return f"{cents // 100}.{cents % 100:02d}"


def build_customers(rng: random.Random) -> pd.DataFrame:
    """Gera a dimensão de clientes (ids 1..CUSTOMER_COUNT)."""
    rows = []
    for customer_id in range(1, CUSTOMER_COUNT + 1):
        first_name = rng.choice(FIRST_NAMES)
        last_name = rng.choice(LAST_NAMES)
        city, state = rng.choice(LOCATIONS)
        created_at = date(2024, 1, 1) + timedelta(days=rng.randrange(730))
        rows.append(
            {
                "customer_id": customer_id,
                "customer_name": f"{first_name} {last_name}",
                "email": f"{first_name}.{last_name}.{customer_id}@example.com".lower(),
                "city": city,
                "state": state,
                "created_at": created_at.isoformat(),
            }
        )
    return pd.DataFrame(rows)


def build_products() -> pd.DataFrame:
    """Gera a dimensão de produtos (ids 1..len(PRODUCTS))."""
    rows = [
        {
            "product_id": product_id,
            "product_name": name,
            "category": category,
            "unit_price": format_cents(price_cents),
        }
        for product_id, (name, category, price_cents) in enumerate(PRODUCTS, start=1)
    ]
    return pd.DataFrame(rows)


def build_sales_and_items(rng: random.Random) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera vendas e itens de forma que todos os totais sejam consistentes."""
    sale_rows = []
    item_rows = []
    next_item_id = 1
    period_days = (PERIOD_END - PERIOD_START).days

    for offset in range(SALE_COUNT):
        sale_id = FIRST_SALE_ID + offset
        sale_date = PERIOD_START + timedelta(days=rng.randrange(period_days + 1))
        customer_id = rng.randint(1, CUSTOMER_COUNT)
        status = rng.choices(STATUSES, weights=STATUS_WEIGHTS)[0]
        product_ids = rng.sample(range(1, len(PRODUCTS) + 1), k=rng.randint(1, 4))

        sale_total_cents = 0
        for product_id in product_ids:
            quantity = rng.randint(1, 5)
            unit_price_cents = PRODUCTS[product_id - 1][2]
            item_total_cents = quantity * unit_price_cents
            sale_total_cents += item_total_cents
            item_rows.append(
                {
                    "sale_item_id": next_item_id,
                    "sale_id": sale_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": format_cents(unit_price_cents),
                    "total_item": format_cents(item_total_cents),
                }
            )
            next_item_id += 1

        sale_rows.append(
            {
                "sale_id": sale_id,
                "customer_id": customer_id,
                "sale_date": sale_date.isoformat(),
                "total_amount": format_cents(sale_total_cents),
                "status": status,
            }
        )

    return pd.DataFrame(sale_rows), pd.DataFrame(item_rows)


def write_sample_csvs(output_dir: Path) -> dict[str, int]:
    """Gera os dados e grava um CSV por tabela. Retorna linhas por tabela."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)

    customers = build_customers(rng)
    products = build_products()
    sales, items = build_sales_and_items(rng)

    tables = {
        "dim_customer": customers,
        "dim_product": products,
        "fact_sales": sales,
        "fact_sale_items": items,
    }
    for table_name, dataframe in tables.items():
        dataframe.to_csv(
            output_dir / f"{table_name}.csv",
            index=False,
            encoding="utf-8",
            lineterminator="\n",
        )
    return {name: len(dataframe) for name, dataframe in tables.items()}
