# filter-checks
GitHub actions to help me maintain my content blocker filter lists.

Once a month it downloads the lists from my filter list repository and checks for potentially inactive domains with [nslookup](https://pypi.org/project/nslookup/).

It also checks for redirects. (Domain name changes.)

Any domains you see in the logs should be taken with a grain of salt. Sometimes the domains are just temporarily down, or a subdomain can still be in use.

## Usage

If you want to use this to check your own filter list or hosts file:

1. Fork this repository.
2. Change the `wget` lines in `.github/workflows/download-file.yml` to your filter list(s) and/or host(s) file(s).
3. Run the action manually, wait until the 1st of every month, or change the cron timers to your preference.

### Workflow usage in order

1. **Download File** (This will download the filter and/or hosts file you specified in `.github/workflows/download-file.yml`). *This is automatically set to run at 00:00 the 1st of every month.*
2. **Run Domain Check Script** (This will extract the domains from a valid filter file `lists/main.txt` and run the status check. The domains that are inactive will be located in `logs/inactive_domains.log`). *This is automatically set to run at 01:00 the 1st of every month.*
3. **Run Hosts Domain Check Script** (This will extract the domains from a valid hosts file `lists/main-hosts.txt` and run the status check. The domains that are inactive will be located in `logs/inactive_domains_hosts.log`). *This is automatically set to run at 02:00 the 1st of every month.*
4. **Check redirects** (This will check any domains that redirects to another one. Useful for finding out if a website has changed name/address. The logfile is in `logs/redirects.log`). *This is automatically set to run at 03:00 the 1st of every month.*
