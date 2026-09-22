"""
Paneles de confirmación con el detalle de lo que se va a crear o eliminar
"""
from ui.panels.panels_ec2 import build_panel_deploy_ec2, build_panel_destroy_ec2
from ui.panels.panels_key_pair import build_panel_destroy_kp
from ui.panels.panels_sg import build_panel_rules_sg

__all__ = [
    "build_panel_deploy_ec2", "build_panel_destroy_ec2",
    "build_panel_destroy_kp",
    "build_panel_rules_sg",
]
