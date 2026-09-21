"""
Prompts de selección: elegir una opción de una tabla, de un menú o un perfil
"""
from rich.prompt import Prompt
from exceptions import UserCancelOperation
from ui.console import console, center_text


def choice_options_table(dict_data: dict, context: str) -> str:

    while True:

        choice = Prompt.ask(center_text(text=f"Ingrese el # {context} ('0' para cancelar)"))

        if not choice:
            console.print("\n[yellow italic]Valor ingresado vacio,por favor ingresar una opción.[/yellow italic]\n", justify="center")
            print()
            continue
        elif choice in dict_data:
            return dict_data[choice]
        elif choice == "0":
            raise UserCancelOperation()

        console.print("[yellow italic]\nValor ingresado no esta en el rango valido.[/yellow italic]\n", justify="center")


def choice_options_menu(dict_options: dict) -> str:

    while True:

        choice = Prompt.ask(center_text(text="Ingrese la opcion que desee"))
        if not choice:
            console.print("\n[yellow italic]Valor ingresado vacio,por favor ingresar una opción.[/yellow italic]\n", justify="center")
            continue
        elif not choice in dict_options:
            console.print("\n[yellow italic]Valor ingresado no esta en el rango valido.[/yellow italic]\n", justify="center")
            continue
        return choice


def choice_profile(dict_options):

    while True:

        selected_profile = Prompt.ask(center_text(text="Ingrese el # del perfil que desea  ('0' para cancelar) ")).strip()

        if selected_profile == "0":
            raise UserCancelOperation()

        elif selected_profile == "1":
            return "__env__"

        elif selected_profile not in dict_options:
            console.print("Valor ingresado no esta en el rango valido.", style="yellow italic", justify="center")
            continue
        return dict_options[selected_profile]
