"""
Configuración de tablas: headers y títulos para visualización
"""

headers_types_ec2 = {
    "header": [
        "INDICE",
        "Instancia",
        "vCPU",
        "RAM",
        "$/hora",
        "$/mes",
        "Free Tier"
    ],
    "title": "\tTipos de instancias disponibles y costes"
}

header_os_general = {
    "header": [
        "INDICE",
        "DISTRO",
        "ARQUITECTURA"
    ],
    "title": "Seleccione el tipo de sistema operativo que desea desplegar :"
}

header_os_version = {
    "header": [
        "INDICE",
        "Distros",
        "Arquitectura",
        "Distribuidor"
    ],
    "title": "Versiones del sistema operativo seleccionado : "
}

header_selected_ami = {
    "header": [
        "INDICE",
        "ID AMI",
        "Name ",
        "Architecture",
        "Free tier",
        "Date creation"
    ],
    "title": "AMIS disponible :"
}