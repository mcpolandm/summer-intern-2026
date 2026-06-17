---
title: "Week 3 Notes"
toc: true
---

<div class="note">
You can place notes in this file in any mix of Markdown, HTML, CSS, and JavaScript.
</div>

# Week 3 — Notes

## What I learned

## IP
- networks connect on layer 2 via ethernet
- internetworks connect two networks on layer 3 via IP
- best effort delivery- no error handling
- IP is designed to be simplistic so it can run over anything
- IP header contains IPv4 vs 6 info, header and packet length, source and destination, checksum, and other info
- all networks have a maximum transmission unit, packets may be split up if they are larger, header has info on disassembly/reassembly
- IP forwarding-check if IP is in network, check if IP is in table, otherwise default gateway
- forward to longest match in the table
- ICMP handles IP erorr messaging
- 

## Subnets
- networks inside networks
- smaller "accounting" nextwork inside larger company network
- ISPs give subnets to customers
- Subnet mask shows distinction between network and host portions, can split these further

## Routing
- routes are picked based on internal routing tables
- static-set once by owner
- dynamic-updating based on availability
- Border Gateway Protocol allows routers to know what other routers are connected to them
- Open Shortest Path First uses shortest path algorithm on distance and speed to route
- Routing Information Protocol uses shortest by hop count

## VLANs
- split one switch into multiple
- traffic cannot cross a VLAN boundary
- each VLAN has seperate mAC address table
- can combine multiple physical switches to one VLAN
- Access ports are only one VLAN, trunk ports are multiple`
- trunk ports attach tags to L2 header saying which VLAN it is for
- Native VLAN-the VLAN untagged traffic is assigned to on that switch
- both sides should be configured with same native VLAN

## LLDP
- used by devices to share identity, capabilities, and neighbors
- useful for network management
- queries via SNMP commands, outputs from MIB
- 

## Questions
- Why use VLANs to break up ports of one switch, rather than just using the one switch as is?
- Do most/all layer 3 switches use VLANs?
- How are routing tables determined at FI? static/dynamic
- 


# Labs

## Lab 1
- ARP table entries can have one of 9 states, including permanent (always valid), noarp (valid), reachable (valid until expiry), stale (valid but suspicious/expired), none (in setup), incomplete (not validated), delay (being validated), probe (probing neighbor), failed.

- looking at the LLDP information on eth0 shows both the switch and the other host, while eth1 only shows the switch. It shows info like name, system, IP, Mac, etc.

- MAC address table entry seems to be populated from the ping. If the addresses were missing, the switch would not have knowledge of how to directly reach either of the hosts, so it would just flood the whole network when trying to contact one.

## Lab 2
- Even though the traffic from host1 to host2 is now routed through layer3, layer2 communication still needs to happen. Host1 uses layer2 to first send to the switch, and host2 uses layer2 to send the response to the switch. These interactions allow the switch to add both MAC addresses, even though the MAC address isn't what's used to send along communication between VLAN10 and VLAN20.

## What confused me

## Artifacts captured

A MAC/ARP/routing table dump, your subnet helper's output, a sketch of the topology graph.
