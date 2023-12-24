import requests
from bs4 import BeautifulSoup
import argparse
import re

def check_css(url, css):
  # Send a GET request to the website
  response = requests.get(url)

  # Parse the HTML content of the page with BeautifulSoup
  soup = BeautifulSoup(response.content, 'html.parser')

  # Extract all link and style tags
  tags = soup.find_all(['link', 'style'])

  # List to store the CSS selectors that are found
  found_selectors = []

  # Check each tag for the presence of the CSS selectors
  for tag in tags:
    if tag.text:
      text = tag.text
      for selector in css:
        if selector in text:
          # Add the selector to the list of found selectors
          found_selectors.append(selector)

  # Print the found selectors
  for selector in found_selectors:
    print(f"Found CSS selector {selector}")

  # Print the selectors that were not found
  for selector in css:
    if selector not in found_selectors:
      print(f"CSS selector {selector} not found.")

  # Return whether any selectors were found
  return len(found_selectors) > 0

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--site", type=str, required=True)
  parser.add_argument("--css", type=str, required=True)
  args = parser.parse_args()

  css = args.css.split(',')
  check_css(args.site, css)
