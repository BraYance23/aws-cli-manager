"""
Configuración de operaciones EC2: parámetros, permisos y colores de estado
"""

parameter_operation_ec2 = {
    "3": ("📟 -Iniciando instancia","running","✅-Instancia iniciada correctamente."),
    "4": ("🔁 -Reiniciando instancia","status_ok","✅-Instancia reiniciada correctamente."),
    "5": ("🛑 -Deteniendo instancia","stopped","✅-Instancia detenenida correctamente."),
    "6": ("🗑️ -Eliminando instancia","terminated","✅-Instancia eliminada correctamente.")
}    

colors_state = {
    "running":  "[green]● Running[/green]",
    "stopped": "[red]● Stopped[/red]", 
    "terminated": "[red]● Terminated[/red]",  
    "pending": "[cyan]● Pending[/cyan]",
    "stopping": "[yellow]● Stopping[/yellow]",  
    "shutting-down": "[red]● Shutting-Down[/red]",
}

permissions_ec2 = {
    "3": {
        "permissions" :["stopped"],
          "message": "No se puede iniciar la instancia en el estado actual | estado de la instancia : "
          },
    "4":{
        "permissions":["running"],
        "message": "No se puede reiniciar la instancia en el estado actual | estado de la instancia : "
        },
    "5": {
        "permissions":["running"],
        "message": "No se puede detener la instancia en el estado actual | estado de la instancia : "
        },
    "6":{
        "permissions":["running","stopped"],
        "message":  "No se puede terminar la instancia en el estado actual | estado de la instancia : "
        }
    }