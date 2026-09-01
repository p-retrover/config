# Files, Directories, and Search

Go back to the [main readme](./README.md)

## `mkdir`

Create directories.

```bash
mkdir <directory>
```

Create a directory hierarchy with parent directories as needed:

```bash
mkdir -p <parent>/<child>/<directory>
```

## `rm`

Remove files.

```bash
rm <file>
```

Remove a directory recursively:

```bash
rm -r <directory>
```

Force removal:

```bash
rm -f <file>
```

Common combination:

```bash
rm -rf <directory>
```

> `rm -rf` is destructive. Double-check the path before running it.

## `find`

Search for files/directories recursively.

Basic form:

```bash
find <path> <expression>
```

Search by name:

```bash
find . -name "*.js"
```

The notes also show case-insensitive name matching:

```bash
find . -iname "<name>"
```

### Search by type

For example, search for directories:

```bash
find . -type d -name "<name>"
```

Common `-type` values:

| Type | Meaning |
|---|---|
| `f` | regular file |
| `d` | directory |
| `l` | symbolic link |

### Search under multiple root paths

You can provide more than one starting path:

```bash
find <path1> <path2> -name "<pattern>"
```

### Execute a command for every match

The notes use `-exec` to run a command on each result:

```bash
find . -type f -exec <command> {} \;
```

Here `{}` is replaced by the current matching path.

The notes emphasize that `-exec` can be used to perform an operation on each search result, such as applying a command to every matching file.
