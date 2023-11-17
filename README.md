# filter-checks
GitHub actions to help me maintain my content blocker filter lists.

Once a month it downloads the lists from my filter list repository and checks for potentially inactive domains with [nslookup](https://pypi.org/project/nslookup/).

It also checks for redirects. (Domain name changes.)

Any domains you see in the logs should be taken with a grain of salt. Sometimes the domains are just temporarily down, or a subdomain can still be in use.
