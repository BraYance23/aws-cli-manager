"""
Paneles de detalle para reglas de Security Groups
"""
from ui.panels.base import print_detail_panel


def build_panel_rules_sg(data: dict, context: str):

    ip_protocol = data["IpProtocol"]
    from_port = data["FromPort"]
    to_port = data["ToPort"]
    for value in data["IpRanges"]:
        cdrip_ip = value["CidrIp"]
        description = value["Description"]

    print_detail_panel(
        title=f"🌐 Datos de reglas a {context}",
        rows=[
            ("Protocolo", ip_protocol),
            ("Puerto inicio", from_port),
            ("Puerto fin", to_port),
            ("Cdrip IP", cdrip_ip),
            ("Descripcion", description),
        ],
        label_style="bold blue",
        value_style="dim magenta",
        border_style="blue",
    )
