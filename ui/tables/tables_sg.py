"""
Tablas de Security Groups: listado de grupos, reglas y VPCs asociables
"""
from ui.tables.base import print_table_panel

COLUMNS_SG = [
    ("#", {"width": 4}),
    ("Group ID", {"style": "italic"}),
    ("Group Name", {}),
    ("Description",{})
]

COLUMNS_RULES = [
    ("#", {}),
    ("Protocolo", {"style": "italic"}),
    ("Puerto inico", {}),
    ("Puerto fin", {}),
    ("CDIR IP", {"style": "bold"}),
    ("Descripción", {}),
]

COLUMNS_VPC = [
    ("#", {"width": 4}),
    ("VPC ID", {}),
    ("Estado", {}),
    ("CIDR BLOCK", {}),
]


def print_table_sg(list_rows: list):

    print_table_panel(
        title="Listado Security Groups",
        columns=COLUMNS_SG,
        rows=list_rows,
        header_style="bold blue",
        border_style="blue",
    )


def print_table_sg_rules(title: str, list_rows: list):

    print_table_panel(
        title=title,
        columns=COLUMNS_RULES,
        rows=list_rows,
        header_style="bold blue",
        border_style="blue",
    )


def print_table_vpc(list_rows: list):

    print_table_panel(
        title="VPC Disponibles",
        columns=COLUMNS_VPC,
        rows=list_rows,
        header_style="bold blue",
        border_style="blue",
    )
