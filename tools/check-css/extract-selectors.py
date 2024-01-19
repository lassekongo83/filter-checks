import re
from collections import OrderedDict

with open('./lists/main.txt', 'r') as f:
  lines = f.readlines()

output_lines = OrderedDict()

for line in lines:
  parts = line.split("##")
  if len(parts) > 1:
    css_selectors = parts[1].strip()
    selectors = []
    for selector in re.split(",| ", css_selectors): # Split selectors based on both commas and spaces
      if '[' not in selector and '>' not in selector and '+' not in selector and '~' not in selector and ':' not in selector and '(' not in selector and ')' not in selector and (selector.startswith('.') or selector.startswith('#')):
        selectors.append(selector.strip())
    if selectors: # Check if selectors list is not empty
      domain_parts = parts[0].strip().split(',')
      domain = domain_parts[0]
      if domain: # Check if domain is not empty
        domain = 'https://' + domain
        if domain in output_lines:
          output_lines[domain].extend(selectors) # Add selectors to existing domain
        else:
          output_lines[domain] = selectors # Create new domain with selectors

# Open the output file in write mode
with open('./logs/selectors.txt', 'w') as f:
  for domain, selectors in output_lines.items():
    output_line = f'--site {domain} --css "{",".join(selectors)}"\n'
    f.write(output_line)
