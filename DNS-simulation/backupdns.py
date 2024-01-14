import socket
import json
import sys
import csv
import threading

def dns(input):
    flag = 0
    file1 = open("data.json", "r")
    localdata = json.loads(file1.read())
    file1.close()
    for key, val in localdata.items():
        if input == key:
            addr = val
            flag = 1
    if flag == 0:
        try:
            addr = socket.gethostbyname(input)
            localdata[input] = addr
        except socket.gaierror as se:
            addr = "Not Found"
        file1 = open("data.json", "w")
        file1.write(json.dumps(localdata))
        file1.close()
    return addr

def handle_client(c):
    data = c.recv(1024).decode()
    print(data)
    result = dns(data)
    print(result)
    c.send(bytes("".join(result), "utf-8"))
    c.close()

def start_server():
    s = socket.socket()
    port = int(sys.argv[1])
    print("Socket created")
    s.bind(('', port))
    print("Socket bound to port", port)
    s.listen(15)
    print("Socket is listening")
    reset_data_count = 0

    while True:
        c, addr = s.accept()
        reset_data_count += 1
        if reset_data_count == 5:
            refresh_server_data()
        print("Connection received")

        # Create a new thread to handle the client request
        client_thread = threading.Thread(target=handle_client, args=(c,))
        client_thread.start()

def refresh_server_data():
    localdata = {}
    l = []

    with open('top500Domains.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            name = "".join(row[1])
            l.append(name)

    t = 0
    print("Refreshing", end="\n")
    for remote_host in l:
        remote_host = remote_host.strip()
        try:
            addr = socket.gethostbyname(remote_host)
            localdata[remote_host] = addr
        except socket.gaierror as se:
            addr = "Not Found"
        print((t / len(l)) * 100, end='\r')
        t += 1

    file1 = open("data.json", "w")
    file1.write(json.dumps(localdata))
    print("Dataset Successfully refreshed")

if __name__ == "__main__":
    flag = 1
    print("DNS SERVER", "1  -> Start server", "2  -> Refresh server data", "3  -> Quit", sep="\n")

    while flag:
        t = int(input())
        if t == 1:
            start_server()
        elif t == 2:
            refresh_server_data()
        elif t == 3:
            print("Shutting down the server...", "Successfully shutdown", sep="\n")
            flag = 0
        else:
            print("Please enter a valid choice")
