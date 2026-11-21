# Fedora System Configuration & Maintenance Log

**System:** HP Pavilion x360 14-dy1xxx  
**CPU:** Intel Core i5-1155G7  
**RAM:** 32 GB  
**Storage:** WD_BLACK SN7100 1TB NVMe SSD  
**OS:** Fedora 45  
**Desktop:** GNOME / Mutter 51.1  
**Display server:** Wayland  
**Boot mode:** UEFI / GPT  

This document consolidates the significant Fedora system configuration changes, maintenance operations, and troubleshooting outcomes. It is intended as a reference for future system maintenance and configuration recovery.

---

# 1. Display Configuration — GDM External Monitor

**Date:** 13 November 2026

## 1.1 Hardware and display arrangement

The laptop uses two displays:

| Display | Connection | Resolution |
|---|---|---|
| LG UltraGear external monitor | HDMI | 1920 × 1080, 179.961 Hz |
| Internal laptop display | eDP | Built-in panel |

Display identifiers observed:

- External: `HDMI-1` / `HDMI-A-1`
- Internal: `eDP-1`

The desired arrangement is to have the GDM login screen appear on the external LG monitor, with the external display acting as the primary display during the user session.

## 1.2 GDM monitor configuration

GNOME stores display configuration in `monitors.xml`. The GDM greeter has its own configuration, separate from the logged-in user's display configuration.

Relevant paths:

```text
~/.config/monitors.xml

/var/lib/gdm/.config/monitors.xml

/var/lib/gdm/seat0/config/monitors.xml
```

A backup was created:

```text
/var/lib/gdm/.config/monitors.xml.backup
```

The user's monitor configuration was copied into the GDM configuration locations. Ownership and SELinux labels were corrected using ownership adjustment and `restorecon`.

Relevant commands used during the procedure included:

```bash
sudo cp ~/.config/monitors.xml /var/lib/gdm/.config/monitors.xml
```

The GDM configuration directories also required appropriate ownership and SELinux context restoration.

After applying the configuration, the system was rebooted to test the greeter.

## 1.3 Internal display disable test

An explicit `<disabled>` entry for `eDP-1` was tested in the GDM monitor configuration.

This caused the login screen to move to the external monitor.

However, this test was subsequently reverted because the intended configuration was to retain the normal dual-display arrangement rather than permanently disable the laptop panel.

## 1.4 Final observed behaviour

After restoring the previous configuration and rebooting:

- The GDM login screen continued to appear on the external monitor.
- The external monitor remained the effective primary display for the login screen.
- A grey background that had previously appeared on the external monitor instead appeared on the laptop display.
- The laptop display was not completely black.

This behaviour persisted even after reverting the explicit internal-display disable test.

**Important:** The final observed behaviour was functional, but the precise reason the grey background changed displays after reverting the configuration was not conclusively established.

Do not assume that the grey background indicates a failed monitor configuration.

## 1.5 Troubleshooting notes

If the GDM login screen moves to the wrong display after a future update:

1. Inspect the user's monitor configuration:

   ```bash
   cat ~/.config/monitors.xml
   ```

2. Inspect GDM's configuration:

   ```bash
   sudo cat /var/lib/gdm/.config/monitors.xml
   sudo cat /var/lib/gdm/seat0/config/monitors.xml
   ```

3. Compare the display connector identifiers and primary-display settings.

4. Check file ownership and SELinux labels before restarting or rebooting.

5. Preserve the existing backup before making changes.

Avoid disabling `eDP-1` unless intentionally testing an external-only GDM configuration.

---

# 2. Storage Configuration — Arch Linux Removal

**Date:** 21 November 2026

## 2.1 Objective

Remove the bare-metal Arch Linux installation and reclaim its disk space for Fedora without moving existing Windows or Fedora partitions.

The intended final arrangement:

- Fedora remains the primary Linux installation.
- Windows 11 remains installed.
- Shared NTFS storage remains available.
- Fedora's existing Btrfs filesystem uses the reclaimed space.
- Arch Linux can later be installed as a virtual machine using KVM/libvirt.

## 2.2 Initial partition layout

| Partition | Size | Filesystem | Purpose |
|---|---:|---|---|
| `p1` | 260 MiB | FAT32 | EFI System Partition |
| `p2` | 16 MiB | — | Microsoft Reserved |
| `p3` | 301.1 GiB | NTFS | Windows |
| `p4` | 869 MiB | NTFS | Windows Recovery |
| `p5` | 1 GiB | ext4 | Fedora `/boot` |
| `p6` | 450 GiB | Btrfs | Fedora `/` and `/home` |
| `p7` | 584 MiB | NTFS | Windows RE tools |
| `p8` | 58.9 GiB | ext4 | Arch root |
| `p9` | 117.7 GiB | NTFS | Shared storage |
| `p10` | 1 GiB | ext4 | Arch boot |

## 2.3 Pre-deletion checks

Before deleting the Arch partitions, verified:

- Neither Arch partition was mounted.
- Neither was being used as swap.
- Fedora's root, home, boot, and EFI partitions were separate.
- Windows and shared storage were not being modified.

The active swap device was `/dev/zram0`.

## 2.4 Removing Arch partitions

Opened `parted`:

```bash
sudo parted /dev/nvme0n1
```

Deleted the Arch partitions:

```text
rm 10
rm 8
quit
```

The partition entries were removed, leaving approximately 61,385 MiB of unallocated space.

No existing partition boundaries were moved.

## 2.5 Creating the Fedora data partition

Instead of moving existing partitions, a new partition was created in the reclaimed space.

```bash
sudo parted /dev/nvme0n1
```

Inside `parted`:

```text
unit MiB
print free
mkpart fedora_data 429191MiB 490576MiB
print
quit
```

The new partition became:

```text
/dev/nvme0n1p8
```

Its capacity was approximately 59.95 GiB.

## 2.6 Removing stale ext4 metadata

The new partition initially contained an old ext4 signature from the former Arch boot partition.

Inspected it:

```bash
sudo wipefs -n /dev/nvme0n1p8
```

After confirming the target, removed the stale signature:

```bash
sudo wipefs -a /dev/nvme0n1p8
```

Verified:

```bash
sudo wipefs -n /dev/nvme0n1p8
```

No old signatures remained.

## 2.7 Adding the partition to Fedora Btrfs

Added the new partition to the existing Fedora Btrfs filesystem:

```bash
sudo btrfs device add /dev/nvme0n1p8 /
```

The operation completed successfully and performed a full device TRIM.

The filesystem now spans two partitions on the same physical SSD.

---

# 3. Btrfs Filesystem Configuration

## 3.1 Filesystem UUID

The existing filesystem UUID remained unchanged:

```text
c3fce8ce-88f8-4c51-a52a-9f2a76d0ee1e
```

Both `/` and `/home` continue to use this UUID.

## 3.2 `/etc/fstab`

The relevant entries remain:

```fstab
UUID=c3fce8ce-88f8-4c51-a52a-9f2a76d0ee1e / btrfs subvol=@,compress=zstd:1 0 0

UUID=b231f965-3d14-44f6-8dcd-2ac23664cbeb /boot ext4 defaults 1 2

UUID=BC06-DEF9 /boot/efi vfat umask=0077,shortname=winnt 0 2

UUID=c3fce8ce-88f8-4c51-a52a-9f2a76d0ee1e /home btrfs subvol=@home,compress=zstd:1 0 0

UUID=558D3E120E80985A /mnt/shared ntfs-3g defaults,uid=1000,gid=1000,umask=022,exec,windows_names,nofail,x-systemd.device-timeout=2 0 0
```

No changes were necessary.

The filesystem UUID identifies the complete Btrfs filesystem, not just the original partition.

## 3.3 Btrfs device layout

Verified using:

```bash
sudo btrfs filesystem show /
```

Final output:

```text
Label: 'fedora' uuid: c3fce8ce-88f8-4c51-a52a-9f2a76d0ee1e
Total devices 2

devid 1 size 450.02GiB used 448.74GiB path /dev/nvme0n1p6
devid 2 size 59.95GiB  used 0.00B    path /dev/nvme0n1p8
```

| Device | Capacity | Role |
|---|---:|---|
| `/dev/nvme0n1p6` | 450.02 GiB | Original Fedora Btrfs member |
| `/dev/nvme0n1p8` | 59.95 GiB | Additional Fedora Btrfs member |

## 3.4 Filesystem capacity

Verified using:

```bash
df -hT /
```

Result:

```text
Filesystem       Type   Size  Used  Avail  Use%
/dev/nvme0n1p6    btrfs  510G  396G  101G   80%
```

The total filesystem capacity increased from approximately 450 GiB to 510 GiB.

The Btrfs data profile remains `single`, while metadata uses `DUP`.

**Storage reliability note:** Both Btrfs devices are partitions on the same SSD. This provides additional capacity, not physical-device redundancy.

A balance operation was not required just to make the new capacity available.

---

# 4. Initramfs and Boot Verification

Since the root filesystem spans two devices, early boot support was checked.

## 4.1 Verify `/etc/fstab`

Confirmed that `/` and `/home` both reference the same Btrfs filesystem UUID.

## 4.2 Verify initramfs contents

Command:

```bash
sudo lsinitrd /boot/initramfs-$(uname -r).img | grep -i btrfs
```

The output included:

- Btrfs utilities.
- `btrfsck`.
- `btrfstune`.
- Btrfs udev rules.

This confirmed that the initramfs contained Btrfs-related utilities and rules.

## 4.3 Reboot test

After rebooting, ran:

```bash
sudo btrfs filesystem show /
df -hT /
```

Both Btrfs devices were detected successfully.

Final verified capacity:

- Total: approximately 510 GiB.
- Used: approximately 396 GiB.
- Available: approximately 101 GiB.
- Usage: 80%.

**Result:** Fedora successfully booted with the expanded multi-device Btrfs filesystem.

No `fstab` changes or initramfs regeneration were necessary.

---

# 5. GRUB Configuration

## 5.1 Existing configuration

The relevant `/etc/default/grub` settings were:

```bash
GRUB_TIMEOUT=5
GRUB_DEFAULT=saved
GRUB_ENABLE_BLSCFG=true
GRUB_DISABLE_OS_PROBER=false
```

`GRUB_DISABLE_OS_PROBER=false` is retained so that Windows can be detected by GRUB.

## 5.2 Regenerating GRUB

After removing Arch, regenerated the GRUB configuration:

```bash
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

Output:

```text
Generating grub configuration file ...
Found theme: /boot/grub2/themes/vimix/theme.txt
Found Windows Boot Manager on /dev/nvme0n1p1@/EFI/Microsoft/Boot/bootmgfw.efi
Adding boot menu entry for UEFI Firmware Settings ...
done
```

Verified:

- Windows Boot Manager detected.
- GRUB configuration generated successfully.
- Arch installation no longer detected.
- UEFI Firmware Settings entry retained.

---

# 6. Final Partition Layout

| Partition | Size | Filesystem | Purpose |
|---|---:|---|---|
| `p1` | 260 MiB | FAT32 | EFI System Partition |
| `p2` | 16 MiB | — | Microsoft Reserved |
| `p3` | 301.1 GiB | NTFS | Windows |
| `p4` | 869 MiB | NTFS | Windows Recovery |
| `p5` | 1 GiB | ext4 | Fedora `/boot` |
| `p6` | 450.02 GiB | Btrfs | Fedora device 1 |
| `p7` | 584 MiB | NTFS | Windows RE tools |
| `p8` | 59.95 GiB | Btrfs | Fedora device 2 |
| `p9` | 117.7 GiB | NTFS | Shared storage |

Partition numbers do not necessarily represent physical disk order.

---

# 7. Pending EFI and UEFI Cleanup

The storage expansion and GRUB regeneration are complete. EFI cleanup remains a separate task.

Previously identified potentially obsolete EFI directories:

```text
/boot/efi/EFI/Arch
/boot/efi/EFI/GRUB
```

The `EFI/GRUB` directory contains a Debian-labelled bootloader entry and appears to reference an unavailable filesystem UUID.

A previous inspection of `EFI/GRUB/BOOTX64.CSV` showed:

```text
shimx64.efi,debian,,This is the boot entry for debian
```

The firmware entries previously included:

- Fedora entries.
- Windows Boot Manager.
- A Debian entry.
- Older Fedora entries.
- An Arch entry, which was removed.

The firmware boot order also contained some stale references.

**Do not delete the EFI directories or additional UEFI entries until the HP firmware boot menu has been inspected.**

Next inspection commands:

```bash
sudo ls -lah /boot/efi/EFI/
```

```bash
sudo efibootmgr -v
```

Distinguish between:

- Actual firmware boot entries.
- EFI files that remain on the EFI System Partition.
- Entries currently included in the firmware boot order.

---

# 8. Other System Troubleshooting — Not Yet a Confirmed Configuration Fix

## 8.1 Bluetooth

A recurring Bluetooth issue was observed after Fedora 45 upgrades and reboots.

Hardware:

```text
USB ID: 13d3:3567
Manufacturer: IMC Networks
```

The Bluetooth controller sometimes disappears from Fedora, while it may reappear after a shutdown or subsequent reboot.

Configuration files previously inspected or modified:

```text
/etc/modprobe.d/mt7921_bt.conf
/etc/modprobe.d/btusb.conf
```

Relevant options included:

```text
options btusb enable_autosuspend=0
options btmtk reset=1
options btusb disable_scofix=1
```

The issue was intermittent and not conclusively resolved.

Do not treat these options as a confirmed permanent fix. Continue diagnosis if the controller disappears again.

## 8.2 Suspend/resume

Suspend/resume and Bluetooth device availability were investigated together because the Bluetooth controller's disappearance appeared to correlate with certain power and reboot sequences.

The underlying cause was not conclusively established.

---

# 9. Maintenance Reference

Useful commands for future checks:

| Purpose | Command |
|---|---|
| Display partition layout | `lsblk -o NAME,SIZE,FSTYPE,LABEL,UUID,MOUNTPOINTS` |
| Inspect free disk space | `sudo parted /dev/nvme0n1 print free` |
| Show Btrfs devices | `sudo btrfs filesystem show /` |
| Show Btrfs capacity and profiles | `sudo btrfs filesystem usage -T /` |
| Check mounted filesystem capacity | `df -hT / /home` |
| Inspect filesystem table | `cat /etc/fstab` |
| Inspect initramfs | `sudo lsinitrd /boot/initramfs-$(uname -r).img` |
| Regenerate GRUB | `sudo grub2-mkconfig -o /boot/grub2/grub.cfg` |
| Inspect EFI files | `sudo ls -lah /boot/efi/EFI/` |
| Inspect UEFI boot entries | `sudo efibootmgr -v` |
| Inspect Bluetooth controllers | `bluetoothctl list` |
| Inspect USB devices | `lsusb` |

---

# 10. Overall Status

| Configuration / Task | Status |
|---|---|
| GDM external-monitor login configuration | Functional; final behaviour documented |
| GDM internal-display disable test | Reverted |
| Arch Linux partition removal | Complete |
| Fedora Btrfs expansion | Complete |
| `/etc/fstab` verification | Complete |
| Initramfs verification | Complete |
| Reboot with two-device Btrfs | Successful |
| GRUB regeneration | Complete |
| Windows Boot Manager detection | Successful |
| EFI directory cleanup | Pending |
| UEFI boot-entry cleanup | Pending |
| Bluetooth intermittent-disappearance diagnosis | Unresolved |
| Arch Linux KVM/libvirt VM preparation | Pending |

**Final summary:** Fedora's GDM login display configuration has been documented, Arch Linux has been removed from the physical installation, and its reclaimed space has been incorporated into Fedora's existing Btrfs filesystem. Fedora successfully boots with the expanded 510 GiB filesystem, and GRUB detects Windows Boot Manager. EFI cleanup and the intermittent Bluetooth issue remain separate pending tasks.