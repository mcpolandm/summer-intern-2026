import ipaddress
import sys

if len(sys.argv) > 1:
    ip = sys.argv[1]

ip_addr = ipaddress.ip_network(ip)

print(f"Network Address: {ip_addr.network_address}")
print(f"Boardcast Address: {ip_addr.broadcast_address}")
print(f"Useable Host Addresses: {list(ip_addr.hosts())}")

other_ip = input("Input IP address: ")
if (ipaddress.ip_address(other_ip) in list(ip_addr.hosts())):
    print("Valid in network")
else:
    print("Not in network")