# Bash Prompt Customization Reference (Git Bash / Linux)

## Overview

The shell prompt in Bash is controlled primarily by the variable:

```
PS1
```

Customizing `PS1` allows you to modify:

* prompt symbols
* colors
* multi-line prompts
* git branch indicators
* timestamps
* command status indicators

This applies to:

* Linux Bash shells
* Git Bash on Windows
* MSYS2 shells
* WSL environments

---

# 1. Bash Prompt Variable (`PS1`)

`PS1` defines the **primary interactive prompt**.

Example:

```
PS1="\u@\h:\w\$ "
```

Result:

```
user@machine:/home/user$
```

### Common Escape Sequences

| Sequence | Meaning                     |
| -------- | --------------------------- |
| `\u`     | username                    |
| `\h`     | hostname                    |
| `\w`     | full working directory      |
| `\W`     | current directory only      |
| `\d`     | date                        |
| `\t`     | time                        |
| `\n`     | newline                     |
| `\$`     | `$` for user / `#` for root |

Example:

```
PS1="\n➤ \W \$ "
```

Output:

```
➤ project $
```

---

# 2. ANSI Color Codes

Bash prompts use **ANSI escape sequences** for colors.

General format:

```
\[\033[COLORm\]
```

Reset color:

```
\[\033[0m\]
```

### Common Colors

| Code | Color   |
| ---- | ------- |
| 30   | black   |
| 31   | red     |
| 32   | green   |
| 33   | yellow  |
| 34   | blue    |
| 35   | magenta |
| 36   | cyan    |
| 37   | white   |

Example:

```
PS1="\[\033[32m\]\W > \[\033[0m\]"
```

Displays the directory in green.

---

# 3. Multi-Line Prompt

A newline can be added using:

```
\n
```

Example:

```
PS1="\n➤ \W > "
```

Output:

```
➤ project >
```

---

# 4. Git Branch in Prompt

Git provides a helper function:

```
__git_ps1
```

This function displays the current git branch.

Example:

```
PS1='\W$(__git_ps1 " (%s)") $ '
```

Output:

```
repo (main) $
```

### Required scripts

Git must load:

```
git-completion.bash
git-prompt.sh
```

Typical location:

```
/usr/share/git/completion/
```

or

```
C:\Program Files\Git\mingw64\share\git\completion\
```

Example loading:

```
source git-completion.bash
source git-prompt.sh
```

---

# 5. Git Bash Specific Configuration

Git Bash loads prompt configuration from:

```
/etc/profile
/etc/profile.d/*.sh
```

Example file:

```
C:\Program Files\Git\etc\profile.d\git-prompt.sh
```

However, editing system files is discouraged because updates may overwrite changes.

Preferred location:

```
~/.bashrc
```

or

```
~/.config/git/git-prompt.sh
```

---

# 6. Bash Startup File Order

Typical startup sequence:

1. `/etc/profile`
2. `/etc/profile.d/*.sh`
3. `~/.bash_profile`
4. `~/.bashrc`

Git Bash also loads:

```
git-prompt.sh
```

from `/etc/profile.d`.

---

# 7. Command Substitution in Prompts

Dynamic information can be inserted using:

```
$(command)
```

Example showing time:

```
PS1='$(date +"%H:%M") \W $ '
```

Output:

```
22:15 project $
```

---

# 8. Exit Status Indicator

The exit code of the previous command is stored in:

```
$?
```

Example showing failure indicator:

```
PS1='$(if [ $? -ne 0 ]; then echo "✗ "; fi)\W $ '
```

Output if previous command failed:

```
✗ project $
```

---

# 9. Example Custom Prompt

Example configuration similar to many modern terminals:

```
PS1='\[\033[35m\]\n➤ \W\[\033[36m\]$(__git_ps1 " (%s)")\[\033[0m\] ➤ '
```

Possible output:

```
➤ project (main) ➤
```

---

# 10. MSYS2 / Git Bash Compatibility

Git Bash is based on **MSYS2**, which emulates a Unix environment on Windows.

Sometimes prompts are stored in:

```
MSYS2_PS1
```

Example:

```
MSYS2_PS1="$PS1"
```

This helps other MSYS tools detect the prompt configuration.

---

# 11. Custom Bash Completion Scripts

Bash can load additional completion scripts from:

```
~/bash_completion.d/
```

Example loader:

```
for c in "$HOME"/bash_completion.d/*.bash
do
    test ! -f "$c" || . "$c"
done
```

This allows custom tab completion for tools.

---

# 12. Useful References

## Bash

* GNU Bash Manual
  [https://www.gnu.org/software/bash/manual/bash.html#Controlling-the-Prompt](https://www.gnu.org/software/bash/manual/bash.html#Controlling-the-Prompt)

* Bash Prompt HOWTO
  [https://tldp.org/HOWTO/Bash-Prompt-HOWTO/](https://tldp.org/HOWTO/Bash-Prompt-HOWTO/)

---

## Git Prompt

Git prompt script documentation

[https://github.com/git/git/blob/master/contrib/completion/git-prompt.sh](https://github.com/git/git/blob/master/contrib/completion/git-prompt.sh)

---

## ANSI Color Codes

Terminal color reference

[https://misc.flogisoft.com/bash/tip_colors_and_formatting](https://misc.flogisoft.com/bash/tip_colors_and_formatting)

---

## Bash Startup Files

Explanation of `.bashrc` vs `.bash_profile`

[https://linuxize.com/post/bashrc-vs-bash-profile/](https://linuxize.com/post/bashrc-vs-bash-profile/)

---

# 13. Recommended Tools for Advanced Prompts

If complex prompts are required, consider using prompt frameworks:

* **Starship Prompt**
  [https://starship.rs](https://starship.rs)

* **Powerlevel10k (zsh)**
  [https://github.com/romkatv/powerlevel10k](https://github.com/romkatv/powerlevel10k)

These provide fast, feature-rich prompts with git status indicators.

---
