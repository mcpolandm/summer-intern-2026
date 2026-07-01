---
title: "Week 5 Notes"
toc: true
---

<div class="note">
You can place notes in this file in any mix of Markdown, HTML, CSS, and JavaScript.
</div>

# Week 5 — Notes

## What I learned
Reading notes
### SFLOW
- One collector central to the network that stores and operates on sFlow data
- prevents large encumbrance on actual network hosts
- Agents use sampling to randomly select data to share with collector
- Agents have a sampling rate (1 in N) such that they collect that many packets to send to collector
- has internal counter decremeneted by each packet received, forwards and resets when counter is 0
- sample by compying the header and forwarding it
- higher rate -> more accurate but more encumbrance
- agent will also periodically sample its counter record (number of in/out bits)
- counter sampling rate set by sampling interval
- uses SNMP for counter sampling, datagram forwarding through UDP for packet sampling
- sFlow MIB has configurations

### Sampling Review
- network managers need data about the use of different connections in order to best manage them
- can result in an incredibly large amount of data lacking small details
- original network protocols lack monitoring capabilities
- data useage measurements can be used to identify potential new customers, determine the most popular addresses and hosts, detecting network attacks, find rerouting paths, and billing
- passive monitoring only watches existing traffic and patterns
- flow records-saving the details of one conversation between hosts (length of time)
- 

### Cisco Netflow
- 

## What confused me

## Artifacts captured

## Lab 1
- Enabling sampling on both eth1 and eth2 in this case would simply result in receiving double the information about the same communications. The router is only covering the communication between these two hosts, so enabling both doesn't actually give new information.
- Before: 1992: eth1@if1991: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default 
    link/ether aa:c1:ab:af:23:11 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    RX:  bytes packets errors dropped  missed   mcast           
          5,042      33      0       0       0       0 
    TX:  bytes packets errors dropped carrier collsns           
          4,562      31      0       0       0       0 
    altname clab-o-614a11f28d7819b2

After: 1992: eth1@if1991: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default 
    link/ether aa:c1:ab:af:23:11 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    RX:   bytes  packets errors dropped  missed   mcast           
    83,835,137,612 55,654,194      0       0       0       0 
    TX:   bytes  packets errors dropped carrier collsns           
      223,473,096  3,385,226      0       0       0       0 
    altname clab-o-614a11f28d7819b2

Estimation:
Direction               Samples   Est. Packets     Est. Bytes
host2 -> host1             3,327      3,327,000    232,958,000
host1 -> host2            55,632     55,632,000 84,010,200,000

At 1-in-1000 sampling of 3,385,195 true packets:
Expected samples observed: 3385.2
Standard error of the estimate: ±58,182 packets (1.72% relative)
Approximate 95% confidence interval: 3,271,157 – 3,499,233 packets

True error: 58,195 (just above standard error)

At 1-in-1000 sampling of 55,654,161 true packets:
Expected samples observed: 55654.2
Standard error of the estimate: ±235,911 packets (0.42% relative)
Approximate 95% confidence interval: 55,191,775 – 56,116,547 packets

True error: 22,161 (far less than standard error)

- For the 1->2 communication, the error is fairly small, and much less than the standard error. For 2->1, the error is slightly larger than the standard error. We can expect that a larger number of total sent packets results in a smaller relative error, so this makes sense.
- A vast majority of the communication was 1->2, which makes sense given that is the direction most of the data went.
- No other types were recorded

1992: eth1@if1991: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default 
    link/ether aa:c1:ab:af:23:11 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    RX:   bytes  packets errors dropped  missed   mcast           
    84066960488 59,165,464      0       0       0       0 
    TX:   bytes  packets errors dropped carrier collsns           
    77963675451 54,993,368      0       0       0       0 
    altname clab-o-614a11f28d7819b2

1992: eth1@if1991: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default 
    link/ether aa:c1:ab:af:23:11 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    RX:    bytes   packets errors dropped  missed   mcast           
     84310792275  62,858,959      0       0       0       0 
    TX:    bytes   packets errors dropped carrier collsns           
    155556535464 106,503,542      0       0       0       0 
    altname clab-o-614a11f28d7819b2

Actual 1->2: 3,693,495
Actual 2->1: 51,510,174

Direction               Samples   Est. Packets     Est. Bytes
host2 -> host1           514,891     51,489,100 77,762,445,000
host1 -> host2            36,651      3,665,100    256,626,600

At 1-in-100 sampling of 51,510,174 true packets:
Expected samples observed: 515101.7
Standard error of the estimate: ±71,771 packets (0.14% relative)
Approximate 95% confidence interval: 51,369,504 – 51,650,844 packets

Actual error: 21,074 (less than standard)

At 1-in-100 sampling of 3,693,495 true packets:
Expected samples observed: 36934.9
Standard error of the estimate: ±19,218 packets (0.52% relative)
Approximate 95% confidence interval: 3,655,827 – 3,731,163 packets

Actual error: 28,395 (more than standard)

- About 10 times more samples were received for 1 in 100 sampling than 1 in 1,000, which makes sense. 
- The error for the ACK side greatly decreased, as expected with the higher ratio of samples. The error of the data side actually increased, but this is probably because the actual error in the 1 in 1,000 sampling was 10 times less than expected, so it is probably an outlier. A decrease in error is expected for both.
- There was no significant difference between the two directions, so sampling both directions is largely redundant here.

## Lab 2
SUM
43,400,007  65,100,000,537

SUM
2,372,987 123,400,376

2007: eth1@if2006: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default 
    link/ether aa:c1:ab:bc:c5:57 brd ff:ff:ff:ff:ff:ff link-netnsid 2
    RX:   bytes  packets errors dropped  missed   mcast           
    80,521,305,423 53,454,104      0       1       0       0 
    TX:   bytes  packets errors dropped carrier collsns           
      187,164,534  2,835,075      0       0       0       0 
    altname clab-o-614a11f28d7819b2

- The actual count is fairly close to the flow count, with 2.8 million vs 2.3 million packets transmitted and 53.4 million vs 43.4 million packets received. Some of this discrepancy may come because the values are printed as rounded rather than exact for the flow count.
- If you only looked at flows after they ended, you would miss issues with continuous connections. This could be something like a purposeful permanent link, or something like a DDoS attack, which you want to have information on. By exporting active flows, you can see this issues in connections that may not close for a long time, or ever.

Top 5     IP Addr ordered by bytes:
Date first seen             Duration     Proto           IP Addr    Flows(%)     Packets(%)       Bytes(%)         pps      bps   bpp
2026-07-01 15:28:38.388     00:00:00.059 any           10.5.1.10       82(93.2)   56.3 M(100.0)   79.9 G(100.0)   939780   10.7 G  1419
2026-07-01 15:28:38.388     00:00:00.059 any           10.5.2.10       82(93.2)   56.3 M(100.0)   79.9 G(100.0)   939780   10.7 G  1419
2026-07-01 15:29:29.977     00:00:00.840 any             ff02::2        6( 6.8)        6( 0.0)      336( 0.0)        0        3    56
2026-07-01 15:29:29.977     00:00:00.840 any    fe80::a..c1:2ca7        3( 3.4)        3( 0.0)      168( 0.0)        0        1    56
2026-07-01 15:29:34.069     00:00:00.737 any    fe80::a..bc:c557        3( 3.4)        3( 0.0)      168( 0.0)        0        1    56
Summary: total flows: 88, total bytes: 79.9 G, total packets: 56.3 M, avg bps: 716.7 M, avg pps: 63095, avg bpp: 1419
Time window: 2026-07-01 15:25:30.  0 - 2026-07-01 15:56:30.  0, Duration:    00:31:00.000
Total records processed: 88, passed: 88, Blocks skipped: 0, Bytes read: 17480
Sys: 0.0026s User: 0.0026s Wall: 0.0019s flows/second: 46709.5 Runtime: 0.0019s

- In this output, I can see the four sent F (FIN) flags meaning the connection was closed with TCP FIN.
- With many short-lived flows, rtr1 would be under no additional pressure in Lab 1's approach, but in Lab 2 it would be swamped. However, this also means in Lab 1 the collector would be struggling, whereas in Lab 2 the collector would be fine. This is because Lab 1's approach, SFLow, has very little overhead on the devices, and places it mostly on the collector instead. Lab 2's approach, NetFlow, requires tracking on the device end, and therefore is more involved for a large number of flows.



## Code Lab
- Going from 10 to 1000 sampling increases the error from 1% to 10%, exactly the predicted 10 times increase.
- Going from 1,000 to 1,000,000 packet count decreases the error from 31.62% to 1%. Having a higher true packet count results in a more true estimate because tje number of received packets is a more accurate reflection. With a small number of packets, sampling often will make traffic patterns appear more often than reality.
- The relative error here is 141%, which is quite high. At this polling rate and such small number of packets, packets appearing once will seem important, even if they only appear a few times in reality. Other packet types will be missed entirely.
- 