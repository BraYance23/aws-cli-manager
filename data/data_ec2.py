from schemas import DictHeaderRulesSG

VERSION_OS = {
    "Ubuntu": {
        "20.04 LTS": {
            "owner": "099720109477",
            "filter": "ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"
        },
        "22.04 LTS": {
            "owner": "099720109477",
            "filter": "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
        },
        "24.04 LTS": {
            "owner": "099720109477",
            "filter": "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"
        }
    },
    "Windows": {
        "Windows 2016": {
            "owner": "amazon",
            "filter": "Windows_Server-2016-English-Full-Base-*"
        },
        "Windows 2019": {
            "owner": "amazon",
            "filter": "Windows_Server-2019-English-Full-Base-*"
        },
        "Windows 2022": {
            "owner": "amazon",
            "filter": "Windows_Server-2022-English-Full-Base-*"
        }
    },
    "Amazon Linux": {
        "2": {
            "owner": "amazon",
            "filter": "amzn2-ami-hvm-2.0.*-x86_64-gp2"
        },
        "2023": {
            "owner": "amazon",
            "filter": "al2023-ami-2023.*-x86_64"
        }
    },
    "Debian": {
        "Debian 11 Bullseye": {
            "owner": "136693071363",
            "filter": "debian-11-amd64-*"
        },
        "Debian 12 Bookworm": {
            "owner": "136693071363",
            "filter": "debian-12-amd64-*"
        }
    },
    "Red Hat": {
        "Red Hat 8": {
            "owner": "309956199498",
            "filter": "RHEL-8.*_HVM-*-x86_64-*"
        },
        "Red Hat 9": {
            "owner": "309956199498",
            "filter": "RHEL-9.*_HVM-*-x86_64-*"
        }
    },
    "SUSE Linux": {
    "SLES 15 SP7": {
        "owner": "013907871322",
        "filter": "suse-sles-15-sp7-v*-hvm-ssd-x86_64*"
    },
    "SLES 16": {
        "owner": "013907871322",
        "filter": "suse-sles-16-v*-hvm-ssd-x86_64*"
    }
}

}

AWS_REGIONS = {
    "us-east-1": "N. Virginia",
    "us-east-2": "Ohio",
    "us-west-1": "N. California",
    "us-west-2": "Oregon",
    "ap-south-1": "Mumbai",
    "ap-northeast-3": "Osaka",
    "ap-northeast-2": "Seoul",
    "ap-southeast-1": "Singapore",
    "ap-southeast-2": "Sydney",
    "ap-northeast-1": "Tokyo",
    "ca-central-1": "Central",
    "eu-central-1": "Frankfurt",
    "eu-west-1": "Ireland",
    "eu-west-2": "London",
    "eu-west-3": "Paris",
    "eu-north-1": "Stockholm",
    "sa-east-1": "São Paulo"
    }

TYPES_INSTANCES = [

    ["1", "t3.nano", "2", "0.5 GB", "$0.0052", "~$3.74", "✓ Free Tier"],
    ["2", "t3.micro", "2", "1 GB", "$0.0104", "~$7.49", "✓ Free Tier"],
    ["3", "t3.small", "2", "2 GB", "$0.0208", "~$14.98", "✓ Free Tier"],
    ["4", "t3.medium", "2", "4 GB", "$0.0416", "~$29.95", ""],
    ["5", "c5a.large", "2", "4 GB", "$0.077", "~$55.44", ""],
    ["6", "t3.large", "2", "8 GB", "$0.0832", "~$59.90", ""],
    ["7", "c7i-flex.large", "2", "4 GB", "$0.0848", "~$61.06", "✓ Free Tier"],
    ["8", "m7i-flex.large", "2", "8 GB", "$0.0958", "~$68.98", "✓ Free Tier"],
    ["9", "c5a.xlarge","4", "8 GB", "$0.154", "~$110.88", ""],
    ["10", "t3.xlarge", "4", "16 GB", "$0.1664", "~$119.81", ""],
    ["11", "c5a.2xlarge", "8", "16 GB", "$0.308", "~$221.76", ""],
    ["12", "t3.2xlarge", "8", "32 GB", "$0.3328", "~$239.62", ""],
    ["13", "c5a.4xlarge", "16", "32 GB", "$0.616", "~$443.52", ""],
    ["14", "c5a.12xlarge", "48", "96 GB", "$1.848", "~$1,330.56", ""],
    ["15", "c5a.24xlarge", "96", "192 GB", "$3.696", "~$2,661.12", ""]
]

parameter_operation_ec2 = {
    "3": ("📟 -Iniciando instancia","running","✅-Instancia iniciada correctamente."),
    "4": ("🔁 -Reiniciando instancia","status_ok","✅-Instancia reiniciada correctamente."),
    "5": ("🛑 -Deteniendo instancia","stopped","✅-Instancia detenenida correctamente."),
    "6": ("🗑️ -Eliminando instancia","terminated","✅-Instancia eliminada correctamente.")
}    

colors_state = {
    "running":  "[green]● Running[/green]",
    "stopped": "[red]● Stopped[/red]", 
    "terminated": "[red]● Terminated[/red]",  
    "pending": "[cyan]● Pending[/cyan]",
    "stopping": "[yellow]● Stopping[/yellow]",  
    "shutting-down": "[red]● Shutting-Down[/red]",
}

OS_AVALIBLE = [
    ["1","Amazon Linux","x86_64"],
    ["2","Ubuntu","x86_64"],
    ["3","Windows","x86_64"],
    ["4","Red Hat","x86_64"],
    ["5","SUSE Linux","x86_64"],
    ["6","Debian","x86_64"]
]

dict_type_instances = {sub[0]:sub[1] for sub in TYPES_INSTANCES}

dict_os_general = {sub[0]:sub[1] for sub in OS_AVALIBLE}

"""
Permisos para operaciones de EC2
va mapeado igual que la tabla de despacho que esta en
ec2_controller.py

metodos_ec2 = {
    "3": self.manager_root.ec2.init_ec2,
    "4": self.manager_root.ec2.reboot_ec2,
    "5": self.manager_root.ec2.stop_ec2,
    "6": self.manager_root.ec2.terminate_ec2
    }
"""
permissions_ec2 = {
    "3": {
        "permissions" :["stopped"],
          "message": "No se puede iniciar la instancia en el estado actual | estado de la instancia : "
          },
    "4":{
        "permissions":["running"],
        "message": "No se puede reiniciar la instancia en el estado actual | estado de la instancia : "
        },
    "5": {
        "permissions":["running"],
        "message": "No se puede detener la instancia en el estado actual | estado de la instancia : "
        },
    "6":{
        "permissions":["running","stopped"],
        "message":  "No se puede terminar la instancia en el estado actual | estado de la instancia : "
        }
    }

"""
Encabezados y titulos para rich
"""

headers_types_ec2 =  {"header": ["INDICE",
                                 "Instancia",
                                 "vCPU",
                                 "RAM",
                                 "$/hora",
                                 "$/mes",
                                 "Free Tier"],
                    "title": "\tTipos de instancias disponibles y costes"}

header_os_general = {"header" :["INDICE",
                                "DISTRO",
                                "ARQUITECTURA" ],
                    "title": "Seleccione el tipo de sistema operativo que desea desplegar :"}

header_os_version = {"header":["INDICE",
                               "Distros",
                               "Arquitectura",
                               "Distribuidor" ],
                    "title": "Versiones del sistema operativo seleccionado : "}

header_selected_ami = {"header": ["INDICE",
                                  "ID AMI",
                                  "Name ",
                                  "Architecture",
                                  "Free tier",
                                  "Date creation"],
                      "title": "AMIS disponible :"}


"""
Control de flujo de servicios y orquestador
"""

main_root = {"1": "Administrar EC2",
            "2": "Administar Security Groups",
            "3": "Administar Key Pairs",
            "4": "Actualizar Dashboard",
            "5": "Cambiar de region",
            "6": "Salir"}

main_ec2 = {"1": "Listar instancias",
            "2": "Desplegar instancia",
            "3": "Iniciar instancia",
            "4": "Reiniciar instancia",
            "5": "Detener instancia",
            "6": "Terminar instancia",
            "7": "Volver al menu principal"}

main_sg = {"1": "Listar reglas de entrada",
           "2": "Listar reglas de salida",
           "3": "Agregar regla de entrada",
           "4": "Eliminar regla de entrada",
           "5": "Agregar regla de salida",
           "6": "Eliminar reglada de salida",
           "7": "Cambiar grupo de seguridad",
           "8": "Volver al menu principal"
           }

main_key_pair = {"1": "Listar llaves SSH",
                 "2": "Crear llave SSH",
                 "3": "Eliminar llave SSH",
                 "4": "Volver al menu principal"}

"""
Manejo de errores centraliazado
"""
AWS_ERROR_MESSAGES: dict[str, str] = {""
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
    "No se encontraron credenciales":   "No se encontraron las credenciales de aws, ejecute en su terminal 'aws configure' para validar credenciales.",
}


