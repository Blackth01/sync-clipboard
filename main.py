import socket
import threading
import pyperclip

from threading import Event
from time import sleep

last_text_on_clipboard = pyperclip.paste()

def check_if_clipboard_changed(client_socket, is_stopped):
    global last_text_on_clipboard

    while not is_stopped.is_set():
        sleep(0.5)
        current_text_on_clipboard = pyperclip.paste()
        if(current_text_on_clipboard != last_text_on_clipboard):
            last_text_on_clipboard = current_text_on_clipboard
            print(f"Will send: {current_text_on_clipboard}")
            client_socket.send(current_text_on_clipboard.encode())

def listen_to_messages(client_socket):
    global last_text_on_clipboard

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(f"Will copy: {data}")
        last_text_on_clipboard = data
        pyperclip.copy(data)

def start_server():
    global last_text_on_clipboard

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = int(input("Enter the port you want to listen on: "))

    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    last_text_on_clipboard = pyperclip.paste()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        is_stopped = Event()
        clipboard_checker = threading.Thread(target=check_if_clipboard_changed, args=(client_socket,is_stopped))
        clipboard_checker.start()

        listen_to_messages(client_socket)

        is_stopped.set()


def start_client():
    global last_text_on_clipboard

    host = input("Enter the server host you want to connect to: ")
    port = int(input("Enter the server port you want to connect to: "))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    last_text_on_clipboard = pyperclip.paste()

    try:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")
        is_stopped = Event()
        clipboard_checker = threading.Thread(target=check_if_clipboard_changed, args=(client_socket,is_stopped))
        clipboard_checker.start()
        listen_to_messages(client_socket)
        is_stopped.set()
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    finally:
        client_socket.close()

def main():
    print("Welcome to sync-clipboard!")
    print("Would you like this instance to be executed as the server, or the client?\
        \nIf you already started a server in the other computer, this one should be the client")
    option = input("Enter \"s\" to run as a server and \"c\" to run as a client: ")
    if option.lower() == "s":
        start_server()
    elif option.lower() == "c":
        start_client()
    else:
        print("Invalid option, sorry :/. It must be only \"c\" or \"s\"")

if __name__ == '__main__':
    main()