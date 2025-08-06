from scapy.all import *

packets = rdpcap("blitzhack_traffic.pcap")

# Collect all TCP payloads
payloads = [
    pkt[Raw].load
    for pkt in packets
    if pkt.haslayer(TCP) and pkt.haslayer(Raw)
]

# Write to PNG if data exists
if payloads:
    with open("recovered_secret.png", "wb") as f:
        f.write(b"".join(payloads))
    print("âœ… PNG file recovered successfully!")
else:
    print("âš ï¸ No payloads found.")