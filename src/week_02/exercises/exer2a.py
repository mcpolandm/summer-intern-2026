from scapy.all import rdpcap
from collections import Counter

packets = rdpcap("The-Ultimate-PCAP.pcapng")  # adjust the filename/path as needed
print(f"Loaded {len(packets)} packets")
packets[0].show()   # inspect the first packet to get your bearings

proto_counts = Counter()
for pkt in packets:
    proto_counts[pkt.lastlayer().name] += len(pkt)

for proto, count in proto_counts.most_common(15):
    print(f"{proto:<30} {count}")