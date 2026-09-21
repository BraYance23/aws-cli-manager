import logging
from typing import Callable
from config.menu_structure import main_sg_deploy
from ui.messages import print_message
from ui.menus import print_menu_deploy_sg
from ui import prompts, panels
from ui import tables
from utils.network import get_ip_public
from exceptions import NoEgressRules,NoIngressRules,NoVpc


logger = logging.getLogger(__name__)

class SGController:

    def __init__(self,manager_root):
        self.manager_root = manager_root

    def select_sg_id(self):

        response = self.manager_root.sg.get_sg_general()
        rich_rows,dict_sg_id = self.manager_root.sg.format_data_sg_general(response)
        tables.print_table_sg(list_rows=rich_rows)
        return prompts.choice_options_table(dict_data=dict_sg_id,context="del grupo de seguridad que desea administrar")

    def create_sg(self)-> str:

        description,group_name = prompts.request_data_sg_create()
        vpc_id = self.select_vpc_id()
        response = self.manager_root.sg.create_sg(description=description,
                                                  group_name=group_name,
                                                  vpc_id=vpc_id)
        sg_id = response["GroupId"]
        print_message(message=f"Grupo de seguridad creado con exito.\nSG ID : {sg_id}")
        logger.info(f"Grupo se seguridad creado con exito | SG ID : {sg_id} - {self.manager_root.region_name}")
        return sg_id
        
        
    def delete_sg(self):

        sg_id = self.select_sg_id()
        it_is_associated = self.manager_root.sg.is_sg_in_use(sg_id=sg_id)
        if it_is_associated:
            print_message(message=f"El grupo de seguridad : {sg_id} tiene recursos asociados, por lo cual no se puede eleminar.",
                          style_message="yellow italic")
            return

        response = self.manager_root.sg.delete_sg(sg_id=sg_id)
        print_message(message=f"Grupo de seguridad : {sg_id} eliminado con exito.",
                      style_message="green italic")
        logger.info(f"Grupo de seguridad : {sg_id} eliminado con exito de la region : {self.manager_root.region_name}")
        

    def select_vpc_id(self):

        response = self.manager_root.sg.get_vpcs()
        list_rows,dict_vpc_id = self.manager_root.sg.format_data_vpc(response=response)
        tables.print_table_vpc(list_rows=list_rows)
        selected_vpc_id = prompts.choice_options_table(dict_data=dict_vpc_id,
                                                              context="de la vpc que desea asociar a su SG ")
        return selected_vpc_id

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

    def select_sg_id(self)-> str:

        response = self.manager_root.sg.get_sg_general()

        list_rows,dict_sg_id = self.manager_root.sg.format_data_sg_general(response=response)
        tables.print_table_sg(list_rows=list_rows)

        selected_sg_id = prompts.choice_options_table(
            dict_data=dict_sg_id,
            context="del grupo de seguirdad que desea")
        return selected_sg_id

    def _get_ip_permissions(self)-> dict:

        ip_public = get_ip_public()
        while True:
            ip_permissions = prompts.request_ip_permissions(ip_public)
            panels.build_panel_rules_sg(data=ip_permissions,context="crear")
            confirmation = prompts.confirmation_config()   
            match confirmation:
                case "confirm":
                    return ip_permissions
                case "retry":
                    continue

    def _authorize_sg_rule(self,direction,autorize_func,action_name):

        ip_permissions = self._get_ip_permissions()
        response = autorize_func(ip_permissions)
        print_message(message=f"Puerto: {response['FromPort']} - {response["ToPort"]} abierto con exito en : {self.manager_root.sg.sg_id}",style_message="green italic")
        logger.info(f"{action_name} en SG ID: {self.manager_root.sg.sg_id} | Rule ID : {response["SecurityGroupRuleId"]}")
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
        selected_rule = prompts.choice_options_table(dict_data=dict_rules,context="de la regla de seguridad que desea eliminar ")
        return selected_rule

    def _revoke_sg_rule(self,direction:str,revoke_fun:Callable,action_name:str):

        selected_rule = self._get_rule_revoke(direction=direction)
        panels.build_panel_rules_sg(data=selected_rule,context="eliminar")
        prompts.confimation_operation_destroy()
        sg_rule_id = selected_rule["SecurityGroupRuleId"]
        response = revoke_fun(sg_rule_id)

        logger.info(f"{action_name} en SG ID : {self.manager_root.sg.sg_id} | Rule ID : {sg_rule_id}")
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


    def resolve_sg_deploy(self):

        print_menu_deploy_sg()

        while True:
            selected_vpc= prompts.choice_options_menu(
                dict_options=main_sg_deploy)

            match selected_vpc:
                        case "1":
                            return self.create_sg()
                        case "2":
                            try:
                                return self.select_sg_id()
                            except NoVpc as e:
                                    print_message(message=str(e),style_message="yellow italic")

    def change_sg_id(self):

        selected_sg_id = self.select_sg_id()
        self.manager_root.sg.sg_id = selected_sg_id
        return True
