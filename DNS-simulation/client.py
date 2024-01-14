import socket
import sys

def get_ip_address(host):
    port = int(sys.argv[1])

    for domain in host.split(','):
        domain = domain.strip()
        s = socket.socket()  # Create a new socket for each request
        print(f"Socket Created for {domain}")

        try:
            s.connect(('127.0.0.1', port))
        except socket.error as e:
            print(f"Socket connection error: {e}")
            continue

        s.sendall(domain.encode())
        print(f"IP requested to Server for {domain}")
        
        try:
            msg = s.recv(1024)
        except socket.error as e:
            print(f"Error receiving data for {domain}: {e}")
            s.close()
            continue

        ip_address = msg.decode("utf-8")

        if ip_address != "Not Found":
            link = f'<a href="http://{ip_address}">{domain}</a>'
            print(f"IP obtained from server for {domain}: {ip_address}")
            print(f"Clickable link for {domain}: {link}")
        else:
            print(f"IP not found for {domain}")

        s.close()

if __name__ == "__main__":
    print("DNS CLIENT", "1 -> Single Input", "2 -> Multiple Inputs", "3 -> Quit", sep="\n")

    while True:
        choice = int(input())
        if choice == 1:
            host = input("Enter a domain name: ")
            get_ip_address(host)
        elif choice == 2:
            hosts = input("Enter multiple domain names separated by commas (e.g., google.com, medium.com): ")
            get_ip_address(hosts)
        elif choice == 3:
            print("Client is shutting down...")
            break
        else:
            print("Please enter a valid choice.")
