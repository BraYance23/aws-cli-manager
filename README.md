# Manage AWS

CLI interactiva para administrar recursos de AWS desde la terminal.  
Permite gestionar instancias EC2, Security Groups y Key Pairs sin salir de la consola, con una interfaz visual construida con [Rich](https://github.com/Textualize/rich).

---

## Características

- **EC2** — Listar, desplegar, iniciar, reiniciar, detener y terminar instancias
- **Security Groups** — Ver, agregar y revocar reglas de entrada y salida
- **Key Pairs** — Listar, crear y eliminar llaves SSH (se guardan automáticamente en `~/.ssh/`)
- Selección interactiva de región AWS al iniciar
- Dashboard con resumen de recursos activos
- Validación de credenciales antes de operar
- Detección automática de IP pública para reglas de Security Group
- Manejo centralizado de errores de la API de AWS
- Logs de operaciones en archivo

---

## Requisitos

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) (gestor de paquetes)
- Credenciales de AWS configuradas (`aws configure`)

---

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd manage_aws

# Instalar dependencias con uv
uv sync
```

O con pip:

```bash
pip install -r requirements.txt
```

---

## Configuración de credenciales AWS

La aplicación usa las credenciales estándar de AWS.  
Si aún no las tienes configuradas, ejecuta:

```bash
aws configure
```

Ingresa tu `Access Key ID`, `Secret Access Key` y región por defecto.

También puedes usar un archivo `.env` en la raíz del proyecto:

```
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_DEFAULT_REGION=us-east-1
```

---

## Uso

```bash
python main.py
```

Al iniciar verás el listado de regiones disponibles. Selecciona una y la aplicación validará tus credenciales antes de mostrar el menú principal.

### Menú principal

```
[1] Administrar EC2
[2] Administrar Security Groups
[3] Administrar Key Pairs
[4] Actualizar Dashboard
[5] Cambiar de región
[6] Salir
```

### Administrar EC2

```
[1] Listar instancias
[2] Desplegar instancia   ← guía paso a paso: OS, versión, AMI, tipo, key pair, SG
[3] Iniciar instancia
[4] Reiniciar instancia
[5] Detener instancia
[6] Terminar instancia
```

### Administrar Security Groups

```
[1] Listar reglas de entrada
[2] Listar reglas de salida
[3] Agregar regla de entrada
[4] Agregar regla de salida
[5] Eliminar regla de entrada
[6] Eliminar regla de salida
[7] Cambiar de Security Group
```

### Administrar Key Pairs

```
[1] Listar llaves SSH
[2] Crear llave SSH     ← se guarda en ~/.ssh/<nombre>.pem con permisos 600
[3] Eliminar llave SSH
```

---

## Estructura del proyecto

```
manage_aws/
├── main.py                  # Punto de entrada
├── exceptions.py            # Excepciones personalizadas
├── schemas.py               # TypedDicts
├── pyproject.toml
│
├── core/                    # Lógica de negocio — comunicación con boto3
│   ├── manage_ec2.py
│   ├── manage_sg.py
│   ├── manage_key_pair.py
│   └── manage_ami.py
│
├── controllers/             # Orquestación entre UI y core
│   ├── menu_services.py
│   ├── ec2_controller.py
│   ├── sg_controller.py
│   ├── kp_controller.py
│   ├── ami_controller.py
│   └── deploy_flow.py
│
├── ui/                      # Presentación con Rich
│   ├── menus.py
│   ├── tables.py
│   ├── messages.py
│   └── prompt_general.py
│
├── data/
│   └── data_ec2.py          # Datos estáticos: regiones, tipos de instancia, OS
│
├── config/
│   └── logging_config.py    # Configuración de logs
│
├── utils/
│   └── network.py           # Detección de IP pública
│
└── logs/
    └── manager_aws.log      # Log de operaciones
```

---

## Regiones disponibles

| Región | Ubicación |
|---|---|
| us-east-1 | N. Virginia |
| us-east-2 | Ohio |
| us-west-1 | N. California |
| us-west-2 | Oregon |
| eu-west-1 | Irlanda |
| eu-central-1 | Frankfurt |
| ap-northeast-1 | Tokio |
| ap-southeast-1 | Singapur |
| sa-east-1 | São Paulo |
| ... | y 8 más |

---

## Sistemas operativos disponibles para despliegue

- Amazon Linux 2 / 2023
- Ubuntu 20.04 / 22.04 / 24.04 LTS
- Windows Server 2016 / 2019 / 2022
- Red Hat 8 / 9
- Debian 11 / 12
- SUSE Linux 15 / 16

---

## Dependencias principales

| Paquete | Uso |
|---|---|
| boto3 | SDK oficial de AWS |
| rich | Tablas, paneles y colores en terminal |
| python-dotenv | Carga de variables de entorno |
| requests | Detección de IP pública |

---

## Logs

Las operaciones importantes se registran en `logs/manager_aws.log`:

- Creación y eliminación de key pairs
- Autorización y revocación de reglas de Security Group
- Errores de waiters en operaciones de EC2

---

## Notas

- Las llaves SSH se guardan en `~/.ssh/<nombre>.pem` con permisos `600`
- Al desplegar una instancia el flujo guía paso a paso la selección de OS, AMI, tipo de máquina, key pair y Security Group
- Las operaciones destructivas (terminar instancia, eliminar llave) piden confirmación explícita antes de ejecutarse
