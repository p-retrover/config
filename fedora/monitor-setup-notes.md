# Fedora GNOME 51 — GDM External Monitor Configuration

## Objective

Make the GDM login screen appear on the external LG Ultragear monitor when connected, while retaining the laptop display as a secondary display and preserving a laptop-only configuration for when the external monitor is disconnected.

## System information

- OS: Fedora 45
- GNOME Shell: 51.1
- Mutter: 51.1
- GDM: 51.1.1
- Display server: Wayland
- External monitor: LG Ultragear
- External connector (Mutter): HDMI-1
- External resolution: 1920 × 1080
- External refresh rate: 179.961 Hz
- Laptop connector: eDP-1
- Laptop resolution: 1920 × 1080

## Important discovery

Copying `~/.config/monitors.xml` to `/var/lib/gdm/.config/monitors.xml` using the traditional instructions did not solve the problem.

The working configuration was established under:

`/var/lib/gdm/seat0/config/monitors.xml`

GDM's per-seat monitor configuration was the important part of the solution.

## What we tested

1. Copied the personal GNOME monitor configuration to `/var/lib/gdm/.config/`.
2. Simplified the configuration to remove alternative monitor layouts.
3. Tested the per-seat configuration directory.
4. Created a single-monitor configuration with the laptop display explicitly disabled using a `<disabled>` section.
5. Confirmed that this made the login interface appear on the external monitor.
6. Restored the original multi-monitor configuration to both GDM configuration locations.

## Current working configuration

The current configuration is the original multi-monitor `monitors.xml`, restored to:

- `/var/lib/gdm/.config/monitors.xml`
- `/var/lib/gdm/seat0/config/monitors.xml`

The observed result after restoration:

- LG Ultragear displays the GDM login interface.
- Laptop display remains enabled and displays the grey GDM background.
- Normal GNOME desktop configuration remains untouched.

The original XML contains multiple configurations, including:
- HDMI-1 primary with eDP-1 secondary.
- Laptop-only configuration with eDP-1 primary.
- Alternative DP-1 configurations.

## Useful commands

### Inspect active connectors

```bash
for f in /sys/class/drm/card*-*/status; do
    printf '%s: ' "$f"
    cat "$f"
done
```

### Inspect GDM monitor configurations

```bash
sudo find /var/lib/gdm -name monitors.xml -ls
```

### Back up the current GDM configuration

```bash
sudo cp /var/lib/gdm/seat0/config/monitors.xml \
/var/lib/gdm/seat0/config/monitors.xml.backup
```

### Restore ownership and SELinux context

```bash
sudo chown --reference=/var/lib/gdm/seat0/config \
/var/lib/gdm/seat0/config/monitors.xml

sudo chmod 644 /var/lib/gdm/seat0/config/monitors.xml

sudo restorecon -v /var/lib/gdm/seat0/config/monitors.xml
```

### Restart GDM

From a TTY:

```bash
sudo systemctl restart gdm
```

Warning: This terminates the current graphical session and any unsaved work.

A reboot is preferable when testing startup monitor configuration.

## Important precautions

- Do not modify the personal `~/.config/monitors.xml` unnecessarily.
- Do not remove the laptop display from the GDM configuration permanently.
- Preserve the original multi-monitor configuration before experimenting.
- If changing the monitor connection or configuration, inspect the active connectors first.
- The laptop-only fallback configuration has not yet been independently tested by booting without the external monitor.

## Final status

The external-monitor GDM login problem is resolved.

The restored multi-monitor configuration is currently working. No further modifications are necessary unless the monitor arrangement changes or a future Fedora/GNOME upgrade alters GDM's behaviour.