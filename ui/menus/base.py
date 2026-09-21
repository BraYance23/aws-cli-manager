"""
Panel base de menú reutilizado por los submenús de cada servicio
"""
from rich.align import Align
from rich.panel import Panel
from ui.console import console


def print_menu_panel(content, title: str, border_style: str, padding: tuple = (1, 5)):

    panel = Panel(
        Align.center(content),
        title=f"[bold bright_white]{title}[/bold bright_white]",
        border_style=border_style,
        padding=padding,
        expand=False
    )

    console.print(Align.center(panel))
