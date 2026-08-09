import time
import logging
from config import logging_config
from core.manage_key_pair import ManageKeyPairs
from core.manage_sg import ManageSecurityGroup
from core.manage_ami import ManageAmi
from core.manage_ec2 import ManageEc2
from core.aws_profiles import build_session
from controllers import menu_services
from ui.messages import print_message,handle_aws_error
from ui.tables import select_region_name,select_profile
import exceptions

logging_config.setup_logging()
logger = logging.getLogger(__name__)

class ManagerAWS:

    def __init__(self,session_root,region_name:str="us-east-1"):
        self.session_root = session_root
        self.region_name = region_name
        self.ec2 = ManageEc2(session_root=session_root,region_name=region_name)
        self.ami = ManageAmi(session_root=session_root,region_name=region_name)
        self.key_pair = ManageKeyPairs(session_root=session_root,region_name=region_name)
        self.sg = ManageSecurityGroup(session_root=session_root,region_name=region_name)

def main():

        manager_root = None
        ask_profile = True
        build_manager = True

        while True:
            try:
                if build_manager:
                    if ask_profile:
                        profile = select_profile()
                        ask_profile = False

                    region_name,location_name = select_region_name()
                    session_root = build_session(profile=profile,region_name=region_name)
                    manager_root = ManagerAWS(session_root=session_root,region_name=region_name)
                    print_message(message="\nValidando credenciales...\nConectando con AWS...",style_message="green italic")
                    time.sleep(1)

                    response = manager_root.ec2.verify_identity()
                    arn_list = response["Arn"].split("/")
                    account_data = (response["Account"],arn_list[1],location_name,region_name)
                    print_message("Conexion exitosa :D\n\n",style_message="bold bright_white")

                response_program = menu_services.root_menu(account_data=account_data,manager_root=manager_root)
                match response_program:
                    case "change region":
                        build_manager = True
                        ask_profile = False
                    case "change profile":
                        build_manager = True
                        ask_profile = True
                    case "exit program":
                        return
                
            except exceptions.UserCancelOperation:
                build_manager = False
                if manager_root is None:
                    print_message(message="Seleccion cancelada, cerrando programa...",style_message="yellow italic")
                    return
                print_message(message="\n\nCambio cancelado, volviendo al menu anteior\n",style_message="yellow italic")
  
            except exceptions.CredentialsError as e:
                handle_aws_error(code=e.code)
                return
            except exceptions.AWSError as e:
                handle_aws_error(code=e.code)
                return
            except KeyboardInterrupt:
                return

                                         
if __name__ == "__main__":
    main()