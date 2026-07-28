import boto3
from botocore.exceptions import ClientError
import logging
from schemas import DictFormatSGRules
from exceptions import AWSError


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

    def _parser_rules(self,ip_permissions:list)-> tuple[list,dict]:

        list_rows = []
        dict_rules = {}
        indice = 1

        for rule in ip_permissions:
            for ip_ranges in rule["IpRanges"]:
                        
                list_rows.append([str(indice),
                                rule.get("IpProtocol","Sin protocolo").upper(),
                                str(rule.get("FromPort","ALL")),
                                str(rule.get("ToPort","ALL")),
                                ip_ranges.get("CidrIp","Sin CidrIp"),
                                ip_ranges.get("Description","Sin descripción")
                                ])
                
                dict_rules[str(indice)] = {
                    "IpProtocol":rule.get("IpProtocol","N/A."),
                    "FromPort": rule.get("FromPort",-1),
                    "ToPort": rule.get("ToPort",-1),
                    "IpRanges": [{"CidrIp" : ip_ranges.get("CidrIp","Sin CidrIp."),
                                    "Description": ip_ranges.get("Description","Sin descipcion.")}]
                                    }
                indice += 1
        return list_rows,dict_rules

    def format_data_sg_rules(self,response:dict)-> DictFormatSGRules:

        ip_permissions_ingress = []
        ip_permissions_egress = []

        for security in response["SecurityGroups"]:

            ip_permissions_ingress = security["IpPermissions"]
            ip_permissions_egress = security["IpPermissionsEgress"]

        list_rows_ingress,dict_rules_ingress = self._parser_rules(ip_permissions_ingress)
        list_rows_egress,dict_rules_egress = self._parser_rules(ip_permissions_egress)
        return {
            "list_rows_ingress": list_rows_ingress,
            "dict_rules_ingress": dict_rules_ingress,
            "list_rows_egress": list_rows_egress,
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
          
    def revoke_rule_ingress(self,ip_permissions:dict)-> dict:

        
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

    def revoke_rule_egress(self,ip_permissions:dict)-> dict:

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