A python tool to check if various CSS selectors from a specified website are found or not.

Requires `beautifulsoup4` and `requests` python libraries.

- Arch: `pacman -S python-beautifulsoup4 python-requests`
- Debian: `apt install python3-bs4 python3-requests`
- Other: `pip install requests beautifulsoup4`

Run with: `python css-check.py --site https://www.google.se --css ".g,.gb4,#gbar,.example-class"`

It currently checks for just classes and IDs. Any CSS selectors you want to check must be separated by commas.

`extract-selectors.py` is a tool that extracts all the CSS selectors *(just a rough estimation)* from your specified filter list to the following output: `--site https://example.se --css ".ad,.ads,#cookies"`
