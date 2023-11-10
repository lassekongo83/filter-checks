import subprocess
import os

# Read the domains from the text file
with open('logs/domains.txt', 'r') as file:
  domains = file.read().splitlines()

# Open the log file
log_file = open('logs/inactive_domains.log', 'w')

# Check the DNS records of each domain and log the inactive ones
for domain in domains:
  try:
      result = subprocess.check_output(['nslookup', '-q=mx', domain])
  except subprocess.CalledProcessError:
      log_file.write(f'{domain}\n')

# Close the log file
log_file.close()
