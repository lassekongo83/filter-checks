# Requires: pip install requests beautifulsoup4

import sys
import requests
from bs4 import BeautifulSoup

def check_css_selectors(url, selectors):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  for selector in selectors:
    if soup.select(selector):
      print(f'Selector "{selector}" found in the website.')
    else:
      print(f'Selector "{selector}" not found in the website.')

if __name__ == "__main__":
  url = sys.argv[1]
  selectors = sys.argv[2].split(',')
  check_css_selectors(url, selectors)

# Run with: python css-check.py site=https://example.com css=.class1,#id1,div[class=class2],[class*=class3]
