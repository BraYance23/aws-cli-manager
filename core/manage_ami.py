import logging
from datetime import datetime
from core.decorators import handles_aws_error
from data import data_ec2
from exceptions import AWSError


logger = logging.getLogger(__name__)


class ManageAmi:
  
    def __init__(self,session_root,region_name = "us-east-1"):
        self.session_root = session_root
        self.region_name = region_name
        self.client_ami = self.session_root.client("ec2",region_name=region_name)

    @handles_aws_error
    def get_ami_id(self,owner:str,filter:str)-> tuple[bool,dict | str]:

        response = self.client_ami.describe_images(
        Owners=[owner],
        Filters=[
                {"Name": "name", "Values": [filter]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "architecture", "Values": ["x86_64"]}
            ]
        )
        return response

    def prepare_data_ami(self,data_ami:dict)-> tuple[list,dict]:

        list_rows = []
        dict_id_ami = {}

        for indice,image in enumerate(data_ami["Images"],start=1):
                
            if image["State"] == "available":
                
                fecha = image.get("CreationDate")
                fecha_formateada = datetime.fromisoformat(fecha[:19]).strftime("%Y/%m/%d %H:%M:%S")
                    
                list_rows.append(
                    [str(indice),
                    image.get("ImageId"),
                    image.get("Name"),
                    image.get("Architecture"),
                    str(image.get("FreeTierEligible")),
                    fecha_formateada
                    ]
                    )
                dict_id_ami[str(indice)] = image.get("ImageId")
                    
        return list_rows,dict_id_ami
         
    def formate_data_selected_os(self,election:str)-> tuple[list,dict]:

        dict_distro = {}
        list_rows = []
         
        for indice,valor in enumerate(data_ec2.VERSION_OS[election],start=1):
            list_rows.append([str(indice),
                                  valor,
                                  "x86_64",
                                  "AMAZON"
                                  ])
            dict_distro[str(indice)] = valor
            
        return list_rows,dict_distro
    

if __name__ == "__main__":
    pass