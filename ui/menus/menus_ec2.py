"""
Menú de administración de instancias EC2
"""
from rich.text import Text
from ui.menus.base import print_menu_panel


def print_menu_ec2():

    ec2_menu_options = Text.from_markup(
        "[green][1][/green] -> Listar instancias\n"
        "[green][2][/green] -> Desplegar instancias\n"
        "[green][3][/green] -> Iniciar instancia\n"
        "[green][4][/green] -> Reiniciar instancia\n"
        "[green][5][/green] -> Detener instancia\n"
        "[green][6][/green] -> Terminar instancia\n"
        "[yellow ][7][/yellow] -> Volver al menu principal\n")

    print_menu_panel(
        content=ec2_menu_options,
        title="Manager EC2",
        border_style="green",
    )
