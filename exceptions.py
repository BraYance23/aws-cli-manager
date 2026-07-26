

class AWSError(Exception):

    def __init__(self,code:str):
        self.code = code

class AplicationException(Exception):
    pass

class ResourceNotFound(Exception):

    def __init__(self,region:str="",sg_id:str|None=""):
        self.region = region
        self.sg_id = sg_id

class NoEC2Instances(ResourceNotFound):
    pass

class NoSecurityGroups(ResourceNotFound):
    pass

class NoIngressRules(ResourceNotFound):
    pass

class NoEgressRules(ResourceNotFound):
    pass

class NoKeyPairs(ResourceNotFound):
    pass

class UserCancelOperation(AplicationException):
    pass

class CredentialsError(AWSError):
    pass

class CredentialsNotFound(AWSError):
    pass

