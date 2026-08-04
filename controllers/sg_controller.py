import json
import logging
from typing import Callable
from ui.messages import print_message
from ui import prompt_general
from ui import tables
from utils.network import get_ip_public
from exceptions import NoEgressRules,NoIngressRules


logger = logging.getLogger(__name__)

class SGController:

    def __init__(self,manager_root):
        self.manager_root = manager_root

    def inject_sg_id(self):

        response = self.manager_root.sg.get_sg_general()
        rich_rows,dict_sg_id = self.manager_root.sg.format_data_sg_general(response)
        tables.print_table_sg(title="Security Groups Existentes",list_rows=rich_rows)
        return prompt_general.choice_options_table(dict_data=dict_sg_id,context="del grupo de seguridad que desea administrar")
            
    def show_rules_sg(self,direction:str):

        response = self.manager_root.sg.get_sg_rules(self.manager_root.sg.sg_id)
        data_sg = self.manager_root.sg.format_data_sg_rules(response)
        list_rows_ingress = data_sg["list_rows_ingress"]
        list_rows_egress = data_sg["list_rows_egress"]

        if direction ==  "ingress":
            if list_rows_ingress:
                print("\n\n")
                tables.print_table_sg_rules(title="Reglas de entrada",list_rows=list_rows_ingress)
                return
            raise NoIngressRules(sg_id=self.manager_root.sg.sg_id,region=self.manager_root.region_name)

        elif direction == "egress":
            if list_rows_egress:
                print("\n\n")
                tables.print_table_sg_rules(title="Reglas de salida",list_rows=list_rows_egress)
                return
            raise NoEgressRules(sg_id=self.manager_root.sg.sg_id,region=self.manager_root.region_name)


    def _get_ip_permissions(self)-> dict:

        ip_public = get_ip_public()
        while True:
            ip_permissions = prompt_general.request_ip_permissions(ip_public)
            prompt_general.build_panel_rules_sg(data=ip_permissions)
            confirmation = prompt_general.confirmation_config(data=ip_permissions)   
            match confirmation:
                case "confirm":
                    return ip_permissions
                case "retry":
                    continue

    def _authorize_sg_rule(self,direction,autorize_func,action_name):

        ip_permissions = self._get_ip_permissions()
        response = autorize_func(ip_permissions)

        format_ip_permissions = json.dumps(ip_permissions,default=str,indent=2)
        print_message(message=f"Puerto: {ip_permissions['FromPort']} abierto con exito en : {self.manager_root.sg.sg_id}",style_message="green italic")
        logger.info(f"{action_name} en SG ID: {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        self.show_rules_sg(direction=direction)

    def authorize_sg_rule(self,direction):

        if direction == "ingress":
            self._authorize_sg_rule(direction=direction,
                                   autorize_func=self.manager_root.sg.authorize_rule_ingress,
                                   action_name="Autorize_ingress")
        elif direction == "egress":
            self._authorize_sg_rule(direction=direction,
                                   autorize_func=self.manager_root.sg.authorize_rule_egress,
                                   action_name="Autorize_egress")

    def _get_rule_revoke(self,direction:str)-> str:

        response = self.manager_root.sg.get_sg_rules(self.manager_root.sg.sg_id)
        data_sg  = self.manager_root.sg.format_data_sg_rules(response)
        dict_rules = data_sg.get(f"dict_rules_{direction}")
        self.show_rules_sg(direction)
        selected_rule = prompt_general.choice_options_table(dict_data=dict_rules,context="de la regla de seguridad que desea eliminar ")
        return selected_rule

    def _revoke_sg_rule(self,direction:str,revoke_fun:Callable,action_name:str):

        selected_rule = self._get_rule_revoke(direction=direction)
        prompt_general.confirmation() 
        response = revoke_fun(selected_rule)
        format_ip_permissions = json.dumps(selected_rule,indent=2,default=str)
        logger.info(f"{action_name} en SG ID : {self.manager_root.sg.sg_id}\nRegla : {format_ip_permissions}")
        print_message(message=f"Regla con protocolo : {response["IpProtocol"]} - Puerto : {response['ToPort']} eliminado con exito de SG ID: {self.manager_root.sg.sg_id}",style_message="green italic")

    def revoke_sg_rule(self,direction):

        if direction == "ingress":
            self._revoke_sg_rule(direction="ingress",
                                 revoke_fun=self.manager_root.sg.revoke_rule_ingress,
                                 action_name="Revoke_ingress")
        elif direction == "egress":
            self._revoke_sg_rule(direction="egress",
                                 revoke_fun=self.manager_root.sg.revoke_rule_egress,
                                 action_name="Revoke_egress")


    def change_sg_id(self):

        selected_sg_id = self.inject_sg_id()
        self.manager_root.sg.sg_id = selected_sg_id
        return True
