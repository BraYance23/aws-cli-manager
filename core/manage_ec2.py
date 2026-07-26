import logging
import  time
import boto3
from botocore.exceptions import ClientError,NoCredentialsError,WaiterError
from exceptions import AWSError,CredentialsNotFound,NoEC2Instances
from data.data_ec2 import colors_state


logger = logging.getLogger(__name__)

class ManageEc2:


    def __init__(self,region_name = "us-east-1"):
        self.region_name = region_name
        self.ec2 = boto3.client("ec2",region_name = self.region_name)
       

    def describe_ec2(self)-> str:

        try:
            response = self.ec2.describe_instances()
            return response

        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)

    def verify_identity(self)-> dict:
        """
        Creamos cliente de STS para validar credenciales, antes de ejecutar
        metodos que llaman a la API de AWS.
        """
        try:
            sts = boto3.client("sts")
            response = sts.get_caller_identity()
            return response
        except NoCredentialsError as e:
            raise CredentialsNotFound("No se encontraron credenciales")
    

    def run_ec2(self,config:dict)-> str:

        type_machine = config.get("TypeMachine")
        ami_id = config.get("AmiId")
        name_instance = config.get("NameInstance")
        key_pair_name = config.get("KeyPairName")
        sg_id = config.get("SecurityGroupsId")
        min_count = config.get("MinCount")
        max_count = config.get("MaxCount")

        try:

            response = self.ec2.run_instances(
                ImageId = ami_id,
                InstanceType = type_machine,
                MinCount = min_count,
                MaxCount = max_count,
                KeyName = key_pair_name,
                SecurityGroupIds = [sg_id],
                TagSpecifications = [
                    {
                        "ResourceType": "instance",
                        "Tags": [{"Key": "Name", "Value": name_instance}]
                    }
                ]
            )

            return response.get("Instances")[0].get("InstanceId")

        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)
        
    def init_ec2(self,instance_id:str)-> str:

        try:
            self.ec2.start_instances(InstanceIds=[instance_id])
            return instance_id
           
        except ClientError  as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code)
        

    def reboot_ec2(self,instance_id:str)-> str:

        try:
            self.ec2.reboot_instances(InstanceIds=[instance_id])
            return instance_id
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)
                   
    def stop_ec2(self,instance_id:str)-> str:

        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])
            return instance_id
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)

    def terminate_ec2(self,instance_id:str)-> str:

        try:
            self.ec2.terminate_instances(InstanceIds=[instance_id])
            return instance_id

        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)

    def format_data_ec2(self,response:dict)-> tuple[dict,list]:

        list_rows = []
        dict_id_ec2 = {}

        if not response["Reservations"]:
            raise NoEC2Instances(self.region_name)
        
        for indice,reservation in enumerate(response["Reservations"],start=1):

            for instance in reservation["Instances"]:
                dict_id_ec2[str(indice)] = (instance.get("InstanceId"))
                fecha = instance.get("LaunchTime")
                fecha_formateada = fecha.strftime("%Y/%m/%d %H:%M:%S")
                instance_state = instance["State"].get("Name")
                instance_state_color = colors_state.get(instance_state,instance_state)
                nombre = "Sin nombre"
             
                for tag in instance.get("Tags",[]):
                    if tag.get("Key") == "Name":
                        nombre = tag.get("Value","Sin Nombre")
                        break

                list_rows.append([str(indice),
                                    nombre,
                                    instance.get("InstanceType"),
                                    instance_state_color,
                            instance.get("Architecture"),instance.get("InstanceId"),
                            instance.get("PublicIpAddress","Sin ip publica"),
                            fecha_formateada
                            ])
        return dict_id_ec2,list_rows
      
    def waiter_for_state(self, instance_id: str, target_state: str) -> bool:

        try:
            if target_state == "status_ok":
                time.sleep(12)

            waiter = self.ec2.get_waiter(f"instance_{target_state}")
            waiter.wait(InstanceIds=[instance_id])
            return True
        except WaiterError as e:
            logger.error(f"Waiter falló para {instance_id} -> {target_state}: {e}")
            return False
    
    def summary_ec2(self):

        instances_on = 0
        instances_off = 0
        response = self.describe_ec2()

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:

                state = instance["State"].get("Name")
                if state == "running":
                    instances_on += 1
                elif state in ["stopped","shutting-down"]:
                    instances_off += 1
        return instances_on,instances_off
               
if __name__ == "__main__":
    pass
    
