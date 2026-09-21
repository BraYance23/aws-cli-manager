"""
Estructura de menús y opciones de la aplicación
"""

main_root = {
    "1": "Administrar EC2",
    "2": "Administar Security Groups",
    "3": "Administar Key Pairs",
    "4": "Cambiar de region",
    "5": "Cambiar de perfil",
    "6": "Salir"
}

main_ec2 = {
    "1": "Listar instancias",
    "2": "Desplegar instancia",
    "3": "Iniciar instancia",
    "4": "Reiniciar instancia",
    "5": "Detener instancia",
    "6": "Terminar instancia",
    "7": "Volver al menu principal"
}

main_sg = {
    "1": "Listar reglas de entrada",
    "2": "Listar reglas de salida",
    "3": "Agregar regla de entrada",
    "4": "Eliminar regla de entrada",
    "5": "Agregar regla de salida",
    "6": "Eliminar reglada de salida",
    "7": "Cambiar grupo de seguridad",
    "8": "Volver al menu principal"
}

main_key_pair = {
    "1": "Listar llaves SSH",
    "2": "Crear llave SSH",
    "3": "Eliminar llave SSH",
    "4": "Volver al menu principal"
}

main_root_sg = {
    "1": "Administrar reglas de un SG",
    "2": "Crear nuevo SG",
    "3": "Eliminar un SG",
    "0": "Volver al menu principal"
}

main_sg_deploy = {
    "1": "Crear nuevo grupo de seguridad",
    "2": "Seleccionar grupo de seguridad existente"
}

main_kp_deploy = {
    "1": "Crear nueva llave SSH",
    "2": "Seleccionar llave SSH existente"
}