import json
import urequests
import machine
import time

try:
    import usocket as socket
except:
    import socket

import src.json_helper as json_helper

RESPONSE_HEADER = '''HTTP/1.1 200 OK\r\nPOST HTTP/1.1\r\nHost: 192.168.1.115\r\nContent-Type: 
text/json\r\nContent-Length: {length}\r\n\r\n '''


class ConnectionHandler:
    """
    Handles connections to the user controller.
    Primary focus are incoming messages, however also sends back data
    """

    def __init__(self, task_manager, setup_mode):
        address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self._socket = socket.socket()
        self._socket.bind(address)
        self._socket.listen(1)
        self._socket.setblocking(False)
        self._socket.settimeout(5)

        self._task_manager = task_manager

        self._setup_mode = setup_mode

        print('New Socket is listening on: ', address, "Setupmode is:", setup_mode)

    def update_socket(self):
        """
        Checks for incoming connection and parses them if needed
        :return: The post data json, or [] if the socket times out
        """
        client = None
        try:
            client, address = self._socket.accept()
            data = self.receive_all_data(client)
        except OSError:
            pass
        if client is not None:
            print("New request from:", address)
            if self._setup_mode:
                if self.handle_setup_connection(client, data):
                    machine.reset()
            else:
                self.handle_connection(client, data)

    def receive_all_data(self, current_socket):
        data = current_socket.recv(8192)
        data = str(data)
        data = data[data.find('{'):-1]
        data_json = json.loads(data)
        return data_json

    def handle_data(self, client, data_json):
        """
        Handles incoming connections.
        Checks what type of connection was made and pipes the given data towards the right handler.
        Then returns a success message back to the client
        :param data_raw:
        :return:
        """
        try:
            request_type = data_json['load']['request_type']
            if request_type == 'get':
                return_data = self._task_manager.on_get_request(data_json['load'])
            else:
                return_data = json.dumps('{"received": True}')
        except ValueError:
            return_data = json.dumps('{"received": True}')
        client.sendall(RESPONSE_HEADER.format(length=len(return_data)))
        client.sendall(return_data)
        client.close()
        if request_type == 'post':
            self._task_manager.on_new_post(data_json['load'])

    def handle_setup_connection(self, client, data_json):
        """
        Handles incoming setup connections.
        :param data_raw:
        :return:
        """
        reboot = False
        data_json = data_json['load']
        print("Got new setup message:", data_json)
        request_type = data_json['type']
        if request_type == "set_network":
            data = data_json['data']
            print("Setting up with data: ", data)
            json_helper.update_json_value("credentials", ["name"], data['name'])
            json_helper.update_json_value("credentials", ["password"], data['password'])
            return_data = json.dumps('{"received": True}')
            reboot = True
        elif request_type == "is_lighthub":
            return_data = json.dumps('{"is_lighthub": True}')
        else:
            return_data = json.dumps('{"received": False}')
        client.sendall(RESPONSE_HEADER.format(length=len(return_data)))
        client.sendall(return_data)
        client.close()
        return reboot

    @staticmethod
    def make_get_request(url):
        """
        Static function to make a get request to a given url
        :param url: The address url
        :return:
        """
        response = urequests.get(url)
        return response.json()


