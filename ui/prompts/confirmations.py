"""
Prompts de confirmación: datos correctos (S/N) y operaciones destructivas
"""
from typing import Literal
from rich.prompt import Prompt
from exceptions import UserCancelOperation
from ui.console import console, center_text


def confirmation_config() -> Literal["confirm", "retry"]:

    while True:
        print("\n")
        confirmation_user = Prompt.ask(center_text(text="¿Los datos ingresados son correctos? [S/N] | [0] Volver al menú anterior ")).strip().upper()

        if confirmation_user not in ["S", "N", "0"]:
            console.print("Valor ingresado no valido, por favor confirmar operacion.", style="yellow italic", justify="center")
            continue

        if confirmation_user == "S":
            return "confirm"
        elif confirmation_user == "N":
            return "retry"
        raise UserCancelOperation()


def confimation_operation_destroy() -> bool:

    while True:

        choice = Prompt.ask(center_text("Esta acción es irreversible, desea continuar S/N ")).strip().upper()
        if choice == "S":
            return True
        elif choice == "N":
            raise UserCancelOperation()
        console.print("Valor ingresado no valido, por favor confirmar operacion.")
