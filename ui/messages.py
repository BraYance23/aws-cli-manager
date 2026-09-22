"""
Mensajes en consola: texto centrado, paneles, spinner y errores de AWS
"""
import time
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from config.error_messages import AWS_ERROR_MESSAGES
from ui.console import console

def print_message(message:str,style_message:str=""):

    console.print(f"\n{message}\n",style=style_message,justify="center")

def print_message_panel(color_panel:str,message:str,style_message:str=""):

    panel = Panel(f"{message}",border_style=color_panel,style=style_message)
    console.print(Align.center(panel))


def spinner(stop_event,text_spinner,):

    console = Console()
    spinnerr = Spinner("dots",text=f"[green]{text_spinner}[/green]",)
  
    spinnerr_center = Align.center(spinnerr)
    print()
    with Live(spinnerr_center,console=console,refresh_per_second=12):
        while not stop_event.is_set():
            time.sleep(0.3)


def handle_aws_error(code: str):
    message = AWS_ERROR_MESSAGES.get(code, f"Error inesperado: {code}")
    print_message(message, style_message="italic red")   
