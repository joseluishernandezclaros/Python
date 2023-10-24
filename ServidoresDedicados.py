import requests
from json import JSONDecodeError
import json
import time

# Clave de API de Steam
STEAM_API_KEY = "0D090CC712FD4CF9F2B2891FB2373DE8"

def get_server_info(server_ip, server_port):
    """Obtiene información sobre un servidor dedicado de Euro Truck Simulator.

    Args:
        server_ip: La dirección IP del servidor.
        server_port: El puerto del servidor.

    Returns:
        Un objeto que contiene información sobre el servidor.
    """

    url = f"https://api.steampowered.com/ISteamRemoteStorage/GetServerInfo/v0001/?ip={server_ip}&port={server_port}"
    response = requests.get(url, headers={"Authorization": f"bearer {STEAM_API_KEY}"})

    try:
        data = response.json()
    except JSONDecodeError:
        # El servidor dedicado no está disponible o la API de Steam está experimentando problemas.
        return None

    return data


def get_number_of_players(server_info):
    """Obtiene la cantidad de jugadores conectados a un servidor dedicado de Euro Truck Simulator.

    Args:
        server_info: Un objeto que contiene información sobre el servidor.

    Returns:
        La cantidad de jugadores conectados al servidor.
    """

    if server_info is None:
        return 0

    players = server_info["players"]

    return players


# Ejemplo de uso

server_ip = "192.168.1.11"
server_port = 27015

while True:
    # Obtener la información del servidor dedicado
    server_info = get_server_info(server_ip, server_port)

    # Obtener la cantidad de jugadores conectados
    number_of_players = get_number_of_players(server_info)

    # Imprimir el resultado
    print(f"La cantidad de jugadores conectados al servidor es {number_of_players}")

    # Esperar 30 segundos
    time.sleep(30)
