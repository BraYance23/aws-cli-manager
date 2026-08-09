import logging
from ui.messages import print_message,handle_aws_error
from ui import prompt_general
from ui import tables


logger = logging.getLogger(__name__)

class KPController:

    def __init__(self,manager_root):
        self.manager_root = manager_root

    def show_key_pairs(self):

        response = self.manager_root.key_pair.request_key_pairs()
        dict_id_key,list_rows = self.manager_root.key_pair.format_data(response)
        tables.print_table_kp(title="Llaves SSH existentes",list_rows=list_rows)

    def select_key_pair(self)-> bool|None|str:

        response = self.manager_root.key_pair.request_key_pairs()
        dict_key,list_rows = self.manager_root.key_pair.format_data(response)
        tables.print_table_kp(title="Llaves SSH existentes",list_rows=list_rows)
        return prompt_general.choice_options_table(dict_data=dict_key,context="de la llave de SSH que desea eliminar ")
        
    def generate_key_pairs(self):

        name_key = prompt_general.request_name_key()
        response_generate_key = self.manager_root.key_pair.generate_key_pair(name_key)
        response_save_key = self.manager_root.key_pair.save_key_pair(response_generate_key,name_key)
        print_message(f"💾-Llave guardada con exito en : {response_save_key}",style_message="green italic")

    def delete_key_pairs(self):
  
        key_selected  = self.select_key_pair()
        prompt_general.confirmation()
        delete_code = self.manager_root.key_pair.delete_key_pair(key_selected)
        logger.info(f"Se elimino la llave SSH : {key_selected}.pem")
        print_message(message=f"Llave SSH : '{key_selected}.pem' eliminada con exito.",style_message="green italic")