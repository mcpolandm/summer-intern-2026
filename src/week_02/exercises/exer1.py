from scapy.all import Ether, IP, UDP, DNS, DNSQR, ARP

# Build a DNS query packet layer by layer and inspect the result
pkt = Ether() / IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="example.com"))
pkt.show()        # full field-by-field breakdown
pkt.summary()     # one-line summary

pkt2 = Ether() / ARP()
pkt2.show()
pkt2.summary()