import sys
import requests
import getopt
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def check_css_selectors(url, selectors):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  not_found_selectors = []

  selectors = selectors.split(',') # Split the css string into a list of selectors

  for selector in selectors:
    if selector.startswith('['): # Check if the selector is an attribute selector
      tag, attr = selector.split('[')[0], selector.split('[')[1].replace(']', '')
      attr_parts = attr.split('*')
      if len(attr_parts) == 2: # Handle * selector
        elements = soup.find_all(tag, attrs={attr_parts[0]: lambda x: x and attr_parts[1] in x})
      elif len(attr_parts) == 3: # Handle ^ and $ selectors
        start, end = attr_parts[0], attr_parts[2]
        elements = soup.find_all(tag, attrs={attr_parts[0]: lambda x: x and (x.startswith(start) if end == '$' else x.endswith(end))})
    else:
      elements = soup.find_all(selector)
      
    if not elements:
      not_found_selectors.append(selector)

  # Check CSS files
  css_links = soup.find_all('link', {'rel': 'stylesheet'})
  for link in css_links:
    css_url = link.get('href')
    if not css_url.startswith('https'):
      css_url = urljoin(url, css_url)
      css_response = requests.get(css_url)
      css_content = css_response.text
    for selector in selectors:
      if selector in css_content:
        not_found_selectors.remove(selector)

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
      css = arg # Pass css as a single string

  if site and css:
    check_css_selectors(site, css)
  else:
    print('Missing arguments')
    sys.exit(2)

if __name__ == "__main__":
  main()
