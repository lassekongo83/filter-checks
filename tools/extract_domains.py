import os
import re

INPUT_FILE = 'lists/main.txt'
OUTPUT = 'logs/domains.txt'

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

with open(OUTPUT, 'r') as f:
  lines = f.readlines()
  lines = sorted(set(lines), key=lines.index)
  lines = sorted(lines)
with open(OUTPUT, 'w') as f:
  for line in lines:
    if ',' not in line and '|' not in line:
      f.write(line)
