import json
import socket
import urequests

RESPONSE_HEADER = '''HTTP/1.1 200 OK\r\nPOST HTTP/1.1\r\nHost: 192.168.1.115\r\nContent-Type: 
text/json\r\nContent-Length: {length}\r\n\r\n '''


class ConnectionHandler:
    """
    Handles connections to the user controller.
    Primary focus are incoming messages, however also sends back data
    """

    def __init__(self, task_manager):
        address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self._socket = socket.socket()
        self._socket.bind(address)
        self._socket.listen(1)
        self._socket.setblocking(False)
        self._socket.settimeout(1)

        self._task_manager = task_manager

        print('New Socket is listening on: ', address)

    def update_socket(self):
        """
        Checks for incoming connection and parses them if needed
        :return: The post data json, or [] if the socket times out
        """
        try:
            client, address = self._socket.accept()
            self.handle_connection(client, address)
        except OSError:
            pass
        finally:
            return

    def handle_connection(self, client, address):
        """
        Handles incoming connections.
        Checks what type of connection was made and pipes the given data towards the right handler.
        Then returns a success message back to the client
        :param client:
        :param address:
        :return:
        """
        _ = client.recv(1024)
        data_raw = client.recv(1024)
        data_json = json.loads(json.loads(data_raw))
        if data_json['load']['request_type'] == 'post':
            self._task_manager.on_new_post(data_json['load'])
            return_data = json.dumps('{"executed": True}')
        else:
            return_data = self._task_manager.on_get_request(data_json['load'])
        client.sendall(RESPONSE_HEADER.format(length=len(return_data)))
        client.sendall(return_data)
        client.close()

    @staticmethod
    def make_get_request(url):
        """
        Static function to make a get request to a given url
        :param url: The address url
        :return:
        """
        response = urequests.get(url)
        return response.json()


