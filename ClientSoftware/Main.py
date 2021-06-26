import socket,json,io
from cryptography.fernet import Fernet, MultiFernet
import Utils
from getpass import getpass


HOST = "localhost"
PORT = 1300
BIGSIZE= 65536

def send_Response(sock,net,message):
    data=b'{"Message":"'+net.encrypt(message)+b'"}'  #send first bit of json
    sock.sendall(data)

def recv(sock):
    data=sock.recv(1024).decode()
    print(data)
    return json.loads(data)

def recvAll(sock,net,packets):
    sock.settimeout(5.0)
    output = b""
    try:
        for x in range(packets):
            output+=sock.recv(BIGSIZE)
        sock.settimeout(None)
    except:
        None
    return output

def format_request(text):
    splitT = text.split(' ')
    command = splitT[0]
    args=[]
    if len(splitT)>1:
        args = text.split(' ')[1::]
    output = {
        "Command":command,
        "Args": args
    }
    #print(json.dumps(output).encode())
    return json.dumps(output).encode()

def establish_connection(sock,net):
    sock.sendall(('{"Version":1,"User":"'+Utils.hashString(name)+'","Message":"'+net.encrypt(b"Test").decode()+'"}').encode())
    data=json.loads(sock.recv(1024).decode())
    print(data)
    if data["Status"] == "Success":
        return True
    return False


if __name__=='__main__':
    name = input(f'{Utils.Colors.GREEN}Username {Utils.Colors.BRED}>{Utils.Colors.RESET} ')
    password = getpass(prompt=f'{Utils.Colors.GREEN}Password {Utils.Colors.BRED}>{Utils.Colors.RESET} ').encode()
    net = Utils.open_Key(name,password)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        connected = establish_connection(sock,net)

        print('\n\n----------------------\n')
        while connected:
            inp = input(f'{Utils.Colors.BRED}> {Utils.Colors.RESET}')
            send_Response(sock,net,format_request(inp))
            if inp.startswith("Close"):
                break
            data=recv(sock)
            if data["File"] == "Shell":
                if data["Status"] == "Success":
                    response = net.decrypt(data["Message"].encode()).decode()
                    print(f'{Utils.Colors.CYAN}{response}')
                else:
                    print(f'{Utils.Colors.RED}{data["Status"]}')
            else:
                #response = net.decrypt(data["Message"].encode())
                content = b""
                sock.send(b'This is just a buffer')
                if data["Status"] == "Content On Next Packet":
                    content = recvAll(sock, net, data["Packs"])
                #print(content)
                with open(f'Files/Downloads/{data["File"]}','wb') as f:
                    f.write(net.decrypt(content))
                print(f'{Utils.Colors.YELLOW}Content Written to File "./Files/Downloads/{data["File"]}"')
        if not connected:
            print("Unable to establish connection (Most Likely the wrong password)")
        