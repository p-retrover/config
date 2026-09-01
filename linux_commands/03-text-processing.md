# Text Processing and Comparison

Go back to the [main readme](./README.md)

## `alias`

Create a shell shortcut.

```bash
alias <name>='<command>'
```

Example from the notes:

```bash
alias l="ls -al"
```

The alias can then be used as:

```bash
l
```

Remove an alias:

```bash
unalias <name>
```

> Shell aliases normally affect the current shell session unless placed in a shell startup file.

## `cat`

Print a file:

```bash
cat <file>
```

Concatenate multiple files:

```bash
cat <file1> <file2>
```

Redirect/append output:

```bash
cat <file1> <file2> > <file>
cat <file1> <file2> >> <file>
```

Display line numbers:

```bash
cat -n <file>
```

The notes also show piping `cat` output into another command:

```bash
cat <file> | <command>
```

## `less`

View a file interactively:

```bash
less <filename>
```

Useful for files too large to comfortably print all at once.

## `tail`

Show the end of a file:

```bash
tail <file>
```

Follow a file as it changes:

```bash
tail -f <file>
```

The notes give log files as the example use case:

```bash
tail -f /var/log/system.log
```

The exact log filename varies by Linux distribution.

## `grep`

Search for matching text:

```bash
grep "<pattern>" <file>
```

A common recursive form is:

```bash
grep -r "<pattern>" <directory>
```

Useful options include:

```bash
grep -i "<pattern>" <file>   # case-insensitive
grep -n "<pattern>" <file>   # show line numbers
grep -r "<pattern>" <dir>    # recursive search
```

## `sort`

Sort lines in a file:

```bash
sort <file>
```

Reverse the order:

```bash
sort -r <file>
```

Remove duplicate lines:

```bash
sort -u <file>
```

The notes associate `-u` with removing duplicate lines.

## `diff`

Compare files line by line:

```bash
diff <file1> <file2>
```

Common options:

```bash
diff -y <file1> <file2>
```

Side-by-side comparison.

```bash
diff -u <file1> <file2>
```

Unified diff format.

The notes also mention comparing directories; `diff` can recursively compare directory contents with:

```bash
diff -r <directory1> <directory2>
```
