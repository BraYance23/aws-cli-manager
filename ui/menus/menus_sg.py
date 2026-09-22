"""
Menús de administración de Security Groups: raíz, reglas de un SG y despliegue
"""
from rich.text import Text
from rich.table import Table
from ui.console import console
from ui.menus.base import print_menu_panel


def print_menu_root_sg():

    options_menu_root_sg = Text.from_markup(
        "[blue][1][/blue] Administrar reglas de un SG\n"
        "[blue][2][/blue] Crear nuevo SG\n"
        "[blue][3][/blue] Eliminar un SG\n"
        "[yellow][4][/yellow] Volver al menu principal"
    )

    print_menu_panel(
        content=options_menu_root_sg,
        title="Manager Security Groups",
        border_style="blue",
    )

def print_create_rule(ip_public:str):

    options_menu = Text.from_markup(
        f"[blue][1][/blue] Crear con IP Publica (solo tu) -> {ip_public}\n"
        "[blue][2][/blue] Crear abierta a cualquier red -> 0.0.0.0/0\n"
        "[yellow][3][/yellow] saltar creacion de regla para despues"
    )

    print_menu_panel(content=options_menu,
                     title="Creacion de regla SSH",
                     border_style="blue"
                     )


def print_menu_sg(sg_id: str, region_name: str):

    grid = Table(
        title=f"Operando sobre : [italic]{sg_id}[/italic] - Region : [italic]{region_name}[/italic]\n",
        show_header=False,
        show_edge=False,
        box=None,
        padding=(0, 2)
    )

    grid.add_column("colum1")
    grid.add_column("separador")
    grid.add_column("colum2")

    grid.add_row("[blue][1][/blue]Listar reglas de entrada", "[dim cyan]│[/dim cyan]", "[blue][2][/blue]Listar reglas de salida")
    grid.add_row("[blue][3][/blue]Agregar regla de entrada", "[dim cyan]│[/dim cyan]", "[blue][4][/blue]Agregar regla de salida")
    grid.add_row("[blue][5][/blue]Eliminar regla de entrada", "[dim cyan]│[/dim cyan]", "[blue][6][/blue]eliminar regla de salida")
    grid.add_row("[yellow][7][/yellow]Cambiar de Security Groups", "[dim cyan]│[/dim cyan]", "[yellow][8][/yellow]Volver al menu anterior")

    console.print("\n\n")
    print_menu_panel(
        content=grid,
        title="Manager Security Groups",
        border_style="blue",
        padding=(1, 3),
    )


def print_menu_deploy_sg():

    sg_menu_options = Text.from_markup(
        "[blue][1][/blue]    Crear security group\n"
        "[blue][2][/blue] Seleccionar security group"
    )

    print_menu_panel(
        content=sg_menu_options,
        title="Manager SG",
        border_style="blue",
    )


