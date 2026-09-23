"""
Configuración de operaciones SG: parámetros para la eleccion de operacion a ejecutar
"""

operations_and_directions = {
    "3": ("Authorize","ingress"),
    "4": ("Authorize","egress"),
    "5": ("Revoke","ingress"),
    "6": ("Revoke","egress")
}