#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SOCKS5_VERSION 0x05
#define AUTH_NO_AUTH 0x00
#define CMD_UDP_ASSOCIATE 0x03
#define ADDR_TYPE_IPV4 0x01

void error(const char *msg) {
    perror(msg);
    exit(1);
}

int create_udp_socket(const char *proxy_host, int proxy_port, const char *target_ip, int target_port) {
    // Membuat soket TCP untuk negosiasi SOCKS5
    int tcp_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (tcp_sock < 0) error("Error opening TCP socket");

    struct sockaddr_in proxy_addr;
    proxy_addr.sin_family = AF_INET;
    proxy_addr.sin_port = htons(proxy_port);
    inet_pton(AF_INET, proxy_host, &proxy_addr.sin_addr);

    // Menghubungkan ke proxy SOCKS5
    if (connect(tcp_sock, (struct sockaddr *)&proxy_addr, sizeof(proxy_addr)) < 0)
        error("Error connecting to proxy");

    // Negosiasi SOCKS5
    unsigned char auth_request[] = {
        SOCKS5_VERSION,  // Versi SOCKS5
        1,               // Jumlah metode otentikasi
        AUTH_NO_AUTH     // Metode otentikasi (tanpa otentikasi)
    };
    send(tcp_sock, auth_request, sizeof(auth_request), 0);

    unsigned char auth_response[2];
    recv(tcp_sock, auth_response, sizeof(auth_response), 0);
    if (auth_response[1] != AUTH_NO_AUTH)
        error("Proxy requires unsupported authentication");

    // Meminta UDP relay
    unsigned char udp_request[10] = {
        SOCKS5_VERSION,         // Versi SOCKS5
        CMD_UDP_ASSOCIATE,      // Perintah untuk UDP relay
        0x00,                   // Reserved
        ADDR_TYPE_IPV4,         // Jenis alamat (IPv4)
        0, 0, 0, 0,             // IP tujuan (0.0.0.0 untuk UDP relay)
        0, 0                    // Port tujuan (0 untuk UDP relay)
    };
    send(tcp_sock, udp_request, sizeof(udp_request), 0);

    unsigned char udp_response[10];
    recv(tcp_sock, udp_response, sizeof(udp_response), 0);
    if (udp_response[1] != 0x00)
        error("Failed to set up UDP relay");

    // Alamat dan port relay dari proxy
    struct sockaddr_in udp_relay_addr;
    udp_relay_addr.sin_family = AF_INET;
    memcpy(&udp_relay_addr.sin_addr, &udp_response[4], 4);  // IP relay
    memcpy(&udp_relay_addr.sin_port, &udp_response[8], 2);  // Port relay

    // Membuat soket UDP
    int udp_sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (udp_sock < 0) error("Error opening UDP socket");

    // Membuat payload
    unsigned char payload[1024];
    size_t payload_size = 0;

    // Prefix "SAMP"
    memcpy(payload, "SAMP", 4);
    payload_size += 4;

    // Alamat target (IP dalam format binary)
    struct in_addr target_addr;
    inet_pton(AF_INET, target_ip, &target_addr);
    memcpy(payload + payload_size, &target_addr, sizeof(target_addr));
    payload_size += sizeof(target_addr);

    // Port target (2-byte, big-endian)
    payload[payload_size] = (target_port >> 8) & 0xFF;  // Byte pertama
    payload[payload_size + 1] = target_port & 0xFF;     // Byte kedua
    payload_size += 2;

    // Suffix "i"
    payload[payload_size] = 'i';
    payload_size += 1;

    // Mengirimkan payload ke proxy
    if (sendto(udp_sock, payload, payload_size, 0, (struct sockaddr *)&udp_relay_addr, sizeof(udp_relay_addr)) < 0)
        error("Error sending UDP packet through proxy");

    printf("UDP packet sent with payload: SAMP+<IP>%d+i\n", target_port);

    close(tcp_sock);  // Tutup koneksi TCP
    close(udp_sock);  // Tutup soket UDP

    return 0;
}

int main() {
    const char *proxy_host = "127.0.0.1";  // IP proxy SOCKS5
    int proxy_port = 1080;                // Port proxy SOCKS5
    const char *target_ip = "#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SOCKS5_VERSION 0x05
#define AUTH_NO_AUTH 0x00
#define CMD_UDP_ASSOCIATE 0x03
#define ADDR_TYPE_IPV4 0x01

void error(const char *msg) {
    perror(msg);
    exit(1);
}

int create_udp_socket(const char *proxy_host, int proxy_port, const char *target_ip, int target_port) {
    // Membuat soket TCP untuk negosiasi SOCKS5
    int tcp_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (tcp_sock < 0) error("Error opening TCP socket");

    struct sockaddr_in proxy_addr;
    proxy_addr.sin_family = AF_INET;
    proxy_addr.sin_port = htons(proxy_port);
    inet_pton(AF_INET, proxy_host, &proxy_addr.sin_addr);

    // Menghubungkan ke proxy SOCKS5
    if (connect(tcp_sock, (struct sockaddr *)&proxy_addr, sizeof(proxy_addr)) < 0)
        error("Error connecting to proxy");

    // Negosiasi SOCKS5
    unsigned char auth_request[] = {
        SOCKS5_VERSION,  // Versi SOCKS5
        1,               // Jumlah metode otentikasi
        AUTH_NO_AUTH     // Metode otentikasi (tanpa otentikasi)
    };
    send(tcp_sock, auth_request, sizeof(auth_request), 0);

    unsigned char auth_response[2];
    recv(tcp_sock, auth_response, sizeof(auth_response), 0);
    if (auth_response[1] != AUTH_NO_AUTH)
        error("Proxy requires unsupported authentication");

    // Meminta UDP relay
    unsigned char udp_request[10] = {
        SOCKS5_VERSION,         // Versi SOCKS5
        CMD_UDP_ASSOCIATE,      // Perintah untuk UDP relay
        0x00,                   // Reserved
        ADDR_TYPE_IPV4,         // Jenis alamat (IPv4)
        0, 0, 0, 0,             // IP tujuan (0.0.0.0 untuk UDP relay)
        0, 0                    // Port tujuan (0 untuk UDP relay)
    };
    send(tcp_sock, udp_request, sizeof(udp_request), 0);

    unsigned char udp_response[10];
    recv(tcp_sock, udp_response, sizeof(udp_response), 0);
    if (udp_response[1] != 0x00)
        error("Failed to set up UDP relay");

    // Alamat dan port relay dari proxy
    struct sockaddr_in udp_relay_addr;
    udp_relay_addr.sin_family = AF_INET;
    memcpy(&udp_relay_addr.sin_addr, &udp_response[4], 4);  // IP relay
    memcpy(&udp_relay_addr.sin_port, &udp_response[8], 2);  // Port relay

    // Membuat soket UDP
    int udp_sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (udp_sock < 0) error("Error opening UDP socket");

    // Membuat payload
    unsigned char payload[1024];
    size_t payload_size = 0;

    // Prefix "SAMP"
    memcpy(payload, "SAMP", 4);
    payload_size += 4;

    // Alamat target (IP dalam format binary)
    struct in_addr target_addr;
    inet_pton(AF_INET, target_ip, &target_addr);
    memcpy(payload + payload_size, &target_addr, sizeof(target_addr));
    payload_size += sizeof(target_addr);

    // Port target (2-byte, big-endian)
    payload[payload_size] = (target_port >> 8) & 0xFF;  // Byte pertama
    payload[payload_size + 1] = target_port & 0xFF;     // Byte kedua
    payload_size += 2;

    // Suffix "i"
    payload[payload_size] = 'i';
    payload_size += 1;

    // Mengirimkan payload ke proxy
    if (sendto(udp_sock, payload, payload_size, 0, (struct sockaddr *)&udp_relay_addr, sizeof(udp_relay_addr)) < 0)
        error("Error sending UDP packet through proxy");

    printf("UDP packet sent with payload: SAMP+<IP>%d+i\n", target_port);

    close(tcp_sock);  // Tutup koneksi TCP
    close(udp_sock);  // Tutup soket UDP

    return 0;
}

int main() {
    const char *proxy_host = "103.139.25.121";  // IP proxy SOCKS5
    int proxy_port = 8080;                // Port proxy SOCKS5
    const char *target_ip = "93.184.216.34";  // IP tujuan
    int target_port = 7023;               // Port tujuan

    create_udp_socket(proxy_host, proxy_port, target_ip, target_port);
    return 0;
}
";  // IP tujuan
    int target_port = 7777;               // Port tujuan

    create_udp_socket(proxy_host, proxy_port, target_ip, target_port);
    return 0;
}
