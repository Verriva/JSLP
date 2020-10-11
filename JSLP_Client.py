import subprocess
import socket
import re

def Ip_Host():
    Ip = subprocess.getoutput("hostname -I")
    Espacio = Ip.find(" ")
    Ip = Ip[0:Espacio]
    return Ip

def scanNetwork():

    process = subprocess.Popen(['nmap', '-sn', '192.168.0.0/24'], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    result = stdout.decode("utf-8")
    
    ipList = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result)

    return ipList

if __name__ == "__main__":
    host = Ip_Host()
    port = 11011

    HOST = '192.168.0.13'
    PORT = 11011


    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #    s.connect((HOST, PORT))
    #    s.sendall(b'{"User":"ironMan2020","Password":"QUEer12#$"}')
    #    data = s.recv(1024) 
    #    print('Received', repr(data))

    scanner = scanNetwork()
    print(scanner)

    for ip in scanner:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"MONITOR TO: {ip} --------------------------------")
        
        try:
            sock.connect((ip,PORT))
            sock.sendall(b'{"User":"ironMan2020","Password":"QUEer12#$"}')
            data = sock.recv(1024) 
            print('Received', repr(data))
        except Exception as identifier:
            print(identifier)
        finally:
            sock.close()
        
        
        