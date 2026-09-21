"""
Prompts interactivos: selección de opciones, confirmaciones y captura de datos
"""
from ui.prompts.choices import choice_options_table, choice_options_menu, choice_profile
from ui.prompts.confirmations import confirmation_config, confimation_operation_destroy
from ui.prompts.inputs import ask_data, ask_int
from ui.prompts.forms import (
    request_ip_permissions, request_name_key,
    request_data_sg_create, request_data_config_ec2
)

__all__ = [
    "choice_options_table", "choice_options_menu", "choice_profile",
    "confirmation_config", "confimation_operation_destroy",
    "ask_data", "ask_int",
    "request_ip_permissions", "request_name_key",
    "request_data_sg_create", "request_data_config_ec2",
]
