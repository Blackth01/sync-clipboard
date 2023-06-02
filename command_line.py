from utils import SyncClipboard

def show_msg(text):
    print(text)

def main():
    print("Welcome to sync-clipboard!")
    print("Would you like this instance to be executed as the server, or the client?\
        \nIf you already started a server in the other computer, this one should be the client")
    option = input("Enter \"s\" to run as a server and \"c\" to run as a client: ")

    sc = SyncClipboard(print_msg=show_msg)

    if option.lower() == "s":
        sc.start_server()
    elif option.lower() == "c":
        sc.start_client()
    else:
        print("Invalid option, sorry :/. It must be only \"c\" or \"s\"")

if __name__ == '__main__':
    main()