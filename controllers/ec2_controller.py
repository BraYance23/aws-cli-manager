import threading
import logging
from ui.messages import print_message,spinner
from controllers.deploy_flow import build_instance_config
from ui import prompt_general,tables
from data import data_ec2



logger = logging.getLogger(__name__)

class EC2Controller:

    def __init__(self,manager_root):
        self.manager_root = manager_root
        pass

    def wait_with_spinner(self,msg_init,msg_succes,instance_id,target_state):

        stop_spinner = threading.Event()
        hilo_spinner = threading.Thread(target=spinner,args=(stop_spinner,msg_init))
        hilo_spinner.start()

        try:
            correct_operation = self.manager_root.ec2.waiter_for_state(instance_id,target_state)                
        finally:
            stop_spinner.set()
            hilo_spinner.join()

        if not correct_operation:
                        print_message(f"No se pudo verificar el estado de la instancia, por favor validar su estado  |1-Listar instancias",style_message="red italic")
                        return False
        logger.info(f"EC2 desplegado correctamente, ID : {instance_id}")
        print_message(message=msg_succes,style_message="green italic")
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
                                msg_succes="Instancia desplegada con extio\n",
                                target_state="running",
                                instance_id=response)

    def show_instances(self):

        response = self.manager_root.ec2.describe_ec2()
        dict_ec2_id,list_rows = self.manager_root.ec2.format_data_ec2(response)
        print("\n\n")
        tables.print_table_ec2(list_rows=list_rows,title="Listado de instancias")

    def operation_ec2(self,selection):

        response = self.manager_root.ec2.describe_ec2()
        dict_id_ec2,filas_tabulate = self.manager_root.ec2.format_data_ec2(response)
        self.show_instances()
        
        instance_id = prompt_general.choice_options_table(dict_id_ec2,context="de la instancia deseada")
        msg_init,target_state,msg_finally = data_ec2.pameter_operation_ec2[selection]
        if target_state == "terminated":
            prompt_general.confirmation()

        metodos_ec2 = {
            "3": self.manager_root.ec2.init_ec2,
            "4": self.manager_root.ec2.reboot_ec2,
            "5": self.manager_root.ec2.stop_ec2,
            "6": self.manager_root.ec2.terminate_ec2
            }
        response = metodos_ec2[selection](instance_id)
        self.wait_with_spinner(msg_init=msg_init,
                                msg_succes=f"{msg_finally}\n",
                                target_state=target_state,
                                instance_id=response)