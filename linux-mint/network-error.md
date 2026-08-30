# Linux Mint Dynamic DNS Fix

## Problem

Domain name resolution fails on certain networks like college Wi-Fi, while pinging IP addresses works. **systemd-resolved** hangs due to router handling of EDNS0 probes.

## Solution

Configure **NetworkManager** to directly update resolv.conf dynamically from network DHCP without hardcoding IP addresses.

1. Create override file:
   sudo nano /etc/NetworkManager/conf.d/00-default-dns.conf

2. Add lines:
   [main]
   dns=default
   rc-manager=file

3. Disable systemd-resolved and apply:
   sudo systemctl stop systemd-resolved
   sudo systemctl disable systemd-resolved
   sudo rm -f /etc/resolv.conf
   sudo touch /etc/resolv.conf
   sudo systemctl restart NetworkManager
   nmcli device disconnect wlp2s0 && nmcli device connect wlp2s0

4. Verify `/etc/resolv.conf` gets dynamically updated by NetworkManager.
