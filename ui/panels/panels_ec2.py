"""
Paneles de detalle para instancias EC2: despliegue y eliminación
"""
from ui.panels.base import print_detail_panel


def build_panel_deploy_ec2(data: dict, name_instance: str):

    print_detail_panel(
        title="🚀 Datos de instancia a desplegar",
        rows=[
            ("Tipo de máquina", data['InstanceType']),
            ("AMI ID", data['ImageId']),
            ("Nombre de instancia", name_instance),
            ("Llave SSH", data['KeyName']),
            ("Grupo de seguridad", data['SecurityGroupIds'][0]),
            ("Mínimo de instancias", data['MinCount']),
            ("Máximo de instancias", data['MaxCount']),
        ],
        label_style="bold green",
        value_style="white",
        border_style="green",
    )


def build_panel_destroy_ec2(data: dict):

    print_detail_panel(
        title=" Datos de instancia a eliminar",
        rows=[
            ("Nombre de la instancia", data['instance_name']),
            ("Tipo de instancia", data['instance_type']),
            ("Estado", data['instance_state']),
            ("Arquitectura", data['architecture']),
            ("Instancia ID", data['instance_id']),
            ("IP Publica", data['instance_ip']),
            ("Fecha de despliegue", data['time_launch']),
        ],
        label_style="bold green",
        value_style="dim magenta",
        border_style="green",
    )
