# Arch Linux Removal & Fedora Storage Expansion

**Date:** 21 November 2026  
**System:** HP Pavilion x360 14-dy1xxx  
**Operating system:** Fedora 45  
**Storage device:** WD_BLACK SN7100 1TB NVMe SSD  
**Partition table:** GPT / UEFI

---

## 1. Objective

Remove the existing bare-metal Arch Linux installation and reclaim its disk space for Fedora.

The objectives were:

- Remove the Arch Linux root and boot partitions.
- Preserve Windows 11, Fedora, and the shared NTFS partition.
- Expand Fedora's existing Btrfs filesystem without moving existing partitions.
- Verify that Fedora can boot with the expanded multi-device Btrfs filesystem.
- Remove the obsolete Arch entry from the GRUB menu.
- Identify leftover EFI bootloader files for later cleanup.

## 2. Initial disk layout

The relevant partition layout before removing Arch was:

| Partition | Size | Filesystem | Purpose |
|---|---:|---|---|
| `/dev/nvme0n1p1` | 260 MiB | FAT32 | EFI System Partition |
| `/dev/nvme0n1p2` | 16 MiB | — | Microsoft Reserved |
| `/dev/nvme0n1p3` | 301.1 GiB | NTFS | Windows |
| `/dev/nvme0n1p4` | 869 MiB | NTFS | Windows Recovery |
| `/dev/nvme0n1p5` | 1 GiB | ext4 | Fedora `/boot` |
| `/dev/nvme0n1p6` | 450 GiB | Btrfs | Fedora `/` and `/home` |
| `/dev/nvme0n1p7` | 584 MiB | NTFS | Windows RE tools |
| `/dev/nvme0n1p8` | 58.9 GiB | ext4 | Arch Linux root |
| `/dev/nvme0n1p9` | 117.7 GiB | NTFS | Shared storage |
| `/dev/nvme0n1p10` | 1 GiB | ext4 | Arch Linux boot |

The Arch partitions were located between the shared NTFS partition and the Windows recovery partition.

## 3. Removing Arch Linux partitions

### 3.1 Pre-deletion checks

Before deleting the partitions, verified that:

- The Arch partitions were not mounted.
- Neither partition was being used as swap.
- Fedora's root, home, boot, and EFI partitions were separate.
- The Windows and shared partitions were not targeted.

### 3.2 Partition deletion

Used `parted`:

```bash
sudo parted /dev/nvme0n1
```

Then:

```text
rm 10
rm 8
quit
```

Both Arch partition entries were removed.

The resulting unallocated space was approximately 61,385 MiB (about 60 GiB).

No existing partition boundaries were moved.

## 4. Creating a new Fedora Btrfs member

Rather than moving Windows recovery and Fedora boot partitions to extend the original Fedora partition, the reclaimed space was used to create another partition for the existing Btrfs filesystem.

### 4.1 Creating the partition

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

The newly created partition became:

```text
/dev/nvme0n1p8
```

Its capacity was approximately 59.95 GiB.

### 4.2 Removing stale filesystem metadata

The new partition initially contained an old ext4 signature from the former Arch boot partition.

Inspected it:

```bash
sudo wipefs -n /dev/nvme0n1p8
```

After confirming that the partition was the newly created Fedora data partition, removed the stale signatures:

```bash
sudo wipefs -a /dev/nvme0n1p8
```

Verified that no old signatures remained:

```bash
sudo wipefs -n /dev/nvme0n1p8
```

### 4.3 Adding the partition to Fedora Btrfs

Added the new partition to the existing Fedora Btrfs filesystem:

```bash
sudo btrfs device add /dev/nvme0n1p8 /
```

The command completed successfully and performed a full device TRIM.

**Important:** This adds another device to the existing Btrfs filesystem. It does not create a separate filesystem or require a new mount point.

## 5. Btrfs filesystem configuration

### 5.1 Filesystem identity

The existing Fedora Btrfs filesystem UUID remained unchanged:

```text
c3fce8ce-88f8-4c51-a52a-9f2a76d0ee1e
```

Both `/` and `/home` continue to use this filesystem.

### 5.2 `/etc/fstab`

The relevant entries remain:

```fstab
UUID=c3fce8ce-88f8-4c51-a52a-9f2a76d0ee1e /     btrfs subvol=@,compress=zstd:1 0 0
UUID=b231f965-3d14-44f6-8dcd-2ac23664cbeb /boot ext4  defaults                 1 2
UUID=BC06-DEF9                            /boot/efi vfat umask=0077,shortname=winnt 0 2
UUID=c3fce8ce-88f8-4c51-a52a-9f2a76d0ee1e /home btrfs subvol=@home,compress=zstd:1 0 0
UUID=558D3E120E80985A                      /mnt/shared ntfs-3g defaults,uid=1000,gid=1000,umask=022,exec,windows_names,nofail,x-systemd.device-timeout=2 0 0
```

No changes to `/etc/fstab` were necessary because both Btrfs devices belong to the same filesystem UUID.

### 5.3 Btrfs device verification

Command:

```bash
sudo btrfs filesystem show /
```

Verified output:

```text
Label: 'fedora' uuid: c3fce8ce-88f8-4c51-a52a-9f2a76d0ee1e
Total devices 2

devid 1 size 450.02GiB used 448.74GiB path /dev/nvme0n1p6
devid 2 size 59.95GiB  used 0.00B    path /dev/nvme0n1p8
```

The filesystem now consists of two devices:

| Device | Size | Role |
|---|---:|---|
| `/dev/nvme0n1p6` | 450.02 GiB | Original Fedora Btrfs member |
| `/dev/nvme0n1p8` | 59.95 GiB | Newly added Btrfs member |

### 5.4 Filesystem capacity

After adding the new device:

```bash
df -hT /
```

Result:

```text
Filesystem       Type   Size  Used  Avail  Use%
/dev/nvme0n1p6    btrfs  510G  396G  101G   80%
```

The filesystem capacity increased from approximately 450 GiB to 510 GiB.

**Note:** Btrfs reports the filesystem through its primary device path in `df`, even though the filesystem spans two partitions.

The data profile remains `single`, while metadata uses `DUP`. Both partitions reside on the same physical SSD, so this configuration does not provide protection against physical SSD failure.

No balance operation was required merely to make the additional capacity available.

## 6. Initramfs and boot verification

Because the root filesystem now spans two partitions, early boot device discovery was checked.

### 6.1 `/etc/fstab` verification

Confirmed that both root and home reference the same Btrfs filesystem UUID.

### 6.2 Initramfs verification

Command:

```bash
sudo lsinitrd /boot/initramfs-$(uname -r).img | grep -i btrfs
```

The output included:

- `btrfs`
- `/usr/bin/btrfs`
- `/usr/bin/btrfsck`
- `/usr/bin/btrfstune`
- Btrfs udev rules

This confirmed that the initramfs contains Btrfs-related utilities and rules.

No initramfs regeneration was necessary.

### 6.3 Reboot verification

After rebooting Fedora, checked:

```bash
sudo btrfs filesystem show /
df -hT /
```

Both Btrfs devices were detected successfully.

Final verified capacity:

- Total: approximately 510 GiB
- Used: approximately 396 GiB
- Available: approximately 101 GiB
- Usage: 80%

**Result: Fedora successfully booted with the expanded multi-device Btrfs filesystem.**

## 7. GRUB configuration cleanup

The previous GRUB configuration had detected both Windows and Arch Linux.

After deleting Arch, regenerated the configuration:

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

This confirms:

- Windows Boot Manager was detected.
- GRUB configuration generation completed successfully.
- The removed Arch installation was no longer detected.
- UEFI Firmware Settings entry was retained.

The existing GRUB configuration settings were preserved, including:

```bash
GRUB_TIMEOUT=5
GRUB_DEFAULT=saved
GRUB_ENABLE_BLSCFG=true
GRUB_DISABLE_OS_PROBER=false
```

## 8. Final partition layout

The resulting partition arrangement is:

| Partition | Size | Filesystem | Purpose |
|---|---:|---|---|
| `/dev/nvme0n1p1` | 260 MiB | FAT32 | EFI System Partition |
| `/dev/nvme0n1p2` | 16 MiB | — | Microsoft Reserved |
| `/dev/nvme0n1p3` | 301.1 GiB | NTFS | Windows |
| `/dev/nvme0n1p4` | 869 MiB | NTFS | Windows Recovery |
| `/dev/nvme0n1p5` | 1 GiB | ext4 | Fedora `/boot` |
| `/dev/nvme0n1p6` | 450.02 GiB | Btrfs | Fedora filesystem, device 1 |
| `/dev/nvme0n1p7` | 584 MiB | NTFS | Windows RE tools |
| `/dev/nvme0n1p8` | 59.95 GiB | Btrfs | Fedora filesystem, device 2 |
| `/dev/nvme0n1p9` | 117.7 GiB | NTFS | Shared storage |

The partition numbering reflects GPT partition numbers, not physical disk order.

## 9. Remaining tasks

The storage expansion and GRUB regeneration are complete. The following items remain for a separate cleanup session.

### EFI bootloader inspection

Inspect:

```bash
sudo ls -lah /boot/efi/EFI/
sudo efibootmgr -v
```

Previously identified potentially obsolete directories:

- `EFI/Arch` — likely leftover Arch bootloader files.
- `EFI/GRUB` — contains a Debian-labelled bootloader entry and appears to reference an unavailable filesystem UUID.

These directories and their associated firmware entries have **not** been deleted.

Before removing anything, verify the actual HP firmware boot menu entries and distinguish active boot entries from orphaned EFI files.

### Future Arch Linux VM

The bare-metal Arch installation has been removed. The plan is to use Arch Linux as a virtual machine through the existing libvirt/KVM setup.

Existing Kali, Windows 10, and Windows 11 virtual machines must be preserved.

---

## 10. Final status

| Task | Status |
|---|---|
| Verify Arch partitions are unused | Complete |
| Delete Arch root and boot partitions | Complete |
| Create new Fedora data partition | Complete |
| Add new partition to Btrfs | Complete |
| Verify filesystem capacity | Complete |
| Verify `/etc/fstab` | Complete |
| Verify Btrfs initramfs contents | Complete |
| Reboot with multi-device Btrfs | Complete |
| Regenerate GRUB configuration | Complete |
| Confirm Windows Boot Manager detection | Complete |
| Inspect leftover EFI directories | Pending |
| Inspect and clean obsolete UEFI entries | Pending |
| Prepare Arch Linux virtual machine | Pending |

**Final outcome:** Arch Linux was removed from the physical installation, its approximately 60 GiB of space was incorporated into Fedora's existing Btrfs filesystem, and Fedora successfully booted with the expanded approximately 510 GiB filesystem. Windows and the shared NTFS partition were preserved.