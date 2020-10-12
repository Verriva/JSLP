import configparser
import subprocess
import socket
import time
import json
import re

def Ip_Host():
    Ip = subprocess.getoutput("hostname -I")
    Espacio = Ip.find(" ")
    Ip = Ip[0:Espacio]
    return Ip

def configuration():
    config = configparser.ConfigParser()
    config.read('JSLP_Conf.ini')
    return config

def scanNetwork():

    process = subprocess.Popen(['nmap', '-sn', '192.168.0.0/24'], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    result = stdout.decode("utf-8")
    
    ipList = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result)

    return ipList

def socketClient(HOST, PORT, usr, passwd):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    credentials = f"{{\"User\":\"{usr}\", \"Password\":\"{passwd}\"}}"
    print(f"MONITOR TO: {ip} --------------------------------")
    
    try:
        sock.connect((ip,PORT))
        sock.sendall(bytes(credentials, "utf-8"))
        data = sock.recv(1024)
        data = data.decode("utf-8") 

        return data

    except Exception as identifier:
        print(identifier)

    finally:
        print(f"Close for: {ip}")
        sock.close()

def writeJsonScann(dict):
    
    with open("JSLP_ScannerData.json","w+") as f:
        json.dump(dict, f, indent=4)

if __name__ == "__main__":

    conf  = configuration()

    monitor = int(conf['JSLP']['monitorTime'])
    userP = conf['JSLP']['user']
    passP = "QUEer12#$"
    PORT = 11011

    while True:

        time.sleep(monitor)
        scanner = scanNetwork()
        reportScann = {}

        for ip in scanner:

            report = socketClient(ip, PORT, userP, passP)

            if report is not None:
                report = json.loads(report)
                reportScann.update({ip:report})

        writeJsonScann(reportScann)