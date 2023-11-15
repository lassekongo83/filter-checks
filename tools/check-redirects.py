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
 response = requests.get(url)
 if response.url != url:
  # Parse the URLs and compare the domain names
  initial_domain = urlparse(url).netloc
  final_domain = urlparse(response.url).netloc
  if initial_domain != final_domain:
      logging.info(f"{url} redirects to {response.url}")

# Use ThreadPoolExecutor to run the function in parallel
with ThreadPoolExecutor(max_workers=100) as executor:
 executor.map(check_redirect, domains)
