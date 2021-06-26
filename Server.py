import socket,threading,json,math,os
from cryptography.fernet import Fernet, MultiFernet
from textwrap import wrap
import Utils,Lib,time

#Tools

class Status:
    WRONGVERSION = "Wrong Version"
    SUCCESS = "Success"
    NOTCOMMAND = "Invalid Command"
    NOFILE = "File Not Found"
    NEXTPACKET = "Content On Next Packet"


def send_Response(conn,net,status,message,file = "Shell",seperate = False):
    if not seperate:
        data = {
            "File": file,
            "Status":status,
            "Message":net.encrypt(message.encode()).decode()
        }
        conn.sendall(json.dumps(data).encode())
    if seperate:
        send = net.encrypt(message).decode()
        sends =[send[i:i + 65536] for i in range(0, len(send), 65536)]
        #print(sends)
        data = {
            "File": file,
            "Status":Status.NEXTPACKET,
            "Packs":len(sends),
            "Message":""
        }
        conn.send(json.dumps(data).encode())
        conn.recv(1024)
        for x in sends:
            conn.send(x.encode())

def establish_connection(conn,addr,size):
    data = json.loads(conn.recv(size).decode())
    name = data["User"]
    net = Utils.open_Key(name)
    
    if data["Version"]!=1:
        conn.send(b'{"Status":"Wrong Version","Message":""}')
        conn.close()
        return False,False
    if net.decrypt(data["Message"].encode()) != b"Test":
        conn.send(b'{"Status":"Incorrect Credentials","Message":""}')
        conn.close()
        return False,False
    conn.send(b'{"Status":"Success","Message":""}')
    print(f"{Utils.Colors.BMAGENTA}Connection Joined at {addr}")
    for x in Lib.GlobalData.Data["Scripts"].keys():
        Lib.Decorators.execScript(addr,x,"OnJoin",data["User"])
    
    return net,name

#Commands        

def command_Info(conn,addr,net,*args):
    send_Response(conn,net,Status.SUCCESS,'This is a basic terminal')

def command_Get(conn,addr,net,file,*args):
    if len(args)>0:
        send_Response(conn,net,Status.NOFILE,"",file="Shell")
        return None
    if not os.path.isfile(f"HostedData/Files/{file}"):
        send_Response(conn,net,Status.NOFILE,"")
        Lib.Tools.Console.Error(f"A Client, {addr}, Tried to Access {file} But Failed")
        return None
    with open(f"HostedData/Files/{file}",'rb') as f:
        send_Response(conn,net,Status.SUCCESS,f.read(),file=file,seperate=True)
        Lib.Tools.Console.Warn(f"A Client, {addr},Accessed {file}")

def command_Run(conn,addr,net,regName, func, *args):
    x = Lib.Decorators.execScript(addr,regName,func,*args)
    if x == False:
        send_Response(conn,net,"Script Not Found","")
        return None
    send_Response(conn,net,x[3],x[0],file=x[1],seperate=x[2])

#Server

def thread_Connection(conn,addr,size):
    #Asking for username in order to load proper Key Files
    net, name = establish_connection(conn, addr,size)
    if net==False:
        return None
    #Continues connection
    while True:
        msg = json.loads(net.decrypt(json.loads(conn.recv(size).decode())["Message"].encode()))
        command = msg["Command"]
        args = msg["Args"]
        if command=="Close":
            conn.close()
            break
        try:
            functions[command](conn, addr, net,*args)
        except Exception as e:
            print(e)
            send_Response(conn,net,Status.NOTCOMMAND,"")
    print(f"{Utils.Colors.BRED}Connection dropped at {addr}")
    for x in Lib.GlobalData.Data["Scripts"].keys():
        Lib.Decorators.execScript(addr,x,"OnLeave")


def server(config):
    HOST = config["Server"]["Host"]
    PORT = config["Server"]["Port"]
    SIZE = config["Server"]["Size"]
    print(f"{Utils.Colors.BOLD}{Utils.Colors.GREEN}Server is Hosting on {Utils.Colors.CYAN}{HOST}:{Utils.Colors.YELLOW}{PORT}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST,PORT))
    while True:
        sock.listen()
        conn,addr = sock.accept()
        x = threading.Thread(target=thread_Connection, args=(conn,addr,SIZE), daemon=True)
        x.start()

functions = {
    "Info": command_Info,
    "Get" : command_Get,
    "Run" : command_Run
}