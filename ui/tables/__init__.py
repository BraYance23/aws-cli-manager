"""
Tablas y rejillas de listado para cada servicio de AWS
"""
from ui.tables.tables_ec2 import print_table_ec2
from ui.tables.tables_key_pair import print_table_kp
from ui.tables.tables_sg import print_table_sg, print_table_sg_rules, print_table_vpc
from ui.tables.tables_ami import print_table_ami
from ui.tables.tables_session import print_regions, print_profiles

__all__ = [
    "print_table_ec2",
    "print_table_kp",
    "print_table_sg", "print_table_sg_rules", "print_table_vpc",
    "print_table_ami",
    "print_regions", "print_profiles",
]
