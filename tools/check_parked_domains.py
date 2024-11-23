import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

# Read the domains from the text file
with open('logs/domains.txt', 'r') as file:
    domains = file.read().splitlines()

# Open the log file
log_file = open('logs/parked_domains.log', 'w')

def check_domain(domain):
    try:
        # Check MX records first
        mx_records = subprocess.check_output(['nslookup', '-q=mx', domain]).decode().strip()
        if not mx_records:
            # If no MX records, check A records
            a_records = subprocess.check_output(['nslookup', '-q=a', domain]).decode().strip()
            if not a_records:
                log_file.write(f'{domain}\n')  # Domain has no active DNS records
            else:
                print(f"{domain} has A records but no MX records")
        else:
            print(f"{domain} has MX records")
    except subprocess.CalledProcessError:
        log_file.write(f'{domain}\n')

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=100) as executor:
    # Use the executor to map the function to the domains
    executor.map(check_domain, domains)

# Close the log file
log_file.close()
