These are log files created by GitHub Actions.

<table>
  <tr align="left">
    <th>Log</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>domains.txt</td>
    <td>All the domains included in the specified filter list</td>
  </tr>
  <tr>
    <td>inactive_domains.log</td>
    <td>If a DNS resolver couldn't be found from any of the domains in <i>domains.txt</i> then it will be logged in this file. It should be noted that it's possible that some of these domains are still in use. It does not check for sub-domains. The websites also could've been temporarily down while the script was running.</td>
  </tr>
  <tr>
    <td>inactive_domains_hosts.log</td>
    <td>The same as above, but just for the hosts file <a href="https://github.com/lassekongo83/filter-checks/blob/main/lists/main-hosts.txt">lists/main-hosts.txt</a></td>
  </tr>
  <tr>
    <td>redirects.log</td>
    <td>Checks the main filter list for domains that redirects to other domains. Useful when you need to know if a larger website has changed name etc.</a></td>
  </tr>
</table>
