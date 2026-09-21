"""
Menú principal: cabecera de bienvenida, datos de la cuenta, métricas y opciones
"""
from rich.columns import Columns
from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from ui.console import console


def build_metrics_budges(summary_total, widht_container_main):

    instance_on, instance_off = summary_total["summary_ec2"]
    sg_total = summary_total["summary_sg"]
    key_pairs_total = summary_total["summary_kp"]

    width_badge = widht_container_main // 3

    badge_ec2 = Panel(
        Align.center(f"[bold green]EC2:[/bold green] [green]●[/green] {instance_on} Running / [red]●[/red] {instance_off} Stopped"),
        border_style="green",
        width=width_badge,
        padding=(0, 0)
    )

    badge_sg = Panel(
        Align.center(f"[bold blue]SG:[/bold blue] {sg_total}"),
        border_style="blue",
        width=width_badge,
        padding=(0, 0)
    )

    badge_kp = Panel(
        Align.center(f"[bold yellow]Keys:[/bold yellow] {key_pairs_total}"),
        border_style="yellow",
        width=width_badge,
        padding=(0, 0)
    )

    columns_badge = Columns([badge_ec2, badge_sg, badge_kp])
    return columns_badge


def build_menu_panel(width_container_main):

    texto_opciones = Text.from_markup(
        "[green][1][/green] -> Administrar EC2\n"
        "[blue][2][/blue] -> Administrar Security Groups\n"
        "[yellow][3][/yellow] -> Administrar Key Pairs\n"
        "[cyan][4][/cyan] -> Cambiar de región\n"
        "[cyan][5][/cyan] -> Cambiar de perfil\n"
        "[red][6][/red] -> Salir"
    )

    panel_menu = Panel(
        Align.center(texto_opciones),
        title="[bold white]Menu de Acciones AWS[/bold white]",
        border_style="cyan",
        width=width_container_main,
        padding=(1, 0)
    )
    return panel_menu


def build_table_account(width_container, account_data):

    table_account = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_black",
        width=width_container
    )

    table_account.add_column("Account ID", justify="center", ratio=2)
    table_account.add_column("Profile IAM", justify="center", ratio=2)
    table_account.add_column("Location Name", justify="center", ratio=2)
    table_account.add_column("Region Name", justify="center", ratio=2)
    table_account.add_row(*account_data)
    return table_account


def print_root_menu(account_data, summary):

    console.clear()

    width_container = 110
    title = Text("Bienvenido a Manage AWS", style="bold cyan")
    subtitle = Text("Datos asociados a su cuenta de AWS", style="italic gray")

    rows_badge = build_metrics_budges(widht_container_main=width_container, summary_total=summary)
    panel_menu = build_menu_panel(width_container_main=width_container)
    table_account = build_table_account(width_container=width_container, account_data=account_data)

    console.print(Align.center(title))
    console.print(Align.center(subtitle))
    console.print(Align.center(table_account))
    console.print(Align.center(rows_badge))
    console.print(Align.center(panel_menu))
    console.print()
