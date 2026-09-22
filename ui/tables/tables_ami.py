"""
Tabla genérica para el flujo de despliegue: tipos de instancia, sistemas operativos y AMIs
"""
from ui.tables.base import print_table_panel


def print_table_ami(list_header: list, title: str, list_rows: list):

    print_table_panel(
        title=title,
        columns=[(header, {}) for header in list_header],
        rows=list_rows,
        header_style="bold blue",
        border_style="green",
    )
