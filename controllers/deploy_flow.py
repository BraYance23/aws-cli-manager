from controllers.ami_controller import AmiController
from controllers.kp_controller import KPController
from controllers.sg_controller import SGController
from ui.prompt_general import request_data_config_ec2

def build_instance_config(manager_root) -> dict:

    ami_controller = AmiController(manager_root=manager_root)
    kp_controller = KPController(manager_root=manager_root)
    sg_controller = SGController(manager_root=manager_root)

    ami_id = ami_controller.get_ami_id()
    type_machine = ami_controller.select_type_ec2()
    key_pair_id = kp_controller.select_key_pair()
    sg_id = sg_controller.inject_sg_id()
    min_count,max_count,name_instance = request_data_config_ec2()

    return name_instance,{
        "ImageId": ami_id,
        "InstanceType": type_machine,
        "MinCount": min_count,
        "MaxCount": max_count,
        "KeyName": key_pair_id,
        "SecurityGroupIds": [sg_id],
        "TagSpecifications" : [
            {
                "ResourceType": "instance",
            "Tags": [{"Key": "Name", "Value": name_instance}]
        }
    ]
}

def select_sg_id(manager_root)-> str|bool:

    sg_controller = SGController(manager_root=manager_root)
    return sg_controller.change_sg_id()
