import json
import socket

RESPONSE_HEADER = '''HTTP/1.1 200 OK\r\nPOST HTTP/1.1\r\nHost: 192.168.1.115\r\nContent-Type: text/json\r\nContent-Length: {length}\r\n\r\n'''


class SocketHandler:

    def __init__(self):
        address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.socket = socket.socket()
        self.socket.bind(address)
        self.socket.listen(1)
        self.socket.setblocking(False)
        self.socket.settimeout(1)
        print('New Socket is listening on: ', address)

    def update_socket(self):
        try:
            client, address = self.socket.accept()
            data = self.handle_connection(client, address)
            return True, data
        except OSError:
            return False, []

    def handle_connection(self, client, address):
        print('Client connected from: ', address)
        _ = client.recv(1024)
        data_raw = client.recv(1024)
        data_json = json.loads(json.loads(data_raw))
        return_data = json.dumps('{"test": True}')
        client.sendall(RESPONSE_HEADER.format(length=len(return_data)))
        client.sendall(return_data)
        client.close()
        return data_json
