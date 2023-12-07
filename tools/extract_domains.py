import os
import re
from collections import OrderedDict

INPUT_FILE = '../lists/main.txt'
OUTPUT = 'domains.txt'

with open(INPUT_FILE, 'r') as f:
 lines = f.readlines()

cosmetic_filters = [re.sub(r'#.*', '', line) for line in lines if '##' in line]
domain_specific = [re.sub(r'.*domain=', '', line) for line in lines if 'domain=' in line]
domain_from_filters = [match[0][1] for line in lines if ('||' in line or '@@||' in line) for match in [re.findall(r'^(@@\|\||\|\|)(.*?)(\^|/)', line)] if match]

lines = cosmetic_filters + domain_specific + domain_from_filters
lines = [line.strip() for line in lines if line.strip()]
lines = [line for line in lines if not any(c in line for c in '*')]
lines = [line.replace('~', '') for line in lines]
lines = [line for line in lines if line.endswith(tuple('abcdefghijklmnopqrstuvwxyz'))] # Remove lines that end with any character other than a-z
lines = sorted(set(lines), key=lines.index)
lines = sorted(lines)

# Remove duplicates and preserve order
lines = list(OrderedDict.fromkeys(lines))

# Track domains that have already been written to the file
written_domains = set()

with open(OUTPUT, 'w') as f:
  for line in lines:
    # Split the line by comma and pipe
    domains = line.split('|')
    for domain in domains:
      # Split the domain by comma
      domain_parts = domain.split(',')
      for domain_part in domain_parts:
        # Only write the domain to the file if it hasn't been written yet
        if domain_part.strip() not in written_domains:
          f.write(domain_part.strip() + '\n')
          written_domains.add(domain_part.strip())
