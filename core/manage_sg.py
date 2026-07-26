import boto3
from botocore.exceptions import ClientError
import logging
from schemas import DictFormatSGRules
from exceptions import AWSError,NoEgressRules,NoIngressRules


logger = logging.getLogger(__name__)

class ManageSecurityGroup:
    
    def __init__(self,region_name:str = "us-east-1"):
        self.region_name = region_name
        self.ec2 = boto3.client("ec2",region_name=region_name)
        self.sg_id = None
 
    def get_rules_sg(self,sg_id:str | None = "")-> dict:

        try:
            response = self.ec2.describe_security_groups(
                GroupIds=[sg_id]
            )
            return response
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)

    def formata_data_sg_rules(self,response:dict)-> DictFormatSGRules:

        list_rows_ingress = []
        list_rows_egress = []
        dict_rules_ingress = {}
        dict_rules_egress = {}

        for security in response["SecurityGroups"]:

            for indice,rule in enumerate(security["IpPermissions"],start=1):

                if not rule["IpRanges"]:
                    raise NoIngressRules(region=self.region_name,sg_id=self.sg_id)
                for ip_ranges in rule["IpRanges"]:

                    dict_rules_ingress[str(indice)] = {

                        "IpProtocol":rule.get("IpProtocol","N/A."),
                        "FromPort": rule.get("FromPort",-1),
                        "ToPort": rule.get("ToPort",-1),
                        "IpRanges": [{"CidrIp" : ip_ranges.get("CidrIp","Sin CidrIp."),
                                    "Description": ip_ranges.get("Description","Sin descipcion.")}]
                                    }
                            
                    list_rows_ingress.append([str(indice),
                                    rule.get("IpProtocol","Sin protocolo").upper(),
                                    str(rule.get("FromPort","ALL")),
                                    str(rule.get("ToPort","ALL")),
                                    ip_ranges.get("CidrIp","Sin CidrIp"),
                                    ip_ranges.get("Description","Sin descripción")
                                    ])

            if not  security["IpPermissionsEgress"]:
                raise NoEgressRules(region=self.region_name,sg_id=self.sg_id)
            for indice,rule_egress in enumerate(security["IpPermissionsEgress"],start=1):

                 for ip_ranges_egress in rule_egress["IpRanges"]:

                        dict_rules_egress[str(indice)] = {

                            "IpProtocol":rule_egress.get("IpProtocol","N/A."),
                            "FromPort": rule_egress.get("FromPort","ALL"),
                            "ToPort": rule_egress.get("ToPort","ALL"),
                            "IpRanges": [{"CidrIp" : ip_ranges_egress.get("CidrIp","Sin CidrIp."),
                                        "Description": ip_ranges_egress.get("Description","Sin descipcion.")}]
                                        }
                        
                        list_rows_egress.append([str(indice),
                                        rule_egress.get("IpProtocol","Sin protocolo").upper(),
                                        str(rule_egress.get("FromPort","ALL")),
                                        str(rule_egress.get("ToPort","ALL")),
                                        ip_ranges_egress.get("CidrIp","Sin CidrIp"),
                                        ip_ranges_egress.get("Description","Sin descripción")
                                        ])


        return {
            "list_rows_ingress": list_rows_ingress,
            "list_rows_egress": list_rows_egress,
            "dict_rules_ingress": dict_rules_ingress,
            "dict_rules_egress": dict_rules_egress
            }

    def format_data_sg_general(self,response:dict)-> tuple[list,dict]:

        dict_sg_id = {}
        list_rows = []

        for indice,valor in enumerate(response["SecurityGroups"],start=1):

            list_rows.append([
                str(indice),
                valor.get("GroupId"),
                valor.get("Description")
            ])
            dict_sg_id[str(indice)] = valor.get("GroupId")
        
        return list_rows,dict_sg_id

    def authorize_rule_ingress(self,ip_permissions:dict)-> dict:

        
        try:
            self.ec2.authorize_security_group_ingress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
            )
            return ip_permissions

        except ClientError as error:
            code = error.response["Error"]["Code"]
            raise AWSError(code=code)
          
    def remove_rule_ingress(self,ip_permissions:dict)-> dict:

        
        try:
            for valor in ip_permissions["IpRanges"]:
                del valor["Description"]        
                
            self.ec2.revoke_security_group_ingress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
            )
            return ip_permissions
                     
        except ClientError as error:
            code = error.response['Error']['Code']
            raise AWSError(code=code)

    def authorize_rule_egress(self,ip_permissions:dict)-> dict:
    
        try:
            self.ec2.authorize_security_group_egress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
            )
            return ip_permissions

        except ClientError as error:
            code = error.response["Error"]["Code"]
            raise AWSError(code=code)  

    def remove_rule_egress(self,ip_permissions:dict)-> dict:

        try:
            for valor in ip_permissions["IpRanges"]:
                del valor["Description"]        
                
            self.ec2.revoke_security_group_egress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
                        )
            return ip_permissions
                        
        except ClientError as error:
            code = error.response['Error']['Code']
            raise AWSError(code=code)
    
    def summary_sg(self)-> int:

        sg_total = 0
        response = self.get_rules_sg()
        list_sg = response["SecurityGroups"]
        return len(list_sg)
            

if __name__ == "__main__":
    pass