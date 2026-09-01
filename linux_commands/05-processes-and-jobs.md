# Processes, Signals, and Jobs

Go back to the [main readme](./README.md)

## `ps`

List processes.

```bash
ps
```

The notes describe `ps` as showing processes associated with the current shell.

Show processes for all users:

```bash
ps aux
```

A common alternative form:

```bash
ps -ef
```

Useful idea from the notes:

- `ps` gives a process snapshot.
- `ps aux` shows a broader list, including processes belonging to other users.

## `top`

Display dynamic, real-time information about running processes and system activity:

```bash
top
```

Unlike `ps`, `top` continuously updates the display.

## `kill`

Send a signal to a process:

```bash
kill <PID>
```

The notes cover these signals:

| Signal | Number | Purpose |
|---|---:|---|
| `SIGHUP` | `1` | Hangup |
| `SIGINT` | `2` | Interrupt |
| `SIGQUIT` | `3` | Quit |
| `SIGKILL` | `9` | Immediately kill; cannot be caught/ignored |
| `SIGTERM` | `15` | Request termination |
| `SIGCONT` | `18` | Continue a stopped process |
| `SIGSTOP` | `19` | Stop a process |

Examples:

```bash
kill <PID>
kill -9 <PID>
kill -15 <PID>
kill -19 <PID>
kill -18 <PID>
```

### `SIGTERM` vs `SIGKILL`

Prefer a graceful termination first:

```bash
kill -15 <PID>
```

or simply:

```bash
kill <PID>
```

Use `SIGKILL` when a process cannot be terminated normally:

```bash
kill -9 <PID>
```

`SIGKILL` cannot be caught or handled by the target process.

## Shell jobs

A command can be run in the background by appending `&`:

```bash
<command> &
```

Example:

```bash
top &
```

## `jobs`

List jobs managed by the current shell:

```bash
jobs
```

The notes show:

```bash
jobs -l
```

for including the process ID (PID) of each job.

## `fg`

Bring a background job to the foreground:

```bash
fg %<job_id>
```

Example:

```bash
fg %1
```

The `%1` refers to shell job number 1, not PID 1.

## `bg`

Continue a stopped job in the background:

```bash
bg %<job_id>
```

Typical workflow:

```text
Ctrl+Z       stop/suspend the foreground job
bg %1        continue it in the background
fg %1        bring it back to the foreground
```

## `nohup`

Run a command so it can continue after the terminal/session closes:

```bash
nohup <command> &
```

The notes describe `nohup` as preventing a command from being terminated by the hangup signal when the terminal closes.

A common example:

```bash
nohup <command> > output.log 2>&1 &
```

This also redirects output so the process can continue independently of the terminal.
