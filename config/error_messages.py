"""
Mensajes de error centralizados para AWS
"""

AWS_ERROR_MESSAGES: dict[str, str] = {
    # Errores de instancias
    "InvalidInstanceID.NotFound":       "Error: La instancia especificada no existe",
    "InvalidInstanceID.Malformed":      "El ID de la instancia tiene formato inválido",
    "IncorrectInstanceState":           "La instancia no puede realizar esta acción desde su estado actual",
    "OperationNotPermitted":            "La instancia tiene protección de terminación activada",
    "InsufficientInstanceCapacity":     "AWS no tiene capacidad disponible para este tipo de instancia",
    "InstanceLimitExceeded":            "Has alcanzado el límite de instancias en tu cuenta",
    "UnsupportedInstanceAttribute":     "Las instancias spot no soportan esta operación",

    # Errores de AMI
    "InvalidAMIID.NotFound":            "La AMI especificada no existe",
    "InvalidAMIID.Malformed":           "El ID de la AMI tiene formato inválido",

    # Errores de Key Pairs
    "InvalidKeyPair.NotFound":          "La key pair especificada no existe",
    "InvalidKeyPair.Duplicate":         "Ya existe una key pair con ese nombre",
    "KeyPairLimitExceeded":             "Has alcanzado el límite de key pairs en tu cuenta",
    "ErrorSaveKey":                     "Hubo un error al intentar guardar las key pairs en su dispositivo.",

    # Errores de Security Groups
    "InvalidGroup.NotFound":            "El security group especificado no existe",
    "InvalidGroupId.Malformed":         "El ID del security group tiene formato inválido",
    "InvalidPermission.Duplicate":      "La regla ya existe en el security group",
    "InvalidPermission.NotFound":       "La regla especificada no existe en el security group",
    "RulesPerSecurityGroupLimitExceeded": "Has alcanzado el límite de reglas en este security group",

    # Errores de Subnet
    "InvalidSubnet.NotFound":           "La subnet especificada no existe",

    # Errores genéricos
    "InvalidParameterValue":            "Uno de los parámetros tiene un valor inválido",
    "UnauthorizedOperation":            "No tienes permisos para realizar esta operación",
    "AuthFailure":                      "Credenciales incorrectas o expiradas",
    "RequestExpired":                   "La solicitud expiró, verifica la hora del sistema",

    # Credenciales
    "NoCredentialProviders":            "No se encontraron las credenciales de aws, ejecute en su terminal 'aws configure' para validar credenciales.",
    "InvalidClientTokenId":             "El Access Key ID no existe o fue eliminado",
    "SignatureDoesNotMatch":            "El Secret Access Key es incorrecto, verifica tus credenciales",
    "ExpiredTokenException":            "Las credenciales temporales han expirado, renueva el token",
    "AccessDenied":                     "Credenciales válidas pero sin permisos para realizar esta operación",

    # Errores de credenciales botocore
    "NoCredentialsError":               "No se encontraron credenciales, ejecuta 'aws configure'",
    "PartialCredentialsError":          "Credenciales incompletas, falta access_key o secret_key",
    "ProfileNotFound":                  "El perfil seleccionado no existe en ~/.aws/credentials",
}