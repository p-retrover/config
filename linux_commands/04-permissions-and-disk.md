# Ownership, Permissions, and Disk Usage

Go back to the [main readme](./README.md)

## `chown`

Change the owner of a file:

```bash
chown <owner> <file>
```

Change owner and group:

```bash
chown <owner>:<group> <file>
```

Apply recursively to a directory and its contents:

```bash
chown -R <owner>:<group> <directory>
```

> The notes emphasize recursive ownership changes for all files and folders within a directory.

## `chmod`

Change file permissions:

```bash
chmod <permissions> <file>
```

A permission string can be understood as:

```text
          owner   group   others
             |      |       |
             v      v       v
          rwx      rwx     rwx
```

For example:

```text
-rwxr-xr-x
```

The first character represents the file type; the remaining permission bits are grouped into owner, group, and others.

### Symbolic permissions

The notes use:

```text
u -> user/owner
g -> group
o -> others
a -> all
```

Operators:

```text
+ -> add permission
- -> remove permission
= -> set permission
```

Permission letters:

```text
r -> read
w -> write
x -> execute
```

Examples:

```bash
chmod u+x <file>
chmod g-w <file>
chmod o-r <file>
chmod a+r <file>
```

The notes also demonstrate setting multiple permissions:

```bash
chmod u=rwx,g=rx,o=rx <file>
```

### Numeric permissions

The notes use the standard numeric values:

```text
r = 4
w = 2
x = 1
```

Therefore:

```text
rwx = 7
rw- = 6
r-x = 5
r-- = 4
-wx = 3
-w- = 2
--x = 1
--- = 0
```

Example:

```bash
chmod 755 <file>
```

means:

```text
owner  = rwx = 7
group  = r-x = 5
others = r-x = 5
```

Another common example:

```bash
chmod 777 <file>
```

gives read/write/execute permission to owner, group, and others.

> Avoid `777` unless you specifically need those permissions; it grants write access broadly.

## `du`

Calculate disk usage of files/directories.

```bash
du <directory>
```

Human-readable form:

```bash
du -h <directory>
```

The notes describe `-h` as human-readable output.

A useful summary form:

```bash
du -sh <directory>
```

Sort directory usage and inspect the largest entries:

```bash
du -h <directory> | sort -h
```

The notes also show the idea of sorting disk usage and taking the first/last entries to inspect large or small items.

## `df`

Show filesystem disk-space usage:

```bash
df
```

Human-readable:

```bash
df -h
```

The notes distinguish:

- `du` -> usage of files/directories
- `df` -> free/used space of mounted filesystems
