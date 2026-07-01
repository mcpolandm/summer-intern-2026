import os
import requests

LIBRENMS_URL = os.environ["LIBRENMS_URL"]
API_KEY = os.environ["LIBRENMS_API_KEY"]
HEADERS = {"X-Auth-Token": API_KEY}

resp = requests.get(
    f"{LIBRENMS_URL}/api/v0/devices",
    headers=HEADERS,
    params={"type": "up", "columns": "device_id,hostname,sysName,os,uptime"},
    timeout=30,
)
resp.raise_for_status()
devices = resp.json()["devices"]
up_device_ids = {int(d["device_id"]) for d in devices}

print(f"{len(devices)} devices currently up")
for d in devices[:10]:
    print(f"  {d['hostname']:30s} {d.get('os', '?'):10s} uptime={d.get('uptime')}")

resp = requests.get(
    f"{LIBRENMS_URL}/api/v0/ports",
    headers=HEADERS,
    params={"columns": "device_id,ifName,ifSpeed,ifOperStatus,ifInOctets_rate,ifOutOctets_rate"},
    timeout=30,
)
resp.raise_for_status()
ports = resp.json()["ports"]
print(f"{len(ports)} ports total")

ports = [p for p in ports if int(p["device_id"]) in up_device_ids]
print(f"{len(ports)} ports on devices that are actually up")

# Not every field is directly useful as-is — utilization is a simple example
# of turning two raw counters into something meaningful: bits/sec as a
# fraction of link speed.
up_ports = [p for p in ports if p.get("ifOperStatus") == "up" and (p.get("ifSpeed") or 0) > 0]
busiest = max(
    up_ports,
    key=lambda p: max(p.get("ifInOctets_rate") or 0, p.get("ifOutOctets_rate") or 0) * 8 / p["ifSpeed"],
)
util = max(busiest.get("ifInOctets_rate") or 0, busiest.get("ifOutOctets_rate") or 0) * 8 / busiest["ifSpeed"]
print(f"Busiest port seen: device {busiest['device_id']} / {busiest['ifName']} at {util:.1%} of {busiest['ifSpeed']:,} bps")

# Devices that are not currently up
resp = requests.get(
    f"{LIBRENMS_URL}/api/v0/devices",
    headers=HEADERS,
    params={
        "type": "down",
        "columns": "hostname,ip,status,status_reason,last_polled,uptime",
    },
    timeout=30,
)
resp.raise_for_status()
down_devices = resp.json()["devices"]

print(f"\n{len(down_devices)} devices not currently up:")
print(f"  {'Name':<30s} {'IP':<18s} {'Status':<8s} {'Last Polled':<22s}")
print(f"  {'-'*30} {'-'*18} {'-'*8} {'-'*22}")
for d in down_devices:
    status_str = "down" if d.get("status") == 0 else str(d.get("status"))
    print(
        f"  {d.get('hostname', '?'):<30s}"
        f" {d.get('ip', '?'):<18s}"
        f" {status_str:<8s}"
        f" {d.get('last_polled', '?'):<22s}"
    )