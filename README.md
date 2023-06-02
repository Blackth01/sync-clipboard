# sync-clipboard
Application to sync clipboards of two computers

## Installation steps:
- ```python3 -m pip install -r requirements.txt```

Besides that, depending on the OS you're running, you'll perhaps need to install some other packages.

- On **Ubuntu** and other **Debian-based** distros: ```sudo apt install xsel```

- On **FreeBSD**: ```sudo pkg install xclip```

## Usage

### Command line
The usage using the command line works this way:

- To run it, execute ```python3 command_line.py```
- It'll ask two options: "s" (to run it as a server) and "c" (to run it as a client). One computer should be the server, and the other should the client, connecting to the IP and port of the server

### GUI
The application also has a graphical interface. To run it, execute ```python3 gui.py```

![Main_screen](https://github.com/Blackth01/sync-clipboard/blob/main/screenshots/initial_screen2.png?raw=true)
