import re
import pandas as pd
import subprocess

regex = r"IF-MIB::ifDescr\.([0-9]*) = STRING: ([A-Za-z0-9]*)"

output = subprocess.run(['snmpwalk', '-v2c', '-c', 'readonly', '10.250.38.43', 'IF-MIB::ifDescr'], capture_output=True, text=True).stdout

data = []

for line in output.strip().split("\n"):
    print(line)
    match = re.match(regex, line.strip())
    if match:
        data.append({
            "Index": match.group(1),
            "Interface": match.group(2)
        })

df = pd.DataFrame(data)
print(df)