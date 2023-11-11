import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

# Read the domains from the text file
with open('logs/domains.txt', 'r') as file:
 domains = file.read().splitlines()

# Open the log file
log_file = open('logs/inactive_domains.log', 'w')

# Function to check the DNS records of a domain
def check_domain(domain):
 try:
     subprocess.check_output(['nslookup', '-q=mx', domain])
 except subprocess.CalledProcessError:
     log_file.write(f'{domain}\n')

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=100) as executor:
 # Use the executor to map the function to the domains
 executor.map(check_domain, domains)

# Close the log file
log_file.close()
