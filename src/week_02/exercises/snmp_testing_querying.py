import re
import pandas as pd
import subprocess
import sys
import time



def add_column_from_command(shell_command, regex, ip_address):
    output = subprocess.run(["snmpwalk", "-v2c", "-c", "readonly", ip_address, f"IF-MIB::{shell_command}"], capture_output=True, text=True).stdout
    temp = []
    for line in output.strip().split("\n"):
        match = re.match(regex, line.strip())
        if match:
            temp.append(match.group(1))
    
    return temp

def main(arg1):
    ip_address = arg1

    regex_descr = r"IF-MIB::ifDescr\.([0-9]*) = STRING: ([A-Za-z0-9]*)"
    regex_oper_status = r"IF-MIB::ifOperStatus\.[0-9]* = INTEGER: ([\(\)A-Za-z0-9]*)"
    regex_type = r"IF-MIB::ifType\.[0-9]* = INTEGER: ([\(\)A-Za-z0-9]*)"
    regex_mtu = r"IF-MIB::ifMtu\.[0-9]* = INTEGER: ([0-9]*)"
    regex_speed = r"IF-MIB::ifSpeed\.[0-9]* = Gauge32: ([0-9]*)"
    regex_addr = r"IF-MIB::ifPhysAddress\.[0-9]* = STRING: ([:a-z0-9]*)"
    regex_admin = r"IF-MIB::ifAdminStatus\.[0-9]* = INTEGER: ([\(\)A-Za-z0-9]*)"
    regex_change = r"IF-MIB::ifLastChange\.[0-9]* = Timeticks: \([0-9]*\) ([:\.0-9]*)"
    regex_octets_i = r"IF-MIB::ifInOctets\.[0-9]* = Counter32: ([0-9]*)"
    regex_ucast_i = r"IF-MIB::ifInUcastPkts\.[0-9]* = Counter32: ([0-9]*)"
    regex_discard_i = r"IF-MIB::ifInDiscards\.[0-9]* = Counter32: ([0-9]*)"
    regex_error_i = r"IF-MIB::ifInErrors\.[0-9]* = Counter32: ([0-9]*)"
    regex_unknown_i = r"IF-MIB::ifInUnknownProtos\.[0-9]* = Counter32: ([0-9]*)"
    regex_octets_o = r"IF-MIB::ifOutOctets\.[0-9]* = Counter32: ([0-9]*)"
    regex_ucast_o = r"IF-MIB::ifOutUcastPkts\.[0-9]* = Counter32: ([0-9]*)"
    regex_discard_o = r"IF-MIB::ifOutDiscards\.[0-9]* = Counter32: ([0-9]*)"
    regex_error_o = r"IF-MIB::ifOutErrors\.[0-9]* = Counter32: ([0-9]*)"
    regex_queue = r"IF-MIB::ifOutQLen\.[0-9]* = Gauge32: ([0-9]*)"
    regex_specific = r"IF-MIB::ifSpecific\.[0-9]* = OID: ([A-Za-z0-9:\-]*)"

    output_descr = subprocess.run(['snmpwalk', '-v2c', '-c', 'readonly', ip_address, 'IF-MIB::ifDescr'], capture_output=True, text=True).stdout
    data = []

    for line in output_descr.strip().split("\n"):
        match = re.match(regex_descr, line.strip())
        if match:
            data.append({
                "Index": match.group(1),
                "Interface": match.group(2)
            })

    df = pd.DataFrame(data)

    df['Operating Status'] = add_column_from_command("ifOperStatus", regex_oper_status, ip_address)
    df['Interface Type'] = add_column_from_command("ifType", regex_type, ip_address)
    df['Max Packet Size'] = add_column_from_command("ifMtu", regex_mtu, ip_address)
    df['Curr Bandwidth'] = add_column_from_command("ifSpeed", regex_speed, ip_address)
    df['Physical Address'] = add_column_from_command("ifPhysAddress", regex_addr, ip_address)
    df['Desired State'] = add_column_from_command("ifAdminStatus", regex_admin, ip_address)
    df['Time Last Change'] = add_column_from_command("ifLastChange", regex_change, ip_address)
    df['Octets Received In'] = add_column_from_command("ifInOctets", regex_octets_i, ip_address)
    df['Unicast Packets In'] = add_column_from_command("ifInUcastPkts", regex_ucast_i, ip_address)
    df['Discarded Packets In'] = add_column_from_command("ifInDiscards", regex_discard_i, ip_address)
    df['Error Packets In'] = add_column_from_command("ifInErrors", regex_error_i, ip_address)
    df['Unknown Packets In'] = add_column_from_command("ifInUnknownProtos", regex_unknown_i, ip_address)
    df['Octets Received Out'] = add_column_from_command("ifOutOctets", regex_octets_o, ip_address)
    df['Unicast Packets Out'] = add_column_from_command("ifOutUcastPkts", regex_ucast_o, ip_address)
    df['Discarded Packets Out'] = add_column_from_command("ifOutDiscards", regex_discard_o, ip_address)
    df['Error Packets Out'] = add_column_from_command("ifOutErrors", regex_error_o, ip_address)
    df['Output Queue Length'] = add_column_from_command("ifOutQLen", regex_queue, ip_address)
    df['MIB Definitions'] = add_column_from_command("ifSpecific", regex_specific, ip_address)


    print(df)
    df.to_csv(f"snmp_data.csv", index=False) 


if __name__ == "__main__":

    if len(sys.argv) > 1:
        main(sys.argv[1])