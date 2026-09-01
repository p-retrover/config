# Linux Commands

A cleaned-up version of the handwritten Linux command sheet.

The notes cover:

- File and directory operations
- Searching with `find`
- Compression and archives
- Text processing and comparison
- Ownership and permissions
- Disk usage
- Processes and signals
- Jobs, foreground/background execution
- `type`, `which`, `sudo`, `su`, and `passwd`
- Networking diagnostics
- Terminal/history/environment variables
- `export`
- `crontab`

> **Notation:** `<...>` means replace it with your own value. `[ ... ]` means an optional argument.

## Files

| File | Topics |
|---|---|
| [`01-files-and-search.md`](./01-files-and-search.md) | Files, directories, `find`, `exec` |
| [`02-compression-and-archives.md`](./02-compression-and-archives.md) | `gzip`, `gunzip`, `tar` |
| [`03-text-processing.md`](./03-text-processing.md) | `alias`, `cat`, `less`, `tail`, `grep`, `sort`, `diff` |
| [`04-permissions-and-disk.md`](./04-permissions-and-disk.md) | `chown`, `chmod`, symbolic/numeric permissions, `du`, `df` |
| [`05-processes-and-jobs.md`](./05-processes-and-jobs.md) | `ps`, `top`, `kill`, jobs, `fg`, `bg`, `nohup` |
| [`06-shell-users-and-environment.md`](./06-shell-users-and-environment.md) | `which`, `who`, `su`, `sudo`, `passwd`, `ping`, `traceroute`, `clear`, `history`, `env`, `uname`, `export` |
| [`07-cron.md`](./07-cron.md) | `crontab` and cron scheduling |

## Quick reference

```text
mkdir       create directory
rm          remove files/directories
find        search for files/directories
gzip        compress
gunzip      decompress gzip files
tar         create/extract archives
cat         print/concatenate files
less        view text interactively
tail -f     follow a growing file
grep        search text
sort        sort lines
diff        compare files
chown       change owner/group
chmod       change permissions
du          directory/file disk usage
df          filesystem disk usage
ps          process snapshot
top         live process/system view
kill        send a signal to a process
jobs        list shell jobs
fg/bg       foreground/background a job
nohup       keep a command running after logout
which       locate a command
who         show logged-in users
su          switch user
sudo        run a command with elevated privileges
passwd      change a password
ping        test network reachability
traceroute  inspect network path
history     shell command history
env         environment variables
export      export shell variables
crontab     schedule recurring jobs
```
