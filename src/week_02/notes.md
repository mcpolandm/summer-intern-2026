---
title: "Week 2 Notes"
toc: true
---

<div class="note">
You can place notes in this file in any mix of Markdown, HTML, CSS, and JavaScript.
</div>

# Week 2 — Notes

OSI Model-Breakdown of the fundamental processes involved in communication between parts of a network

- 7 layers build bottom up from the physical transmission of data to the software systems and models that fascilitate communication

## Layer 1: Physical
- Manages transmission of 0s and 1s through wire or radio waves. 
- Involves cables, hubs, modems
- Clock synchronization
- What data is sent and the manner it is sent is controlled by higher layers

## Layer 2: Data Link
- Splits data packets into Frames to be sent in the physical layer
- uses MAC address to identify destination
- Switches and Bridges use this layer
- Controls rate of flow of information and detects lost or damaged frames
- The data sent and its destination is controlled by higher layers

## Layer 3: Network
- Handles the path finding to the destination
- Uses IP addresses to identify sender and receiver, as well as path stops
- Routes data along physical path based on IP address
- Data is encased in packets. Packet headers are from each layer above and below and contain information
- Layer 3 header includes IP address. Layer 2 has MAC address
- Routers and Switches use this layer
- The data sent and the appropriate communication is handled by higher layers

## Layer 4: Transport
- ensures the delivery of the data
- Data is broken into segments here
- Uses port numbers to ensure delivery to correct process (where the destination user is expecting it)
- Handles splitting anf reconstruction of data here
- Uses TCP or UCP protocols
- The data sent and communication management is handled by higher layers

## Layer 5: Session
- manages the opening, security, and closing of the communication
- Determines duplex/half-duplex communication
- Uses checkpoints to handle communication failures

## Layer 6: Presentation
- Ensures the data is properly formatted and secured
- Handles data formats like JPEG, GIF, etc
- Handles encyption/decryption

## Layer 7: Application
- Handles direct interfacing between user and the network
- Produces the data to be sent and the data received
- Uses HTTPS, FTP, DNS, etc

## The Packet

IP-destination info{TCP/UDP-info about packet(Some encryption [Raw data])}

Then split into Frames that add MAC address info


## IP
- The address for a node on the netwrok that other nodes can find it at
- Often changes upon each connection to the network
- For IPv4, format xxx.xxx.xxx.xxx
- IPv6 is hex, xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx
- IPv4 can have /xx after, designated how many bits represent the network (32-xx represents the host itself)
- IP often assigned by router

## TCP
- handles communication between sender and receiver so that data is error-free
- Making connection requires three-way handshake: sender sends SYN, receiver sends SYN-ACK, sender sends ACK
- Each data segment has a TCP header so receiver can verify order and check for corruption
- Receiver sends ACK for each non-errored packet it receives, sender retransmits after a time with no ACK
- Three-way handshake to close
- TCP also ensures that the data flow is such that everything is received, while also limiting traffic congestion

## UDP
- TCP but the goal is speed over correctness
- no guaruntee that the data makes it or is free of errors
- simply splits into packets and sends, with no prior connection or error handling
- good for high speed connection with dropped packets (streaming)

## Routing
- Say a node is transmitting some packet
- looks at IP header for destination IP
- If this IP is in the node's routing table, it knows where to send packets for this IP and sends them away
- If not, they go to the default gateway
- Follows this process to the destination or too many nodes visited

## Ethernet
- Upon reaching the correct network, the data then needs to be sent to the specific device through it's physical MAC address
- Router uses ARP to figure out what the MAC address is for the destination IP (asks everyone on LAN, target responds with MAC)
- Packets are then further broken into frames to transmit to destination

## DNS
- websites use DNS to connect their IP to a human-readable string (google.com)
- check locally if that name is stored
- if not ask root DNS server, who gives result or a drilled down server to ask
- repeat until IP is provided
- IP is cached for some time to limit traffic to root servers

# Lab Notes
Results from this week's lab

## Wireshark

1. ARP requests are to retrieve MAC addresses given IP addresses, so they are only meant to be run on the local area network, rather than across the whole internet. Therefore, only devices with a local IP address will respond to any ARP queries. Given the requester's IP is 193.24.225.56, we know 1.1.1.1 is not an IP on the local network. Therefore, no devices will respond to the ARP query, because there is no device with the IP 1.1.1.1 that will receive the query.

2. The purpose of a gratuitous ARP is to update the ARP tables of every other device on the local network. A gratuitous ARP is sent when the sender has had the details of their connection updated, usually the IP address, but potentially the MAC address. This can happen if the device disconnects and then reconnects to the network. The gratuitous ARP allows the network devices to be aware of this change rather than needing to send an ARP query later, or forward some other data to the wrong destination.

3. The response of "No such name" indicates that the target domain is not listed in the domain servers. Basically, there is no record in the server for a domain with that name. This means the DNS protocol aims to return an IP address to access a domain, but if that is not possible, it may also return information why. Instead of dropping the request, the server tells the requester that the domain doesn't exist. The acronyms A, AAAA, SOA, and TXT represent Host Address, IPv6 Address, Start Of A Zone Of Authority, and Text Record respectively. They are different types of DNS records, essentially what kind of data the requester is looking for. A website would be A, a website on IPv6 would be AAAA, a DNS zone start of authority, or where information about DNS records are kept, would be SOA, and text information about a domain would be TXT.

4. When closing a connection, both sides must receive a FIN and an ACK acknowledging it's own FIN before closing. Here, the client sends a FIN, ACK to say "I got all your data, let's close the connection". The server sends FIN, PSH, ACK, not just a FIN, ACK, which implies there was more data left for the server to send. This FIN, PSH, ACK says "Here's the last bit of data. I saw you wanted to close, so I will close too." Then the client sends an ACK to say "I see you have closed". This all follows the closing procedure correctly, but the server then sends 4 RST packets. Given that this was a live SSH connection, and there was a PSH sent from the server during the closing, it seems that the SSH process and the TCP handshake had a timing issue on the server's side. This could have caused the connection to close early or some other issue affected the connection, so when the final ACK was sent the server followed the usual process for receiving packets from a closed connection, which is 4 RST packets.

5. A layer would resend the same information if it believed or knew that the information did not reach the destination. For TCP connections, all packets received must be acknowledged with an ACK to confirm the packet reached the destination and was intact. After some time with no ACK, the sender will resend the packet. Different layers handle this dropped packet handling differently. UDP, on the same layer as TCP, does not handle this at all. IP and MAC address communications use checksums in the header for the receiver to see if the data was altered, and send a request to retransmit the data in this instance.

6. Questions:
- What exactly is BGP? What is the difference between BGP open and a TCP handshake?
- IP and MAC have error handling, but do they have dropped packet handling too like TCP?
- What is the purpose in asking for a SOA? What can the requester do with that?
