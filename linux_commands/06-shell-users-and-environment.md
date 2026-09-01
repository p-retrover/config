# Shell Utilities, Users, Networking, and Environment

Go back to the [main readme](./README.md)

## `type`

Determine how the shell interprets a command:

```bash
type <command>
```

It can identify whether a name refers to a shell builtin, alias, function, keyword, or external command.

The notes use `type` to investigate commands such as:

```bash
type ls
```

## `which`

Find the executable associated with a command name:

```bash
which <command>
```

Example:

```bash
which python
```

## `who`

Show users currently logged in:

```bash
who
```

The notes also show:

```bash
who am i
```

to identify the current login/session.

## `su`

Switch to another user:

```bash
su <username>
```

Switch to another user's login shell:

```bash
su - <username>
```

The `-` requests a login environment for the target user.

## `sudo`

Run a command with elevated privileges:

```bash
sudo <command>
```

Example:

```bash
sudo <command>
```

The notes explain that `sudo` may ask for the current user's password and that the user must be authorized to use `sudo`.

## `passwd`

Change a user's password:

```bash
passwd
```

Change another user's password when permitted:

```bash
sudo passwd <username>
```

The notes also mention that the root user can change another user's password.

## `ping`

Test network reachability using ICMP:

```bash
ping <host>
```

Example:

```bash
ping google.com
```

The notes describe ICMP as a network-layer protocol used for control/error messaging and commonly used by `ping`.

## `traceroute`

Show the network path toward a destination:

```bash
traceroute <host>
```

Example:

```bash
traceroute google.com
```

The notes also show a limited-hop example:

```bash
traceroute -m 1 <host>
```

where `-m` controls the maximum number of hops.

## `clear`

Clear the terminal screen:

```bash
clear
```

The notes distinguish this from merely removing terminal history: clearing the screen does not erase shell history.

## `history`

Show previously executed shell commands:

```bash
history
```

Search the history:

```bash
history | grep "<pattern>"
```

The notes describe `history` as displaying commands stored in the shell history.

## `env`

Display environment variables:

```bash
env
```

Environment variables can be passed to programs launched from the shell.

## `uname`

Display system information:

```bash
uname
```

Useful options:

```bash
uname -a
```

Show a broad set of system information.

The notes mention information such as:

- OS/kernel name
- kernel release/version
- machine architecture
- processor information
- hardware/platform information

## `export`

Export a shell variable so it is available to child processes.

Set and export:

```bash
export TEST="test"
```

Check it:

```bash
echo "$TEST"
```

A child process can then access `TEST`.

### Why `export` matters

A normal shell variable is available in the current shell:

```bash
TEST="test"
```

Exporting it makes it part of the environment inherited by commands/programs started by that shell:

```bash
export TEST="test"
```

### Appending to a variable

The notes use `PATH` as an example:

```bash
export PATH="$PATH:/new/path"
```

This preserves the existing `PATH` and appends another directory.

### Remove an exported variable

```bash
export -n TEST
```

This removes the export attribute from the variable in shells supporting `export -n`; it does not necessarily unset the variable itself.

To unset the variable entirely:

```bash
unset TEST
```

> The handwritten notes specifically show `export -n TEST` for removing the export attribute.

### Export with no arguments

```bash
export
```

In common shells, this displays the exported variables.
