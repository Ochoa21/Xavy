import os

# Ruta al archivo hosts
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
# Dirección IP a la que redirigir (localhost)
redirect_ip = "127.0.0.1"
# Lista de dominios que deseas bloquear
website_list = [
    "assets.queue-it.net",
    "queue.eticket.net",
    "queue.tuboleta.net",
    "queue.taquillalive.net",
    "queue.latiquetera.net"
]

def block_websites():
    with open(hosts_path, 'r+') as file:
        content = file.read()
        for website in website_list:
            if website not in content:
                file.write(redirect_ip + " " + website + "\n")
                print(f"{website} ha sido bloqueado.")
            else:
                print(f"{website} ya está bloqueado.")

def unblock_websites():
    with open(hosts_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(website in line for website in website_list):
                file.write(line)
        file.truncate()
        print(f"{website_list} han sido desbloqueados.")

if __name__ == "__main__":
    action = input("¿Quieres bloquear o desbloquear los sitios web? (bloquear/desbloquear): ").strip().lower()
    if action == "bloquear":
        block_websites()
    elif action == "desbloquear":
        unblock_websites()
    else:
        print("Acción no reconocida. Por favor, elige 'bloquear' o 'desbloquear'.")
