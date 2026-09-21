"""
Entradas genéricas reutilizables: texto no vacío y números en un rango
"""
from rich.prompt import Prompt
from ui.console import console, center_text


def ask_data(context: str):

    while True:

        data = Prompt.ask(center_text(context)).strip()
        if data:
            return data
        console.print("No se aceptan valores vacios")


def ask_int(prompt: str, value_min: int = 1, value_max: int = 100, msg_max: str = "") -> int:

    while True:

        try:
            value = int(input(center_text(prompt)).strip())

            if value < value_min:
                console.print(f"El valor debe ser mayor o igual a : {value_min}", style="yellow italic", justify="center")
                continue

            elif value > value_max:
                console.print(f"\n{msg_max} {value_max}\n", style="yellow italic", justify="center")
                continue
            return value
        except ValueError:
            console.print("Solo ingresar valores numericos.", style="yellow italic", justify="center")
