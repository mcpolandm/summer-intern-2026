from scapy.all import IP
from collections import defaultdict
from scapy.all import rdpcap

packets = rdpcap("The-Ultimate-PCAP.pcapng")  # adjust the filename/path as needed
print(f"Loaded {len(packets)} packets")

conversations = {}

for pkt in packets:
    if not pkt.haslayer(IP):
        continue

    src = pkt[IP].src
    dst = pkt[IP].dst
    size = len(pkt)

    # Find existing conversation in either direction
    if (src, dst) in conversations:
        conv = conversations[(src, dst)]
        conv["fwd"] += size

    elif (dst, src) in conversations:
        conv = conversations[(dst, src)]
        conv["rev"] += size

    else:
        conversations[(src, dst)] = {
            "fwd": size,   # SRC -> DST
            "rev": 0,      # DST -> SRC
            "pkts": 0,
        }
        conv = conversations[(src, dst)]

    conv["pkts"] += 1

top = sorted(
    conversations.items(),
    key=lambda kv: kv[1]["fwd"] + kv[1]["rev"],
    reverse=True
)

print(f"{'SRC':<16} {'DST':<16} {'SRC→DST bytes':>10} {'DST→SRC bytes':>10} {'pkts':>6}")

for (src, dst), v in top[:20]:
    print(
        f"{src:<16} {dst:<16} "
        f"{v['fwd']:>10} {v['rev']:>10} {v['pkts']:>6}"
    )