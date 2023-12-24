A python tool to check if various CSS selectors are active OR not found on a website.

Requires `beautifulsoup4` and `requests` python libraries.

- Arch: `pacman -S python-beautifulsoup4 python-requests`
- Debian: `apt install python3-bs4 python3-requests`
- Other: `pip install requests beautifulsoup4`

Run with: `python css-check.py --site https://example.com --css ".class,#id"`

Any CSS selectors you want to check must be separated by commas.
