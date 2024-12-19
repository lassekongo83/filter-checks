# filter-checks
GitHub actions to help me maintain my content blocker filter lists.

Once a month it downloads the lists from my filter list repository and checks for potentially inactive domains with [nslookup](https://pypi.org/project/nslookup/).

It also checks for redirects. (Domain name changes.)

Any domains you see in the logs should be taken with a grain of salt. Sometimes the domains are just temporarily down, or a subdomain can still be in use.

## Usage

If you want to use this to check your own filter list or hosts file:

1. Fork this repository.
2. Change the `wget` lines in `.github/workflows/download-file.yml` to your filter list(s) and/or host(s) file(s).
3. Run the action manually, wait until the 1st of every month, or change the cron timer to your preference.
