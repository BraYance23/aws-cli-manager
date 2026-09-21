"""
Paneles de detalle para llaves SSH (Key Pairs)
"""
from ui.panels.base import print_detail_panel


def build_panel_destroy_kp(data: dict):

    print_detail_panel(
        title=" Datos de llave SSH a eliminar",
        rows=[
            ("Nombre de llave SSH", data['KeyName']),
            ("SSH ID", data['KeyPairId']),
            ("Fecha de creación", data['CreateTime']),
        ],
        label_style="bold yellow",
        value_style="white",
        border_style="yellow",
    )
