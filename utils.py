import json

def lstServersServices():
    with open('JSLP_ScannerData.json') as f:
        data = json.load(f)
    
    for item in data:
        print(item)

lstServersServices()