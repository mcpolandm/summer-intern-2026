from scapy.all import DNS, DNSQR, DNSRR, IP
from scapy.all import rdpcap


packets = rdpcap("The-Ultimate-PCAP.pcapng")  # adjust the filename/path as needed
print(f"Loaded {len(packets)} packets")

query_results = {}

for pkt in packets:
    try:
        if not pkt.haslayer(DNS):
            continue

        dns = pkt[DNS]

        if dns.qr == 0 and dns.qd:   # qr=0 is a query
            qname = dns.qd.qname.decode().rstrip(".")
            #print(f"QUERY  {pkt[IP].src:<16} → {qname}")

        elif dns.qr == 1 and dns.an:  # qr=1 is a response, an=answer section
            name = dns.an.rrname.decode().rstrip(".")
            rdata = dns.an.rdata
            ttl   = dns.an.ttl
            rcode = dns.rcode
            #print(f"ANSWER {name:<40} → {rdata}  (TTL {ttl}s, rcode {rcode})")
            query_results[name] = rdata
    except Exception as e:
        # We dont really care about exceptions, some packets fail to parse which is fine
        # just ignore them and move on.
        continue

print([k for k, v in query_results.items() if v == "5.35.226.136"])