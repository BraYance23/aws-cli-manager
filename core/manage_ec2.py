import  time
import logging
from botocore.exceptions import ClientError,NoCredentialsError,WaiterError,PartialCredentialsError,ProfileNotFound
from exceptions import AWSError,NoEC2Instances,CredentialsError
from data.data_ec2 import colors_state


logger = logging.getLogger(__name__)

class ManageEc2:

    def __init__(self,session_root,region_name = "us-east-1"):
        self.session_root = session_root
        self.region_name = region_name
        self.client_ec2 = session_root.client("ec2",region_name=region_name)
        self.client_sts = session_root.client("sts",region_name=region_name)
       

    def describe_ec2(self)-> str:

        try:
            response = self.client_ec2.describe_instances()
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
            response = self.client_sts.get_caller_identity()
            return response
        
        except NoCredentialsError:
            raise CredentialsError(code="NoCredentialProviders")

        except PartialCredentialsError:
            raise CredentialsError(code="PartialCredentialsError")

        except ProfileNotFound:
            raise CredentialsError(code="ProfileNotFound")
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)
    
    def run_ec2(self,config:dict)-> list[str]:

        try:
            response = self.client_ec2.run_instances(**config)
            return [i["InstanceId"] for i in response["Instances"]]

        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)
        
    def init_ec2(self,instance_id:str)-> str:

        try:
            self.client_ec2.start_instances(InstanceIds=[instance_id])
            return instance_id
           
        except ClientError  as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)   
           
    def reboot_ec2(self,instance_id:str)-> str:

        try:
            self.client_ec2.reboot_instances(InstanceIds=[instance_id])
            return instance_id
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)
                   
    def stop_ec2(self,instance_id:str)-> str:

        try:
            self.client_ec2.stop_instances(InstanceIds=[instance_id])
            return instance_id
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)

    def terminate_ec2(self,instance_id:str)-> str:

        try:
            self.client_ec2.terminate_instances(InstanceIds=[instance_id])
            return instance_id

        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)

    def format_data_ec2(self,response:dict)-> tuple[dict,list]:

        list_rows = []
        dict_id_ec2 = {}
        indice = 0

        if not response["Reservations"]:
            raise NoEC2Instances(self.region_name)
        
        for reservation in response["Reservations"]:

            for instance in reservation["Instances"]:
                indice += 1
                fecha = instance.get("LaunchTime")
                fecha_formateada = fecha.strftime("%Y/%m/%d %H:%M:%S")
                instance_state = instance["State"].get("Name")
                instance_state_color = colors_state.get(instance_state,instance_state)
                nombre = "Sin nombre"
                dict_id_ec2[str(indice)] = {"instance_id":instance.get("InstanceId"),
                                            "instance_state": instance_state}
             
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
      
    def waiter_for_state(self, list_instance_ids: str, target_state: str) -> bool:

        try:
            if target_state == "status_ok":
                time.sleep(12)

            waiter = self.client_ec2.get_waiter(f"instance_{target_state}")
            waiter.wait(InstanceIds=list_instance_ids)
            return True
        except WaiterError as e:
            logger.error(f"Waiter falló para {list_instance_ids} -> {target_state}: {e}")
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
                elif state  == "stopped":
                    instances_off += 1
        return {
            "summary_ec2": (instances_on,instances_off)
        }

               
if __name__ == "__main__":
    pass
    
