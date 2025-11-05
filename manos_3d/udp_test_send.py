import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(5):
    msg = f"Hola {i}".encode("utf-8")
    sock.sendto(msg, (UDP_IP, UDP_PORT))
    print("📤 Enviado:", msg)
    time.sleep(1)

sock.close()
print("✅ Prueba finalizada.")
