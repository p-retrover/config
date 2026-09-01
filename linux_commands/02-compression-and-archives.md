# Compression and Archives

Go back to the [main readme](./README.md)

## `gzip`

`gzip` compresses individual files.

```bash
gzip <filename>
```

A typical result is:

```text
filename -> filename.gz
```

### Compression level

The notes describe levels from **1 to 9**:

```text
1 -> fastest, least compression
9 -> slowest, best compression
6 -> default
```

Example:

```bash
gzip -3 <filename>
```

### Verbose mode

```bash
gzip -v <filename>
```

`-v` displays information about the compression.

### Keep the original file

```bash
gzip -k <filename>
```

### Decompress

```bash
gzip -d <filename>.gz
```

Equivalent commonly used command:

```bash
gunzip <filename>.gz
```

## `tar`

`tar` creates and extracts archives. Unlike `gzip`, `tar` itself primarily **archives** files rather than compressing them.

Create an archive:

```bash
tar -cf archive.tar file1 file2
```

The notes also show the common compressed archive form:

```bash
tar -czf archive.tar.gz file1 file2
```

Extract an archive:

```bash
tar -xf archive.tar
```

Extract a gzip-compressed tar archive:

```bash
tar -xzf archive.tar.gz
```

### Useful `tar` options

| Option | Meaning |
|---|---|
| `-c` | create archive |
| `-x` | extract archive |
| `-f` | specify archive file |
| `-z` | gzip compression/decompression |
| `-v` | verbose output |

The handwritten notes specifically describe the pattern:

```bash
tar -czf <archive>.tar.gz <file1> <file2>
```

as creating a compressed archive, and `tar -x...` for extraction.
