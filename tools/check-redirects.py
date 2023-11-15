import requests
import logging
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

# Set up the logger
logging.basicConfig(filename='logs/redirects.log', level=logging.INFO, filemode='w')

# Read the domains from the file
with open('logs/domains.txt', 'r') as file:
   domains = file.readlines()

# Function to check for redirects
def check_redirect(domain):
 url = domain.strip()
 if not url.startswith('http://') and not url.startswith('https://'):
  url = 'http://' + url
 try:
  response = requests.get(url, timeout=20)
  if response.url != url:
      # Parse the URLs and compare the domain names
      initial_domain = urlparse(url).netloc
      final_domain = urlparse(response.url).netloc
      # Check if the domain names are different and if the final domain is not the same as the initial domain (ignoring www)
      if initial_domain != final_domain and not final_domain.startswith(f'www.{initial_domain}') and not final_domain.endswith(':443/'):
          logging.info(f"{url} redirects to {response.url}")
 except requests.exceptions.Timeout:
  logging.info(f"{url} did not respond within the timeout period")

# Use ThreadPoolExecutor to run the function in parallel
with ThreadPoolExecutor(max_workers=100) as executor:
 executor.map(check_redirect, domains)
