import socket
import logging
import whois
import http.client
from concurrent.futures import ThreadPoolExecutor

# Create separate logger objects for each log file
dns_logger = logging.getLogger('dns')
whois_logger = logging.getLogger('whois')
http_logger = logging.getLogger('http')

# Configure each logger object to write to a different log file
dns_handler = logging.FileHandler('logs/dns/inactive.log')
whois_handler = logging.FileHandler('logs/whois/inactive.log')
http_handler = logging.FileHandler('logs/httpstatus/logfile.log')

dns_logger.addHandler(dns_handler)
whois_logger.addHandler(whois_handler)
http_logger.addHandler(http_handler)

# Function to perform DNS lookup
def is_domain_active(domain):
 try:
    socket.gethostbyname(domain)
    return True
 except socket.gaierror:
    dns_logger.info(f"{domain} is inactive")
    return False

# Function to perform WHOIS lookup
def get_whois_info(domain):
 try:
    return whois.whois(domain)
 except Exception as e:
    whois_logger.info(f"Error getting WHOIS info for {domain}: {e}")
    return None

# Function to perform HTTP status code check
def get_http_status(domain):
 try:
    conn = http.client.HTTPConnection(domain)
    conn.request("GET", "/")
    r1 = conn.getresponse()
    return r1.status, r1.reason
 except Exception as e:
    http_logger.info(f"Error getting HTTP status for {domain}: {e}")
    return None, None

# Read the file containing the domains
with open('logs/domains.txt', 'r') as file:
  domains = [line.strip() for line in file]

# Perform DNS lookups in parallel
with ThreadPoolExecutor(max_workers=100) as executor:
  results = executor.map(is_domain_active, domains)

# Process the results
for domain, is_active in zip(domains, results):
 if not is_active:
     dns_logger.info(f"{domain} is inactive")
 else:
     whois_info = get_whois_info(domain)
     http_status, http_reason = get_http_status(domain)
     if whois_info is not None:
         whois_logger.info(f"WHOIS info for {domain}: {whois_info}")
     if http_status is not None:
         http_logger.info(f"HTTP status for {domain}: {http_status} {http_reason}")
