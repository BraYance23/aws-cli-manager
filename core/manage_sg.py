import logging
from botocore.exceptions import ClientError
from schemas import DictFormatSGRules
from exceptions import AWSError,NoSecurityGroups


logger = logging.getLogger(__name__)

class ManageSecurityGroup:
    
    def __init__(self,session_root,region_name:str = "us-east-1"):
        self.session_root = session_root
        self.region_name = region_name
        self.client_sg = session_root.client("ec2",region_name=region_name)
        self.sg_id = None


    def get_sg_rules(self,sg_id):

        try:
            response = self.client_sg.describe_security_group_rules(
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [sg_id]
                    }
                ]
            )
            return response
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)

    def get_sg_general(self)-> dict:

        try:
            response = self.client_sg.describe_security_groups()
            return response
        except ClientError as e:
            code = e.response["Error"]["Code"]
            raise AWSError(code=code)

    def _parser_rules(self,ip_permissions:list)-> tuple[list,dict]:

        list_rows = []
        dict_rules = {}

        for indice,rule in enumerate(ip_permissions,start=1):
            list_rows.append([str(indice),
                              rule.get("IpProtocol","Sin protocolo").upper(),
                              str(rule.get("FromPort","ALL")),
                              str(rule.get("ToPort","ALL")),
                              rule.get("CidrIpv4","Sin CidrIp"),
                              rule.get("Description","Sin descripción")
                              ]
                            )
            dict_rules[str(indice)] = rule["SecurityGroupRuleId"]
        return list_rows,dict_rules



    def format_data_sg_rules(self,response:dict)-> DictFormatSGRules:

        ip_permissions_ingress = []
        ip_permissions_egress = []

        for rule in response["SecurityGroupRules"]:

            if rule["IsEgress"]:
                ip_permissions_egress.append(rule)
            else:
                ip_permissions_ingress.append(rule)

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

        if not response["SecurityGroups"]:
            raise NoSecurityGroups(region=self.region_name)
        
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
            self.client_sg.authorize_security_group_ingress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
            )
            return True

        except ClientError as error:
            code = error.response["Error"]["Code"]
            raise AWSError(code=code)
          
    def revoke_rule_ingress(self,sg_rule_id:dict)-> dict:

        try:        
            response = self.client_sg.revoke_security_group_ingress(
                GroupId = self.sg_id,
                SecurityGroupRuleIds = [sg_rule_id]
            )
            return response["RevokedSecurityGroupRules"][0]
                        
        except ClientError as error:
            code = error.response['Error']['Code']
            raise AWSError(code=code)

    def authorize_rule_egress(self,ip_permissions:dict)-> dict:
    
        try:
            self.client_sg.authorize_security_group_egress(
                GroupId = self.sg_id,
                IpPermissions = [ip_permissions]
            )
            return True

        except ClientError as error:
            code = error.response["Error"]["Code"]
            raise AWSError(code=code)  

    def revoke_rule_egress(self,sg_rule_id:dict)-> dict:

        try:               
            response = self.client_sg.revoke_security_group_egress(
                GroupId = self.sg_id,
                SecurityGroupRuleIds = [sg_rule_id]
            )
            return response["RevokedSecurityGroupRules"][0]
                        
        except ClientError as error:
            code = error.response['Error']['Code']
            raise AWSError(code=code)
    
    def summary_sg(self)-> int:

        response = self.get_sg_general()
        list_sg = response["SecurityGroups"]
        return {
            "summary_sg": len(list_sg)
        }
            

if __name__ == "__main__":
    pass