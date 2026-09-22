"""
Tabla de instancias EC2
"""
from ui.tables.base import print_table_panel

COLUMNS = [
    ("#", {"width": 4}),
    ("Nombre", {"style": "italic"}),
    ("Tipo de instancia", {}),
    ("Estado", {}),
    ("Arquitectura", {}),
    ("ID instancia", {"style": "bold"}),
    ("IP Publica", {}),
    ("Fecha Despliegue", {}),
]


def print_table_ec2(title: str, list_rows: list):

    print_table_panel(
        title=title,
        columns=COLUMNS,
        rows=list_rows,
        header_style="bold cyan",
        border_style="green",
    )
