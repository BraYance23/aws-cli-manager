import threading
import logging
from ui.messages import print_message,spinner
from controllers.deploy_flow import build_instance_config
from ui import prompt_general,tables
from data import data_ec2
from exceptions import InvalidOperation_EC2



logger = logging.getLogger(__name__)

class EC2Controller:

    def __init__(self,manager_root):
        self.manager_root = manager_root
        pass

    def _validate_state(self,instance_state,operation):

         operation_selected = data_ec2.permissions_ec2[operation]
         permissions = operation_selected["permissions"]
         message = operation_selected["message"]

         if instance_state in permissions:
              return 
         raise InvalidOperation_EC2(message=message,instance_state=instance_state)
         
    def wait_with_spinner(self,msg_init,msg_success,list_instance_id,target_state):

        stop_spinner = threading.Event()
        hilo_spinner = threading.Thread(target=spinner,args=(stop_spinner,msg_init))
        hilo_spinner.start()

        try:
            correct_operation = self.manager_root.ec2.waiter_for_state(list_instance_id,target_state)
        finally:
            stop_spinner.set()
            hilo_spinner.join()

        if not correct_operation:
                        print_message(f"No se pudo verificar el estado de la instancia, por favor validar su estado  |1-Listar instancias",style_message="red italic")
                        return False
        
        for instance_id in list_instance_id:
            logger.info(f"{msg_success} | ID : {instance_id}")
        print_message(message=msg_success,style_message="green italic")
        return True
        
    def run_ec2(self):
        
        while True:

            name_instance,config_instace = build_instance_config(manager_root=self.manager_root)
            prompt_general.build_panel_deploy_ec2(data=config_instace,name_instance=name_instance)
            confirmation = prompt_general.confirmation_config(data=config_instace)
            match confirmation:
                 case "confirm":
                      break
                 case "retry":
                      continue

        response = self.manager_root.ec2.run_ec2(config_instace)
        self.wait_with_spinner(msg_init=" 🚀-Desplegando instancia...",
                                msg_success="Instancia desplegada con extio",
                                target_state="running",
                                list_instance_id=response)
        
    def _preparate_data(self):

        response = self.manager_root.ec2.describe_ec2()
        dict_id_ec2,list_rows = self.manager_root.ec2.format_data_ec2(response)
        return dict_id_ec2,list_rows

    def _show_instances(self,list_rows:list):

        print("\n\n")
        tables.print_table_ec2(list_rows=list_rows,title="Listado de instancias")

    def show_instaces(self):

         dict_id_ec2,list_rows = self._preparate_data()
         self._show_instances(list_rows=list_rows)

    def operation_ec2(self,selection):

        dict_id_ec2,list_rows = self._preparate_data()
        self._show_instances(list_rows=list_rows)
        
        data_instace = prompt_general.choice_options_table(dict_id_ec2,context="de la instancia deseada")
        instance_state = data_instace["instance_state"]
        instance_id = data_instace["instance_id"]

        self._validate_state(instance_state=instance_state,operation=selection)
        msg_init,target_state,msg_finally = data_ec2.parameter_operation_ec2[selection]
        if target_state == "terminated":
            prompt_general.confirmation()

        metodos_ec2 = {
            "3": self.manager_root.ec2.init_ec2,
            "4": self.manager_root.ec2.reboot_ec2,
            "5": self.manager_root.ec2.stop_ec2,
            "6": self.manager_root.ec2.terminate_ec2
            }
        response = [metodos_ec2[selection](instance_id)]
        self.wait_with_spinner(msg_init=msg_init,
                                msg_success=f"{msg_finally}",
                                target_state=target_state,
                                list_instance_id=response)
