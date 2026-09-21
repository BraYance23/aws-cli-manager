"""
Formularios por dominio: combinan las entradas genéricas para pedir datos de SG, llaves SSH y EC2
"""
from rich.prompt import Prompt
from ui.console import console, center_text
from ui.prompts.inputs import ask_data, ask_int


def request_ip_permissions(public_ip: str | None) -> dict:

    console.print(f"Por favor asegurarse de que los datos ingresados sean correctos.\n", style="bold bright_white", justify="center")
    protocol = Prompt.ask(center_text(text="Protocolo (tcp/udp/icmp/-1 para todo) ")).strip()

    if protocol in ("icmp", "-1"):
        from_port, to_port = -1, -1
    else:
        while True:

            from_port = ask_int(prompt="Puerto inicio : ", value_min=1, value_max=65535, msg_max="El rango valido para puertos es : 1 -")
            to_port = ask_int(prompt="Puerto fin : ", value_min=1, value_max=65535, msg_max="El rango valido para puertos es : 1 -")

            if to_port >= from_port:
                break
            console.print("El puerto de inicio no puede ser mayor al puerto fin.", style="yellow italic", justify="center")
            continue

    cidr_ip = Prompt.ask(center_text(text="CIDR IP (ej: 0.0.0.0/0 o ingresa \"1\" para colocar automaticamente su ip publica) ")).strip()
    description = Prompt.ask(center_text(text="Descripción de la regla (opcional) "))
    cidr_ip_finaly = public_ip if cidr_ip == "1" else cidr_ip
    return {
        "IpProtocol": protocol,
        "FromPort": from_port,
        "ToPort": to_port,
        "IpRanges": [
            {
                "CidrIp": cidr_ip_finaly,
                "Description": description
            }
        ]
    }


def request_name_key() -> str:

    while True:
        name_key = Prompt.ask(center_text("Ingrese el nombre de la llave SSH que desea crear ")).strip()

        if name_key:
            return name_key
        console.print("No se puede crear una llave sin nombre", style="yellow italic", justify="center")


def request_data_sg_create() -> tuple[str, str]:

    group_name = ask_data(context="Ingrese el nombre del grupo de seguridad que deasea crear ")
    description = ask_data(context="Ingrese una descripción breve del SG que desea crear ")

    return group_name, description


def request_data_config_ec2() -> tuple[int, int, str]:

    name_ec2 = Prompt.ask(center_text("Ingrese el nombre de la instancia a desplegar ")).strip()

    print("\n")
    console.print("""[bold bright_white]Explicacion de parametros minimo de instancias y maxino de instancias[/bold bright_white]
                  
AWS intentara lanzar hasta maximo de instancias que le indiques, pero si no puede (por falta de capacidad),
aceptara lanzar hasta llegar al minimo de instancias. Si no puede garantizar ni el mínimo, falla toda la operación.
                  
MaxCount = 5  → "quiero hasta 5"
MinCount = 2  → "pero necesito al menos 2"\n""", style="green", justify="center")

    while True:

        min_count = ask_int(prompt="Ingrese el minimo de instancias que desea desplegar : ", msg_max="El maximo de instancias que se puede desplegar es :")
        max_count = ask_int(prompt="Ingrese el máximo de instancias que desea desplegar : ", msg_max="El maximo de instancias que se puede desplegar es :")

        if max_count >= min_count:
            break
        console.print("\nError: El máximo debe ser mayor o igual al mínimo. Intente de nuevo.\n", style="yellow italic", justify="center")

    return min_count, max_count, name_ec2
