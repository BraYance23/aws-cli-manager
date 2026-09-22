"""
Rejillas de selección de sesión: regiones de AWS y perfiles disponibles
"""
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from ui.console import console


def print_regions(title_regions, rows):

    grid = Table(show_header=False, show_edge=False, box=None, padding=(0, 2))
    grid.add_column("Col1")
    grid.add_column("Separador", justify="center")
    grid.add_column("Col2")

    cols = 2
    for i in range(0, len(rows), cols):
        chunk = rows[i : i + cols]

        r1 = chunk[0]
        cell1 = f"[bold cyan][ {r1['id']:02d} ][/bold cyan] [white]{r1['region_name']:<15}[/white] [dim magenta]<{r1['location_name']}>[/dim magenta]"

        if len(chunk) > 1:
            r2 = chunk[1]
            cell2 = f"[bold cyan][ {r2['id']:02d} ][/bold cyan] [white]{r2['region_name']:<15}[/white] [dim magenta]<{r2['location_name']}>[/dim magenta]"
            grid.add_row(cell1, "[dim cyan]│[/dim cyan]", cell2)
        else:
            grid.add_row(cell1, "", "")

    panel = Panel(
        Align.center(grid),
        title=f"[bold bright_white]{title_regions}[/bold bright_white]",
        border_style="cyan",
        padding=(1, 3),
        expand=False,
    )

    console.print(Align.center(panel))


def print_profiles(list_profile):

    grid = Table(
        title=False,
        show_header=False,
        show_edge=False,
        box=None,
        padding=(0, 2)
    )

    grid.add_column("indices")
    grid.add_column("profiles", justify="center")

    grid.add_row("1", "[italic bright_white](.env / variables de entorno)[/italic bright_white]")

    for profile in list_profile:
        grid.add_row(*profile, style="green italic")

    panel = Panel(
        Align.center(grid),
        title="🔐-Perfiles disponibles",
        border_style="cyan",
        padding=(1, 3),
        expand=False
    )

    console.print(Align.center(panel))
