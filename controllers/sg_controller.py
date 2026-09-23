import logging
from config.menu_structure import main_sg_deploy,main_create_rule
from config.dashboard_config import need_update_dashboard
from ui.messages import print_message
from ui.menus import menus_sg
from ui import prompts
from ui.panels import panels_sg
from ui.tables import tables_sg
from utils.network import get_ip_public,resolve_ip_permissions
from exceptions import NoEgressRules,NoIngressRules,NoVpc


logger = logging.getLogger(__name__)

class SGController:

    def __init__(self,manager_root):
        self.manager_root = manager_root

    def select_sg_id(self,context)->dict:

        response = self.manager_root.sg.get_sg_general()
        rich_rows,dict_sg_id = self.manager_root.sg.format_data_sg_general(response)
        tables_sg.print_table_sg(list_rows=rich_rows)
        return prompts.choice_options_table(dict_data=dict_sg_id,
                                            context=f"del grupo de seguridad que desea {context}")

    def create_sg(self)-> str:

        group_name,description = prompts.request_data_sg_create()
        vpc_id = self.select_vpc_id()
        response = self.manager_root.sg.create_sg(description=description,
                                                  group_name=group_name,
                                                  vpc_id=vpc_id)
        sg_id = response["GroupId"]
        print_message(message=f"\nGrupo de seguridad creado con exito.\nSG ID : {sg_id}\n",
                      style_message="green italic")
        logger.info(f"Grupo se seguridad creado con exito | SG ID : {sg_id} - {self.manager_root.region_name}")
        if self.authorize_sg_rule_automatic(sg_id=sg_id):
            print_message(message="Regla SSH asociado con exito al grupo de seguridad.",
                          style_message="green italic")
        need_update_dashboard(service="sg")
        return sg_id

    def validate_state_sg(self,sg_name)->bool:

        if sg_name == "default":
            
            print_message(
            message="\nEl grupo de seguridad 'default' es del sistema y AWS no permite eliminarlo.\n",
            style_message="yellow italic")
            return False
        return True
  
    def delete_sg(self):

        data_sg = self.select_sg_id(context="eliminar")
        sg_id,sg_name = data_sg["GroupId"],data_sg["GroupName"]
        sg_is_valid = self.validate_state_sg(sg_name=sg_name)
        if not sg_is_valid:
            return

        panels_sg.build_panel_sg(group_name=sg_name,sg_id=sg_id)
        prompts.confimation_operation_destroy()
        response = self.manager_root.sg.delete_sg(sg_id=sg_id)
        
        if sg_id == self.manager_root.sg.sg_id:
            self.manager_root.sg.clear_selection()
        
        print_message(message=f"\nGrupo de seguridad : {sg_id} eliminado con exito.\n",
                      style_message="green italic")
        logger.info(f"Grupo de seguridad : {sg_id} eliminado con exito de la region : {self.manager_root.region_name}")
        need_update_dashboard(service="sg")

    def authorize_sg_rule_automatic(self,sg_id:str)->bool:

        ip_public = get_ip_public()
        menus_sg.print_create_rule(ip_public=ip_public)
        choice_menu = prompts.choice_options_menu(
            dict_options=main_create_rule,
        )

        if choice_menu in ("1","2"):
            cidr_ip =  ip_public if choice_menu == "1" else "0.0.0.0/0"
            ip_permissions = resolve_ip_permissions(
                cidr_ip=cidr_ip
            )
            self.manager_root.sg.authorize_rule_ingress(
                sg_id=sg_id,
                ip_permissions=ip_permissions
            )
            return True

        elif choice_menu == "3":
            return False

    def select_vpc_id(self):

        response = self.manager_root.sg.get_vpcs()
        list_rows,dict_vpc_id = self.manager_root.sg.format_data_vpc(response=response)
        tables_sg.print_table_vpc(list_rows=list_rows)
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
                tables_sg.print_table_sg_rules(title="Reglas de entrada",list_rows=list_rows_ingress)
                return
            raise NoIngressRules(sg_id=self.manager_root.sg.sg_id,region=self.manager_root.region_name)

        elif direction == "egress":
            if list_rows_egress:
                print("\n\n")
                tables_sg.print_table_sg_rules(title="Reglas de salida",list_rows=list_rows_egress)
                return
            raise NoEgressRules(sg_id=self.manager_root.sg.sg_id,region=self.manager_root.region_name)

    def _get_ip_permissions(self)-> dict:

        ip_public = get_ip_public()
        while True:
            ip_permissions = prompts.request_ip_permissions(ip_public)
            panels_sg.build_panel_rules_sg(data=ip_permissions,context="crear")
            confirmation = prompts.confirmation_config()   
            match confirmation:
                case "confirm":
                    return ip_permissions
                case "retry":
                    continue
                
    def _get_rule_revoke(self,direction:str)-> str:

        response = self.manager_root.sg.get_sg_rules(self.manager_root.sg.sg_id)
        data_sg  = self.manager_root.sg.format_data_sg_rules(response)
        dict_rules = data_sg.get(f"dict_rules_{direction}")
        list_rows = data_sg[f"list_rows_{direction}"]
        direction_title = "entrada" if direction == "ingress" else "salida"
        tables_sg.print_table_sg_rules(
            title=f"Reglas de {direction_title}",
            list_rows=list_rows
        )
        selected_rule = prompts.choice_options_table(dict_data=dict_rules,context="de la regla de seguridad que desea eliminar ")
        return selected_rule

    def _authorize_sg_rule(self,direction):

        dict_func = {"ingress": self.manager_root.sg.authorize_rule_ingress,
                     "egress": self.manager_root.sg.authorize_rule_egress}

        ip_permissions = self._get_ip_permissions()
        func_core = dict_func[direction]
        response = func_core(sg_id=self.manager_root.sg.sg_id,
                                 ip_permissions=ip_permissions)
        print_message(
            message=f"Puerto: {response['FromPort']} - {response["ToPort"]} abierto con exito en : {self.manager_root.sg.sg_id}",
            style_message="green italic")
        logger.info(f"Authorize_{direction} en SG ID: {self.manager_root.sg.sg_id} | Rule ID : {response["SecurityGroupRuleId"]}")
        self.show_rules_sg(direction=direction)


    def _revoke_sg_rule(self,direction:str):

        dict_func = {"ingress": self.manager_root.sg.revoke_rule_ingress,
                     "egress": self.manager_root.sg.revoke_rule_egress}

        selected_rule = self._get_rule_revoke(direction=direction)
        panels_sg.build_panel_rules_sg(data=selected_rule,context="eliminar")
        prompts.confimation_operation_destroy()
        sg_rule_id = selected_rule["SecurityGroupRuleId"]
        func_core = dict_func[direction]
        response = func_core(sg_id=self.manager_root.sg.sg_id,
                              sg_rule_id=sg_rule_id)

        logger.info(f"Revoke_{direction} en SG ID : {self.manager_root.sg.sg_id} | Rule ID : {sg_rule_id}")
        print_message(
            message=f"Regla con protocolo : {response["IpProtocol"]} - Puerto : {response['ToPort']} eliminado con exito de SG ID: {self.manager_root.sg.sg_id}",
            style_message="green italic")


    def operation_rules_sg(self,operation,direction):

        dict_operation = {
            "Authorize": self._authorize_sg_rule,
            "Revoke":self._revoke_sg_rule,        
        }
        dict_operation[operation](
            direction=direction
            )

    def resolve_sg_deploy(self):

        menus_sg.print_menu_deploy_sg()

        while True:
            selected_vpc= prompts.choice_options_menu(
                dict_options=main_sg_deploy)

            match selected_vpc:
                        case "1":
                            return self.create_sg()
                        case "2":
                            try:
                                return self.select_sg_id(context="asociar a su instancia")
                            except NoVpc as e:
                                    print_message(message=str(e),style_message="yellow italic")

    def change_sg_id(self):

        selected_sg_id = self.select_sg_id(context="administrar")["GroupId"]
        self.manager_root.sg.sg_id = selected_sg_id
        return True
