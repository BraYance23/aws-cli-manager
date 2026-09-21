"""
Tabla base con panel centrado reutilizada por los listados de cada dominio
"""
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from ui.console import console


def print_table_panel(title: str, columns: list[tuple[str, dict]], rows: list,
                      header_style: str, border_style: str):
    """
    columns: lista de (encabezado, opciones extra de add_column), ej. ("#", {"width": 4}).
    Todas las columnas se centran por defecto.
    """
    table = Table(
        box=box.DOUBLE_EDGE,
        show_lines=True,
        header_style=header_style
    )

    for header, options in columns:
        table.add_column(header, justify="center", **options)

    for row in rows:
        table.add_row(*row)

    panel = Panel(
        Align.center(table),
        title=f"[bold bright_white]{title}[/bold bright_white]",
        border_style=border_style,
        padding=(1, 3),
        expand=False
    )
    console.print(Align.center(panel))
