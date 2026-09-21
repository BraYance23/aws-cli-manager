"""
Paneles de confirmación con el detalle de lo que se va a crear o eliminar
"""
from ui.panels.ec2 import build_panel_deploy_ec2, build_panel_destroy_ec2
from ui.panels.key_pair import build_panel_destroy_kp
from ui.panels.security_group import build_panel_rules_sg

__all__ = [
    "build_panel_deploy_ec2", "build_panel_destroy_ec2",
    "build_panel_destroy_kp",
    "build_panel_rules_sg",
]
