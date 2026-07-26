import json
import logging
from ui.messages import print_message
from ui import prompt_general
from ui import tables
from utils.network import get_ip_public


logger = logging.getLogger(__name__)

class SGController:

    def __init__(self,manager_root):
        self.manager_root = manager_root

    def inject_sg_id(self):

        response = self.manager_root.sg.get_rules_sg()
        rich_rows,dict_sg_id = self.manager_root.sg.format_data_sg_general(response)
        tables.print_table_sg(title="Security Groups Existentes",list_rows=rich_rows)
        return prompt_general.choice_options_table(dict_data=dict_sg_id,context="del grupo de seguridad que desea administrar")
            
    def show_rules_sg(self,direction:str):

        response = self.manager_root.sg.get_rules_sg(self.manager_root.sg.sg_id)
        data_sg = self.manager_root.sg.formata_data_sg_rules(response)
        list_rows_ingress = data_sg["list_rows_ingress"]
        list_rows_egress = data_sg["list_rows_egress"]

        if direction ==  "ingress":
            if list_rows_ingress:
                print("\n\n")
                tables.print_table_sg_rules(title="Reglas de entrada",list_rows=list_rows_ingress)

        elif direction == "egress":
            if list_rows_egress:
                print("\n\n")
                tables.print_table_sg_rules(title="Reglas de salida",list_rows=list_rows_egress)

            
    def autorize_sg_ingress(self,direction):

        ip_public = get_ip_public()

        while True:
            ip_permissions = prompt_general.request_ip_permissions(ip_public)
            prompt_general.build_panel_rules_sg(data=ip_permissions)
            confirmation = prompt_general.confirmation_config(data=ip_permissions)   
            match confirmation:
                case "confirm":
                    break
                case "retry":
                    continue

        response = self.manager_root.sg.authorize_rule_ingress(ip_permissions)
        format_ip_permissions = json.dumps(ip_permissions,indent=2,default=str)   
        print_message(message=f"Puerto: {ip_permissions['FromPort']} abierto con exito en : {self.manager_root.sg.sg_id}",style_message="green italic")
        logger.info(f"Autorize_ingress en SG ID: {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        self.show_rules_sg(direction)

    def autorize_sg_egress(self,direction):

        ip_public = get_ip_public()

        while True:
            ip_permissions = prompt_general.request_ip_permissions(ip_public)
            prompt_general.build_panel_rules_sg(data=ip_permissions)
            confirmation = prompt_general.confirmation_config(func_panel_data=prompt_general.build_panel_desploy_sg,data=ip_permissions)
            
            match confirmation:
                case "confirm":
                    break
                case "retry":
                    continue

        response = self.manager_root.sg.authorize_rule_egress(ip_permissions)
        format_ip_permissions = json.dumps(ip_permissions,indent=2,default=str)   
        print_message(message=f"Puerto: {ip_permissions['FromPort']} abierto con exito en : {self.manager_root.sg.sg_id}",style_message="green italic")
        logger.info(f"Autorize_egress en SG ID: {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        self.show_rules_sg(direction)

    def revoke_sg_ingress(self,direction):

        response_get_rules = self.manager_root.sg.get_rules_sg(self.manager_root.sg.sg_id)
        data_sg  = self.manager_root.sg.formata_data_sg_rules(response_get_rules)
        dict_rules = data_sg.get("dict_rules_ingress")
        self.show_rules_sg(direction)
        selected_rule = prompt_general.choice_options_table(dict_data=dict_rules,context="de la regla de seguridad que desea eliminar ")

        selected_rule = prompt_general.confirmation() 
        response = self.manager_root.sg.remove_rule_ingress(selected_rule)
        format_ip_permissions = json.dumps(selected_rule,indent=2,default=str)
        logger.info(f"Revoke ingress en SG ID : {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        print_message(message=f"Puerto : {response['ToPort']} eliminado con exito de : {self.manager_root.sg.sg_id}",style_message="green italic")

    def revoke_sg_egress(self,direction):

        response_get_rules = self.manager_root.sg.get_rules_sg(self.manager_root.sg.sg_id)
        data_sg  = self.manager_root.sg.formata_data_sg_rules(response_get_rules)
        dict_rules = data_sg.get("dict_rules_egress")


        self.show_rules_sg(direction)
        selected_rule = prompt_general.choice_options_table(dict_data=dict_rules,context="de la regla de seguridad que desea eliminar ")
        prompt_general.confirmation()  
        response  = self.manager_root.sg.remove_rule_egress(selected_rule)
        format_ip_permissions = json.dumps(selected_rule,indent=2,default=str)
        logger.info(f"Revoke egress en SG ID : {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        print_message(message=f"Puerto : {response['ToPort']} eliminado con exito de : {self.manager_root.sg.sg_id}",style_message="green italic")

    def change_sg_id(self):

        selected_sg_id = self.inject_sg_id()
        self.manager_root.sg.sg_id = selected_sg_id
        return True
