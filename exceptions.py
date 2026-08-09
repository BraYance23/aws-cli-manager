

class AWSError(Exception):

    def __init__(self,code:str):
        self.code = code

class ApplicationException(Exception):
    pass

class ResourceNotFound(Exception):

    def __init__(self,region:str="",sg_id:str=""):
        self.region = region
        self.sg_id = sg_id

class InvalidOperationEC2(ApplicationException):

    def __init__(self,message:str,instance_state:str):
        self.message = message
        self.instance_state = instance_state

    def __str__(self):
        return f"{self.message} {self.instance_state}"

class NoEC2Instances(ResourceNotFound):
    pass

class NoSecurityGroups(ResourceNotFound):

    def __str__(self):
        return f"No hay grupos de seguidad existentes en la region : {self.region}"

class NoIngressRules(ResourceNotFound):

    def __str__(self):
        return f"No hay reglas de entrada en el grupo de seguridad : {self.sg_id} | Region : {self.region}"

class NoEgressRules(ResourceNotFound):
    def __str__(self):
            return f"No hay reglas de salida en el grupo de seguridad : {self.sg_id} | Region : {self.region}"
    
class NoKeyPairs(ResourceNotFound):

    def __str__(self):
        return f"No hay llaves SSH en la region : {self.region}"

class UserCancelOperation(ApplicationException):
    pass

class CredentialsError(AWSError):
    pass
