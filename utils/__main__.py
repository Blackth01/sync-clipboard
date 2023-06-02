import socket
import threading
import pyperclip

from threading import Event
from time import sleep

class SyncClipboard:
    def __init__(self, print_msg):
        self.last_text_on_clipboard = pyperclip.paste()
        self.print_msg = print_msg 

    def check_if_clipboard_changed(self, client_socket, is_stopped):
        while not is_stopped.is_set():
            sleep(0.5)
            current_text_on_clipboard = pyperclip.paste()
            if(current_text_on_clipboard != self.last_text_on_clipboard):
                self.last_text_on_clipboard = current_text_on_clipboard
                self.print_msg(f"Will send: {current_text_on_clipboard}")
                client_socket.send(current_text_on_clipboard.encode())

    def listen_to_messages(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            self.print_msg(f"Will copy: {data}")
            self.last_text_on_clipboard = data
            pyperclip.copy(data)

    def start_threads(self, client_socket):
        is_stopped = Event()
        clipboard_checker = threading.Thread(target=self.check_if_clipboard_changed, args=(client_socket,is_stopped))
        clipboard_checker.start()

        self.listen_to_messages(client_socket)

        is_stopped.set()

    def start_server(self, port=None):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '0.0.0.0'
        if(not port):
            port = int(input("Enter the port you want to listen on: "))

        server_socket.bind((host, port))
        server_socket.listen(1)

        self.print_msg(f"Server listening on {host}:{port}")

        self.last_text_on_clipboard = pyperclip.paste()

        while True:
            client_socket, client_address = server_socket.accept()
            self.print_msg(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            self.start_threads(client_socket)


    def start_client(self, host=None, port=None):
        if(not host):
            host = input("Enter the server host you want to connect to: ")

        if(not port):
            port = int(input("Enter the server port you want to connect to: "))

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.last_text_on_clipboard = pyperclip.paste()

        try:
            client_socket.connect((host, port))
            self.print_msg(f"Connected to {host}:{port}")
            self.start_threads(client_socket)
        except ConnectionRefusedError:
            self.print_msg("Connection refused. Make sure the server is running.")
        finally:
            client_socket.close()