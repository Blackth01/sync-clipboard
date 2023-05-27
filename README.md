# sync-clipboard
Application to sync clipboards of two computers

## Installation steps:
- ```python3 -m pip install -r requirements.txt```

Besides that, depending on the OS you're running, you'll perhaps need to install some other packages.

- On **Ubuntu** and other **Debian-based** distros: ```sudo apt install xsel```

- On **FreeBSD**: ```sudo pkg install xclip```

## Usage

The application works this way:

- To run it, execute ```python3 main.py```
- It'll ask two options: "s" (to run it as a server) and "c" (to run it as a client). One computer should be the server, and the other should the client, connecting to the IP and port of the server
