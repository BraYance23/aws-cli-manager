from controllers.ec2_controller import EC2Controller
from controllers.sg_controller import SGController
from controllers.kp_controller import KPController
from controllers.deploy_flow import select_sg_id
from ui import menus
from ui.messages import handle_aws_error,print_message
from ui.prompt_general import choice_options_menu,center_text
from data import data_ec2
import exceptions


def ec2_menu(manager_root):

    ec2_controller = EC2Controller(manager_root=manager_root)
    while True:

        try:
            options_ec2 =  data_ec2.main_ec2
            print("\n")
            menus.print_menu_ec2()
            choice_ec2 = choice_options_menu(options_ec2)

            match choice_ec2: 
                case "1":
                    ec2_controller.show_instaces()
                    input(center_text("Presione enter para continuar"))
                case "2":
                    ec2_controller.run_ec2()
                    data_ec2.dashboard_dirty["ec2"]["needs_update"] = True
                case "3" | "4" |"5" | "6":
                    change_dashboard = ec2_controller.operation_ec2(choice_ec2)
                    if change_dashboard:
                        data_ec2.dashboard_dirty["ec2"]["needs_update"] = True
                case "7":
                    break
        except exceptions.InvalidOperation_EC2 as e:
            print_message(str(e),style_message="yellow italic")
        except exceptions.NoEC2Instances as e:
            print_message(f"No hay instancias en la region : {e.region}",style_message="yellow italic")
        except exceptions.UserCancelOperation:
            print_message("operacion cancelada",style_message="yellow italic")
        except exceptions.AWSError as e:
            handle_aws_error(e.code)

def sg_menu(manager_root):

    sg_controller = SGController(manager_root=manager_root)
    while True:

        try:
            menus.print_menu_sg(sg_id=manager_root.sg.sg_id,region_name=manager_root.region_name)
            options_sg = data_ec2.main_sg
            choice_operation = choice_options_menu(dict_options=options_sg)

            match choice_operation:
                case "1":
                    sg_controller.show_rules_sg(direction="ingress")
                    input(center_text("Presione enter para continuar"))
                case "2":
                    sg_controller.show_rules_sg(direction="egress")
                    input(center_text("Presione enter para continuar"))    
                case "3":
                    sg_controller.authorize_sg_rule(direction = "ingress")
                case "4":
                    sg_controller.authorize_sg_rule(direction = "egress")
                case "5":
                    sg_controller.revoke_sg_rule(direction = "ingress")
                case "6":
                    sg_controller.revoke_sg_rule(direction = "egress")
                case "7":
                    sg_controller.change_sg_id()
                case "8":
                    break
        except exceptions.NoIngressRules as e:
            print_message(message = str(e),style_message="yellow italic")
        except exceptions.NoEgressRules as e:
             print_message(message = str(e),style_message="yellow italic")
        except exceptions.UserCancelOperation:
            print_message(message="operacion cancelada",style_message="yellow italic")
        except exceptions.AWSError as e:
            handle_aws_error(e.code)


def kp_menu(manager_root):

    kp_controller = KPController(manager_root=manager_root)
    while True:

        try:
            options_key_pair = data_ec2.main_key_pair
            menus.print_menu_kp(manager_root.region_name)
            choice_key_pair = choice_options_menu(dict_options=options_key_pair)

            match choice_key_pair:

                case "1":
                    kp_controller.show_key_pairs()
                    input(center_text("Presione enter para continuar"))
                case "2":
                    kp_controller.generate_key_pairs()
                    data_ec2.dashboard_dirty["kp"]["needs_update"] = True
                case "3":
                    kp_controller.delete_key_pairs()
                    data_ec2.dashboard_dirty["kp"]["needs_update"] = True
                case "4":
                    break
        except (PermissionError,OSError) as e:
            print_message(message=f"Error al intentar guardar la llave SSH,| {e.strerror}",style_message="italic red")
        except exceptions.NoKeyPairs as e:
            print_message(message=str(e))
        except exceptions.UserCancelOperation:
            print_message(message="operacion cancelada",style_message="italic yellow")
        except exceptions.AWSError as e:
            handle_aws_error(e.code)


def root_menu(account_data,manager_root):

    while True:

        try:

            summary_resources = get_summary_all(manager_root)
            menus.print_root_menu(account_data=account_data,summary=summary_resources)
            options_root = data_ec2.main_root
            choice_aws = choice_options_menu(dict_options=options_root)
            match choice_aws:

                case "1":
                    ec2_menu(manager_root)
                case "2":
                    if not manager_root.sg.sg_id:
                        if select_sg_id(manager_root=manager_root) == "cancel":
                            continue
                    sg_menu(manager_root)

                case "3":
                    kp_menu(manager_root)         
                case "4":
                    break
                case "5":
                    print_message(message=":D Hasta pronto...",style_message="green italic")
                    return True
        except exceptions.UserCancelOperation:
            print_message(message="Operacion cancelada",style_message="yellow italic")

def get_summary_all(manager_root):

    try:
        if data_ec2.dashboard_dirty["ec2"]["needs_update"]:
            instance_on, instance_off = manager_root.ec2.summary_ec2()
            data_ec2.dashboard_dirty["ec2"]["needs_update"] = False
            data_ec2.dashboard_dirty["ec2"]["last_summary"] = (instance_on,instance_off)
        instance_on,instance_off = data_ec2.dashboard_dirty["ec2"]["last_summary"]
    except exceptions.AWSError:
        instance_on, instance_off = "N/A", "N/A"

    try:
        if data_ec2.dashboard_dirty["sg"]["needs_update"]:
            sg_total = manager_root.sg.summary_sg()
            data_ec2.dashboard_dirty["sg"]["needs_update"] = False
            data_ec2.dashboard_dirty["sg"]["last_summary"] = sg_total
        sg_total = data_ec2.dashboard_dirty["sg"]["last_summary"]
    except exceptions.AWSError:
        sg_total = "N/A"

    try:
        if data_ec2.dashboard_dirty["kp"]["needs_update"]:
            key_pairs_total = manager_root.key_pair.summary_key_pairs()
            data_ec2.dashboard_dirty["kp"]["needs_update"] = False
            data_ec2.dashboard_dirty["kp"]["last_summary"] = key_pairs_total
        key_pairs_total = data_ec2.dashboard_dirty["kp"]["last_summary"]

    except exceptions.AWSError:
        key_pairs_total = "N/A"
    return {
        "instance_on": instance_on,
        "instance_off": instance_off,
        "sg_total": sg_total,
        "key_pairs_total": key_pairs_total
    }