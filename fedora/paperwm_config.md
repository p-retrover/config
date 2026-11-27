# PaperWM Configuration — Fedora 45

## 1. Environment

| Component | Configuration |
|---|---|
| OS | Fedora Linux 45 |
| GNOME Shell | 51.1 |
| Display server | Wayland |
| Window manager | Mutter 51.1 |
| Extension | PaperWM |
| Window switcher | AATWS (Advanced Alt-Tab Window Switcher) |

## 2. Extension paths

**PaperWM**
```text
~/.local/share/gnome-shell/extensions/paperwm@paperwm.github.com
```

**AATWS**
```text
~/.local/share/gnome-shell/extensions/advanced-alt-tab@G-dH.github.com
```

## 3. Alt-Tab configuration

AATWS is used as the window-switching interface alongside PaperWM.

The configuration uses the Alt-Tab interaction. Avoid introducing additional shortcut bindings that conflict with this setup.

### AATWS monitor filter

Configured to show windows from the current workspace across all monitors.

```bash
AATWS="$HOME/.local/share/gnome-shell/extensions/advanced-alt-tab@G-dH.github.com"
SCHEMA="org.gnome.shell.extensions.advanced-alt-tab-window-switcher"

gsettings --schemadir "$AATWS/schemas" set "$SCHEMA" \
  win-switcher-popup-filter 2
```

Monitor filter values:

| Value | Behaviour |
|---|---|
| `1` | All workspaces and monitors |
| `2` | Current workspace across monitors |
| `3` | Current monitor |

Selected value: `2`.

### AATWS search

To use type-to-search:
1. Hold Alt to open the switcher.
2. Keep Alt pressed while typing.
3. Release Alt to close the popup.

## 4. Extension management

List enabled extensions:

```bash
gnome-extensions list --enabled
```

Inspect PaperWM:

```bash
gnome-extensions info paperwm@paperwm.github.com
```

Enable or disable PaperWM:

```bash
gnome-extensions enable paperwm@paperwm.github.com
gnome-extensions disable paperwm@paperwm.github.com
```

## 5. Troubleshooting notes

### PaperWM and AATWS interaction

A compatibility issue was investigated involving their window-switcher implementations.

The extensions use different window-list interfaces, which can cause problems when interacting with the same GNOME switcher implementation.

Avoid unnecessary changes to extension source files when configuring shortcuts.

### Display blackout issue

A separate display issue was investigated in November 2026:
- Both internal and external displays occasionally went black after approximately 25 seconds.
- Caps Lock woke the displays.
- Disabling PaperWM did not resolve the issue.
- Disabling the GJS on-screen keyboard extension did not resolve it.
- Disabling ambient brightness did not resolve it.
- Logging out and starting a fresh GNOME session temporarily resolved it.

No causal relationship with PaperWM was established.

## 6. Configuration principles

- Preserve the existing Alt-Tab configuration.
- Avoid introducing conflicting window-switcher shortcuts.
- Use GSettings schemas for configuration where possible.
- Change one extension setting at a time when troubleshooting.
- Keep PaperWM and AATWS troubleshooting separate from unrelated display-power issues.

---

**Last documented:** November 2026  
**Platform:** Fedora 45 / GNOME 51.1 / Wayland