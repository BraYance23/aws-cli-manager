"""
Consola compartida de Rich y utilidades de alineación de texto
"""
from rich.console import Console

console = Console()


def center_text(text: str) -> str:
    width = console.size.width
    padding = max(0, (width - len(text)) // 2)
    return " " * padding + text
