# Requires: beautifulsoup4

import sys
import requests
import getopt
from bs4 import BeautifulSoup

def check_css_selectors(url, selectors):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  not_found_selectors = []

  for selector in selectors:
    if selector and not soup.select(selector):
      not_found_selectors.append(selector)

  if not_found_selectors:
    print('Selectors NOT found in the website:')
    for selector in not_found_selectors:
      print(f'{selector}')

def main():
  try:
    opts, _ = getopt.getopt(sys.argv[1:], '', ['site=', 'css='])
  except getopt.GetoptError:
    print('Invalid argument')
    sys.exit(2)

  site = None
  css = None
  for opt, arg in opts:
    if opt == '--site':
      site = arg
    elif opt == '--css':
      css = arg.split(',')

  if site and css:
    check_css_selectors(site, css)
  else:
    print('Missing arguments')
    sys.exit(2)

if __name__ == "__main__":
  main()

# Run with: python css-check.py --site https://example.com --css .class1,#id1,div[class="class2"],[class*="class3"]
