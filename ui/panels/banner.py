from rich.text import Text
from ui.console import console


def display_banner():
    banner = Text.from_markup(
        "[bold cyan]╔════════════════════════════════════════════════════╗[/bold cyan]\n"
        "[bold cyan]║[/bold cyan]                                                  [bold cyan]║[/bold cyan]\n"
        "[bold cyan]║[/bold cyan]           [bold green]⚡ MANAGER AWS ⚡[/bold green]              [bold cyan]║[/bold cyan]\n"
        "[bold cyan]║[/bold cyan]                                                  [bold cyan]║[/bold cyan]\n"
        "[bold cyan]╠════════════════════════════════════════════════════╣[/bold cyan]\n"
        "[bold cyan]║[/bold cyan]  [dim italic]AWS Resource Management CLI by BraYance23[/dim italic]   [bold cyan]║[/bold cyan]\n"
        "[bold cyan]╚═══                                              ═══╝[/bold cyan]"
    )
    console.print(banner,justify="center")
    print()