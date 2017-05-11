# Check Backup Age for Nagios/Icinga

If you're using rsnapshot, this script will check when the last snapshot was taken. Using nothing but plain Python3.

# Usage

This script takes as input a file containing list of dates, as you would get from *ls --full-time*. It extracts the dates and compares them to today's date.

The format of the dates and the regex to extract the dates can be adjusted.

Date Format: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
Regex Format: https://docs.python.org/3.5/library/re.html

# Examples

Example for OK
```bash
./check_backup_age.py -p examples/offline-backup-list.ok
OK - Last backup was 0 days ago
```

Example for Critical
```bash
./check_backup_age.py -p examples/offline-backup-list.crit
CRIT - Last backup was 7 days ago
```
