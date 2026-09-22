"""
Tabla de llaves SSH (Key Pairs)
"""
from ui.tables.base import print_table_panel

COLUMNS = [
    ("#", {"width": 4}),
    ("Name Key", {}),
    ("Key ID", {}),
    ("Fecha de creacion", {}),
]


def print_table_kp(title: str, list_rows: list):

    print_table_panel(
        title=title,
        columns=COLUMNS,
        rows=list_rows,
        header_style="bold yellow",
        border_style="yellow",
    )
