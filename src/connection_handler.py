import json
import urequests
import machine
import time

import usocket as socket


import src.json_helper as json_helper

RESPONSE_HEADER = '''HTTP/1.1 200 OK\r\nPOST HTTP/1.1\r\nHost: 192.168.1.115\r\nContent-Type: 
text/json\r\nContent-Length: {length}\r\n\r\n '''


class ConnectionHandler:
    """
    Handles connections to the user controller.
    Primary focus are incoming messages, however also sends back data
    """

    def __init__(self, task_manager, setup_mode):
        address_info = socket.getaddrinfo('0.0.0.0', 80)
        address = address_info[0][-1]

        self._socket = socket.socket()
        self._socket.bind(address)
        self._socket.listen(1)
        self._socket.setblocking(False)
        self._socket.settimeout(5)

        self._task_manager = task_manager

        self._setup_mode = setup_mode

        print('New Socket is listening on: ', address, "Setup-mode is:", setup_mode)

    def update_socket(self):
        """
        Checks for incoming connection and parses them if needed
        :return: True if controller needs to restart, false otherwise
        """
        client = None
        try:
            client, address = self._socket.accept()
        except OSError:
            return False
        print("New connection from: {}".format(address))
        data, success = self.receive_all_data(client)

        if client is not None and success:
            if self._setup_mode:
                return self.handle_setup_connection(client, data)
            else:
                self.handle_data(client, data)
                return False
        else:
            print("Error while receiving a valid connection!")

    @staticmethod
    def receive_all_data(current_socket):
        """
        Parses all data from the socket and returns a json of it
        :param current_socket: The to parse from client
        :return: The parsed json
        """
        data = ""
        content_length = 99999
        set_length = False
        while len(data) < content_length:
            parsed_data = current_socket.recv(512)
            data += parsed_data.decode("utf-8")
            if not set_length:
                length = data[data.find("Content-Length:"):]
                length = length[length.find(":")+2:]
                length = length[:length.find('\n')-1]
                content_length = int(length)
                set_length = length
                data = data[data.find('{'):]
        # print("Loaded data! Size -> should: {}, have: {}, data: {}".format(content_length, len(data), data))
        try:
            return json.loads(data), True
        except:
            return [], False

    def handle_data(self, client, data_json):
        """
        Handles incoming connections.
        Checks what type of connection was made and pipes the given data towards the right handler.
        Then returns a success message back to the client
        :param client: The socket client
        :param data_json: The data json
        :return:
        """
        try:
            return_data = self._task_manager.on_request(data_json['load'])
        except ValueError:
            return_data = json.dumps({"received": False})
        client.sendall(RESPONSE_HEADER.format(length=len(return_data)+1))
        client.sendall(return_data)
        client.close()

    @staticmethod
    def handle_setup_connection(client, data_json):
        """
        Handles incoming setup connections.
        :param client: The socket client
        :param data_json: The data json
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
            return_data = json.dumps({"received": True})
            reboot = True
        elif request_type == "is_lighthub":
            return_data = json.dumps({"is_lighthub": True})
        else:
            return_data = json.dumps({"received": False})
        client.sendall(RESPONSE_HEADER.format(length=len(return_data)+1))
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


