"""
Menús de la aplicación: dashboard principal y submenús por servicio
"""
from ui.menus.dashboard import print_root_menu
from ui.menus.menus_ec2 import print_menu_ec2
from ui.menus.menus_sg import print_menu_root_sg, print_menu_sg, print_menu_deploy_sg
from ui.menus.menus_key_pair import print_menu_kp, print_menu_deploy_kp

__all__ = [
    "print_root_menu",
    "print_menu_ec2",
    "print_menu_root_sg", "print_menu_sg", "print_menu_deploy_sg",
    "print_menu_kp", "print_menu_deploy_kp",
]
