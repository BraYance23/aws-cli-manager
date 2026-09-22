"""
Menús de administración de llaves SSH (Key Pairs): raíz y despliegue
"""
from rich.text import Text
from ui.menus.base import print_menu_panel


def print_menu_kp(region):

    kp_menu_options = Text.from_markup(
        f"[italic]Operando sobre la region[/italic] : [bold bright_white]{region}[/bold bright_white]\n\n"
        "[yellow][1][/yellow] -> Listar llaves SSH\n"
        "[yellow][2][/yellow] -> Crear llave SSH\n"
        "[yellow][3][/yellow] -> Eliminar llave SSH\n"
        "[red][4][/red] -> Volver al menu principal\n"
    )

    print_menu_panel(
        content=kp_menu_options,
        title="Manager Key Pairs",
        border_style="yellow",
    )


def print_menu_deploy_kp():

    kp_menu_options = Text.from_markup(
        "[yellow][1][/yellow] \t  Crear llave SSH\n"
        "[yellow][2][/yellow] Seleccionar llave SSH existente"
    )

    print_menu_panel(
        content=kp_menu_options,
        title="Manager Key Pairs",
        border_style="yellow",
    )
