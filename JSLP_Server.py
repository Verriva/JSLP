from datetime import datetime
import configparser
import subprocess
import hashlib
import socket
import json

def configuration():
    config = configparser.ConfigParser()
    config.read('/etc/jslp/JSLP_Conf.ini')
    return config

def Ip_Host():
    Ip = subprocess.getoutput("hostname -I")
    Espacio = Ip.find(" ")
    Ip = Ip[0:Espacio]
    return Ip

def jsonReadUpdate():

    with open('/etc/jslp/JSLP_ServerConf.json','r+') as f:
        data = json.load(f)
        data['ServerIP'] = Ip_Host()
        data['TimeStamp'] = str(datetime.now())
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    return json.dumps(data)

def validatePassword(request):

    request = json.loads(request.decode('utf-8'))

    user  = request['User']
    passw = request['Password']
    passw = encrypt_string(passw)

    conf  = configuration()
    userP = conf['JSLP']['user']
    passP = conf['JSLP']['pass']

    return True if (user==userP and passw==passP) else False


def encrypt_string(hash_string):

    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    
    return sha_signature

def socketServer(HOST, PORT):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)

    while True:

        conn, addr = sock.accept()
        print('Connected by: ', addr)
        try:
            jsonFile = jsonReadUpdate()
            data = conn.recv(1024)
            if not data: break
            if validatePassword(data):
                arr = bytes(jsonFile, 'utf-8')
                conn.sendall(arr)
        finally:
            conn.close()

if __name__ == "__main__":
    host = Ip_Host()
    port = 11011
    jsonFile = jsonReadUpdate()
    socketServer(host, port)