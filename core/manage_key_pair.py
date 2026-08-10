import logging
from pathlib import Path
from botocore.exceptions import ClientError
from exceptions import AWSError,NoKeyPairs


logger = logging.getLogger(__name__)

class ManageKeyPairs:

    def __init__(self,session_root,region_name = "us-east-1"):
        self.session_root = session_root
        self.region_name = region_name
        self.client_kp = self.session_root.client("ec2",region_name=region_name)


    def request_key_pairs(self)-> dict:

        try:
            response = self.client_kp.describe_key_pairs()
            return response
            
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)
      
    def format_data(self,response:dict)-> tuple[dict,list]:
        
        list_rows = []
        dict_key_id = {}

        if not response["KeyPairs"]:
            raise NoKeyPairs(region=self.region_name)
        
        for indice,key in enumerate(response["KeyPairs"],start=1):

            fecha = key.get("CreateTime")
            fecha_formateada = fecha.strftime("%Y/%m/%d %H:%M:%S")

            dict_key_id[str(indice)] = key.get("KeyName",None)

            list_rows.append([
                str(indice),
                key.get("KeyName","Sin llave"),
                key.get("KeyPairId",None),
                fecha_formateada
            ])
    
        return dict_key_id,list_rows

    def generate_key_pair(self, key_name:str)-> str:

        try:
            response = self.client_kp.create_key_pair(KeyName=key_name)
            private_key = response["KeyMaterial"]
            return private_key
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)

    def save_key_pair(self,private_key:str,key_name:str)-> Path:

        key_path = Path.home()/".ssh"/f"{key_name}.pem"
        key_path.parent.mkdir(parents=True,exist_ok=True)
        key_path.write_text(private_key)
        key_path.chmod(0o600)
        return key_path


    def delete_key_pair(self,key_delete:str)-> str:

        try:
            self.client_kp.delete_key_pair(KeyName=key_delete)
            return key_delete

        except ClientError as error:
            code = error.response["Error"]["Code"]
            raise AWSError(code=code)

    def summary_key_pairs(self)-> int:

        response = self.request_key_pairs()
        list_key_pairs = response["KeyPairs"]
        return {
            "summary_kp": len(list_key_pairs)
        }
    
if __name__ == "__main__":
    pass