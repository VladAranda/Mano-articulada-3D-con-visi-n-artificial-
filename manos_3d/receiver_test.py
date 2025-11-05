import socket, json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("Esperando datos...")

while True:
    data, _ = sock.recvfrom(4096)
    payload = json.loads(data.decode("utf-8"))
    print("Mano detectada:", payload["found"], " | Puntos:", len(payload["landmarks"]))
