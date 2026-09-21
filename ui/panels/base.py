"""
Panel base de detalle (campo / valor) reutilizado por los paneles de cada dominio
"""
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich import box
from ui.console import console


def print_detail_panel(rows: list[tuple[str, object]], title: str,
                       label_style: str, value_style: str, border_style: str):

    table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
        expand=True
    )

    table.add_column(
        "Campo",
        style=label_style,
        justify="right",
        no_wrap=True
    )

    table.add_column(
        "Valor",
        style=value_style
    )

    for label, value in rows:
        table.add_row(label, f"{value}")

    panel = Panel(
        table,
        title=f"[bold white]{title}[/bold white]",
        title_align="center",
        border_style=border_style,
        box=box.ROUNDED,
        padding=(1, 2),
    )

    console.print(
        Align.center(panel)
    )
