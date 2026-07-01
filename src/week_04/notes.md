---
title: "Week 4 Notes"
toc: true
---

<div class="note">
You can place notes in this file in any mix of Markdown, HTML, CSS, and JavaScript.
</div>

# Week 4 — Notes

## What I learned

### Congestion Avoidance
- early internet experienced congestion collapse
- attempt to maintain a packet equilibrium on the network
- starting systems that only send when another packet is received can be hard, as it uses very little of the bandwidth because it only sends one at a time
- slow start- send 1 packet, and then increase number of packets sent for each ACK
- need a good estimation of round trip time that is able to capture variability to avoid unnecessary retransmissions
- use exponential timer backoff for multiple retransmissions of the same packet
- most packet loss is due to congestion
- congestion avoidance strategy must have a way for the network to tell endpoints about congestion, and a strategy at each endpoint to lower congestion
- use timeout to communicate network congestion
- use multiplicative decrease of window size at endpoint to lower congestion
- gateway protocols to drop excessive numbers of packets canuse endpoint protocols to balance out used bandwidth


## What confused me

## Artifacts captured


## Lab 1
- From 10ms to 100ms, the Mathis percentage drops from 4.5% to 0.5%. This is not exactly a 10x decrease, but it is close to it at 9 times. 
- From 0.1% loss to 1.0% loss, the Mathis percentage goes from 2.3% to 0.7%, which is approximately 3.2 times degredation. 
- From the 4.5% at 10ms/0.1%, we go down to 0.1% at 100ms/1.0%, which is a 45 times decrease. This is a bit more than the predicted 31 times decrease. Adding latency to an already lossy path clearly makes the communication far worse.


Results:
625
340	
138	
63.9

118	
59.2
28
14.8

These results are above the Mathis trendline. At each step, the throughput roughly halves for both lines. The 0.1% loss line is over 3 times the values of the 1.0% loss line.

CUBIC 0.00-30.01  sec  70.0 MBytes  19.6 Mbits/sec   90            sender
BBR 0.00-30.01  sec   558 MBytes   156 Mbits/sec  629            sender

Cubic is only slightly better than the 100ms/1.0%, which can be expected. BBR is significantly better, since it ignores loss.

## Lab 2
- The number of devices is 127, though there are only 97 when filtering just to up devices.
- 