import logging
from config.menu_structure import main_kp_deploy
from ui.messages import print_message
from ui.menus import print_menu_deploy_kp
from ui import prompts
from ui.tables import tables_key_pair
from ui.panels import panels_key_pair
from exceptions import NoKeyPairs



logger = logging.getLogger(__name__)

class KPController:

    def __init__(self,manager_root):
        self.manager_root = manager_root

    def show_key_pairs(self):

        response = self.manager_root.key_pair.request_key_pairs()
        dict_id_key,list_rows = self.manager_root.key_pair.format_data(response)
        tables_key_pair.print_table_kp(title="Llaves SSH existentes",list_rows=list_rows)

    def select_key_pair(self,context:str)-> bool|None|str:

        response = self.manager_root.key_pair.request_key_pairs()
        dict_key,list_rows = self.manager_root.key_pair.format_data(response)
        tables_key_pair.print_table_kp(title="Llaves SSH existentes",list_rows=list_rows)
        return prompts.choice_options_table(dict_data=dict_key,context=f"de la llave de SSH que desea {context} ")
        
    def generate_key_pairs(self):

        name_key = prompts.request_name_key()
        private_key = self.manager_root.key_pair.generate_key_pair(name_key)
        response_save_key = self.manager_root.key_pair.save_key_pair(private_key,name_key)
        logger.info(f"llave SSH creada con exito | nombre de la llave : {name_key}")
        print_message(f"💾-Llave guardada con exito en : {response_save_key}",style_message="green italic")
        return name_key

    def delete_key_pairs(self):
  
        key_selected  = self.select_key_pair(context="eliminar")
        panels_key_pair.build_panel_destroy_kp(data=key_selected)
        prompts.confimation_operation_destroy()
        key_name = key_selected["KeyName"]
        self.manager_root.key_pair.delete_key_pair(key_name)
        logger.info(f"Llave SSH eliminada con exito | Nombre de llave : {key_name} - ID : {key_selected["KeyPairId"]}")
        print_message(message=f"Llave SSH : '{key_name}.pem' eliminada con exito.",style_message="green italic")


    def resolve_kp_deploy(self):

        print_menu_deploy_kp()

        while True:
            selected_option = prompts.choice_options_menu(
                dict_options=(main_kp_deploy))

            match selected_option:
                        case "1":
                            return self.generate_key_pairs()
                        case "2":
                            try:
                                return self.select_key_pair(context="asociar a su instancia")["KeyName"]
                            except NoKeyPairs as e:
                                 print_message(message=str(e),style_message="yellow italic")