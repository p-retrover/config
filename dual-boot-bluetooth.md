# Dual-Boot Bluetooth Synchronization Guide

## Synchronizing Bluetooth Pairing Keys Between Windows and Linux

When the same Bluetooth adapter is used by both Windows and Linux, each operating system can end up storing different pairing credentials for the same Bluetooth device.

For **Classic Bluetooth**, the important credential is the **Link Key**. If Windows and Linux have different keys, pairing the device in one OS can cause it to stop connecting in the other.

The goal of this guide is to extract the Windows pairing key and install the corresponding key into Linux/BlueZ so that both operating systems use the same pairing credentials.

> **Scope:** This procedure primarily applies to Classic Bluetooth devices. BLE devices may require additional keys such as LTK, IRK, EDIV, and RAND.

---

# 1. Current Device Profile

The example configuration used throughout this guide is:

| Device                  | MAC address         |
| ----------------------- | ------------------- |
| PC Bluetooth adapter    | `90:08:68:12:83:1c` |
| Target Bluetooth device | `9a:b1:7a:4f:97:8d` |

The same procedure works with different MAC addresses; replace the example addresses accordingly.

---

# 2. Initial Pairing Sequence — Mandatory

Before extracting any keys, establish a working pairing in both operating systems.

### Step 1 — Linux

1. Boot into Linux.
2. Pair the target Bluetooth device normally.
3. Verify that it connects.
4. **Shut Linux down completely.**

Do not simply suspend the machine.

### Step 2 — Windows

1. Boot into Windows.
2. Pair the same Bluetooth device.
3. Verify that it connects.
4. **Shut Windows down completely.**

### Windows Fast Startup

Make sure Windows Fast Startup is disabled.

Alternatively, hold **Shift** while clicking **Shut down** to force a full shutdown.

This is important because Windows Fast Startup can leave the system in a partially hibernated state.

---

# 3. Boot Back Into Linux

Boot Linux again.

At this point, Linux may fail to connect to the device because Windows has generated/stored a different pairing key.

This is the state we want before extracting the Windows key.

---

# 4. Back Up Linux Bluetooth Configuration

Before modifying anything under `/var/lib/bluetooth`, create a backup:

```bash
sudo cp -a /var/lib/bluetooth /var/lib/bluetooth.backup
```

Verify that the backup exists:

```bash
sudo ls -la /var/lib/bluetooth.backup
```

If something goes wrong later, this gives you a way to restore the previous BlueZ state.

---

# 5. Method A — Automated Synchronization

If you have multiple Bluetooth devices such as:

* mouse
* keyboard
* headphones
* game controller
* earbuds

an automated synchronization utility can save considerable time.

However, because these are third-party utilities, **verify the upstream repository/package before installing and running them as root**.

---

## Option 1 — `bt-dualboot`

If you have verified the package and it supports your Linux distribution and BlueZ configuration:

```bash
sudo pip install bt-dualboot
```

A safer Python-environment approach is preferable if the package supports it, but the command above is retained here because it is part of the original procedure.

### Check what needs to change

First run a dry run:

```bash
sudo bt-dualboot --sync-all --dry-run
```

Review the output carefully.

You want to verify that:

* the correct Windows partition was detected;
* the correct Windows registry hive was found;
* the correct Bluetooth adapter was detected;
* the expected Bluetooth devices were identified;
* the proposed changes are going to the expected Linux BlueZ files.

If everything looks correct:

```bash
sudo bt-dualboot --sync-all
```

Then restart Bluetooth:

```bash
sudo systemctl restart bluetooth
```

Check the service:

```bash
systemctl status bluetooth
```

---

## Option 2 — `bt-keys-sync`

An alternative approach is to clone the synchronization utility and run it directly.

The original command should use the **actual upstream repository URL** rather than a placeholder:

```bash
git clone <VERIFIED-BT-KEYS-SYNC-REPOSITORY>
cd bt-keys-sync
```

Then:

```bash
sudo ./bt-keys-sync --windows-keys
```

Restart Bluetooth:

```bash
sudo systemctl restart bluetooth
```

Check the service:

```bash
systemctl status bluetooth
```

> **Do not blindly execute an unknown GitHub script with `sudo`.** Verify the repository, source code, maintenance status, and expected files modified before using it.

---

# 6. Method B — Manual Extraction

If an automated tool cannot correctly detect your Windows installation or Bluetooth device, use the manual method.

This method gives you direct control over the Windows registry data and Linux BlueZ configuration.

---

# 7. Mount the Windows Partition

First, make sure the Windows system partition is mounted.

You can check mounted filesystems with:

```bash
findmnt
```

or:

```bash
lsblk -f
```

You can also check common mount locations:

```bash
ls /run/media/$USER/
```

If you mounted the Windows partition using your file manager, locate its mount point.

For example:

```text
/mnt/windows
```

or:

```text
/run/media/<username>/Windows
```

The Windows registry hive we need is:

```text
Windows/System32/config/SYSTEM
```

---

# 8. Open the Windows SYSTEM Registry Hive

Navigate to the Windows registry directory.

For example:

```bash
cd /path/to/mounted/Windows/Windows/System32/config
```

Then open the `SYSTEM` hive:

```bash
sudo chntpw -e SYSTEM
```

You should now be inside the `chntpw` registry editor.

> **Important:** The exact `chntpw` commands available can vary by version. The important task is to navigate to the Bluetooth `BTHPORT` key and identify the value corresponding to your Bluetooth device.

---

# 9. Locate the Bluetooth Adapter

The PC Bluetooth adapter is:

```text
90:08:68:12:83:1c
```

Windows represents the MAC without colons:

```text
90086812831c
```

The Bluetooth registry path is generally under:

```text
ControlSet001\Services\BTHPORT\Parameters\Keys\
```

For this example:

```text
ControlSet001\Services\BTHPORT\Parameters\Keys\90086812831c
```

Inside that location, the target device:

```text
9a:b1:7a:4f:97:8d
```

is represented as:

```text
9ab17a4f978d
```

So the relevant location is:

```text
ControlSet001\Services\BTHPORT\Parameters\Keys\90086812831c
```

with the value corresponding to:

```text
9ab17a4f978d
```

---

# 10. Extract the Windows Bluetooth Key

In the registry editor, inspect the value corresponding to:

```text
9ab17a4f978d
```

The raw data obtained for the example device is:

```text
28 D1 C4 99 18 90 09 A6 8E 84 C5 C3 6D 2A F0 DA
```

Your value will normally be different.

Record the bytes exactly as Windows reports them.

---

# 11. Convert the Windows Key

The Windows representation must be reversed at the **byte level** before being written to the Linux BlueZ `Key=` field.

### Windows raw value

```text
28 D1 C4 99 18 90 09 A6 8E 84 C5 C3 6D 2A F0 DA
```

### Reverse the byte order

```text
DA F0 2A 6D C3 C5 84 8E A6 09 90 18 99 C4 D1 28
```

### Remove spaces and convert to lowercase

```text
daf02a6dc3c5848ea609901899c4d128
```

Therefore:

```text
Windows:
28 D1 C4 99 18 90 09 A6 8E 84 C5 C3 6D 2A F0 DA

Linux:
daf02a6dc3c5848ea609901899c4d128
```

### Important

The operation is performed on **bytes**, not individual hexadecimal characters.

Correct:

```text
28 D1 C4 → C4 D1 28
```

Incorrect:

```text
28 D1 C4 → 82 1D 4C
```

---

# 12. Locate the Linux Bluetooth Device

BlueZ normally stores Bluetooth pairing information under:

```bash
/var/lib/bluetooth/
```

List the Bluetooth adapters:

```bash
sudo ls -la /var/lib/bluetooth/
```

For this example, the adapter directory is:

```text
90:08:68:12:83:1c
```

List its contents:

```bash
sudo ls -la /var/lib/bluetooth/90:08:68:12:83:1c/
```

The target device should appear as:

```text
9a:b1:7a:4f:97:8d
```

Check it:

```bash
sudo ls -la /var/lib/bluetooth/90:08:68:12:83:1c/9a:b1:7a:4f:97:8d/
```

The relevant file is:

```text
info
```

Full path:

```text
/var/lib/bluetooth/90:08:68:12:83:1c/9a:b1:7a:4f:97:8d/info
```

---

# 13. Stop Bluetooth Before Editing

Stop `bluetoothd` before modifying its database:

```bash
sudo systemctl stop bluetooth
```

Verify:

```bash
systemctl status bluetooth
```

The service should be stopped.

---

# 14. Edit the BlueZ `info` File

Open the file:

```bash
sudo nano /var/lib/bluetooth/90:08:68:12:83:1c/9a:b1:7a:4f:97:8d/info
```

Find:

```text
[LinkKey]
Key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Replace the key with the converted Windows value:

```text
[LinkKey]
Key=daf02a6dc3c5848ea609901899c4d128
```

Do **not** modify unrelated sections.

Save:

```text
Ctrl+O
Enter
```

Exit:

```text
Ctrl+X
```

---

# 15. Restart Bluetooth

Start Bluetooth again:

```bash
sudo systemctl start bluetooth
```

Or:

```bash
sudo systemctl restart bluetooth
```

Check its status:

```bash
systemctl status bluetooth
```

If it reports:

```text
Active: active (running)
```

the Bluetooth service is running normally.

---

# 16. Verify the Link Key

Check the edited file:

```bash
sudo grep -A2 -B1 '\[LinkKey\]' \
/var/lib/bluetooth/90:08:68:12:83:1c/9a:b1:7a:4f:97:8d/info
```

Expected result:

```text
[LinkKey]
Key=daf02a6dc3c5848ea609901899c4d128
```

You can also inspect the complete file:

```bash
sudo cat /var/lib/bluetooth/90:08:68:12:83:1c/9a:b1:7a:4f:97:8d/info
```

---

# 17. Test the Device

Try connecting to the Bluetooth device.

If using `bluetoothctl`:

```bash
bluetoothctl
```

Then:

```text
power on
agent on
default-agent
connect 9a:b1:7a:4f:97:8d
```

If successful, you should see a connection confirmation.

Exit:

```text
quit
```

You can also inspect the device:

```bash
bluetoothctl info 9a:b1:7a:4f:97:8d
```

---

# 18. Check Bluetooth Logs

If the device does not connect, inspect the Bluetooth service logs:

```bash
sudo journalctl -u bluetooth -b
```

For live troubleshooting:

```bash
sudo journalctl -u bluetooth -f
```

Then attempt to connect the device while the log is running.

Press:

```text
Ctrl+C
```

to stop following the log.

---

# 19. Test Both Operating Systems

After successfully connecting in Linux:

### Linux → Windows

1. Disconnect the device.
2. Shut Linux down completely.
3. Boot Windows.
4. Connect the device.
5. Confirm that it works.
6. Shut Windows down completely.

### Windows → Linux

1. Boot Linux.
2. Connect the same device.
3. Confirm that it works.

The goal is for both operating systems to reconnect without requiring the device to be removed and paired again.

---

# 20. Bluetooth LE Caveat

The `[LinkKey]` method applies primarily to **Classic Bluetooth**.

BLE devices may use additional bonding information such as:

```text
LTK
IRK
EDIV
RAND
```

Examples include many:

* modern wireless keyboards
* mice
* game controllers
* earbuds
* smart devices

For these devices, changing only:

```text
[LinkKey]
Key=...
```

may not be sufficient.

If a BLE device still fails after synchronizing the Classic Bluetooth key, inspect the Windows registry for its BLE bonding information and the corresponding BlueZ device data.

Do not assume that every Bluetooth device can be synchronized by copying one 16-byte Link Key.

---

# 21. Important Pairing Behavior

Once the pairing information is synchronized, avoid unnecessarily selecting:

```text
Remove Device
```

or:

```text
Forget Device
```

in either operating system.

Re-pairing can generate new bonding information and cause Windows and Linux to become out of sync again.

The key normally remains valid until the pairing/bond is removed, replaced, or otherwise invalidated.

---

# 22. Troubleshooting

## Device directory does not exist

Check:

```bash
sudo ls -la /var/lib/bluetooth/
```

Then:

```bash
sudo ls -la /var/lib/bluetooth/90:08:68:12:83:1c/
```

If the device directory is missing, Linux may no longer have a stored pairing for the device.

---

## No `[LinkKey]` section

Check the device type.

It may be:

* BLE-only;
* using a different bonding mechanism;
* not currently paired in Linux;
* storing its credentials differently.

Do not create a random Link Key manually.

---

## Bluetooth service will not start

Check:

```bash
systemctl status bluetooth
```

Then:

```bash
sudo journalctl -u bluetooth -b
```

If necessary, restore the backup.

---

# 23. Restore the Backup

If you need to revert the Linux Bluetooth database:

First stop Bluetooth:

```bash
sudo systemctl stop bluetooth
```

Remove the current database:

```bash
sudo rm -rf /var/lib/bluetooth
```

Restore the backup:

```bash
sudo cp -a /var/lib/bluetooth.backup /var/lib/bluetooth
```

Start Bluetooth:

```bash
sudo systemctl start bluetooth
```

Verify:

```bash
systemctl status bluetooth
```

> Restoring the backup also removes any legitimate Bluetooth changes made after the backup was created.

---

# 24. Quick Reference — Example

### Adapter

```text
90:08:68:12:83:1c
```

### Target device

```text
9a:b1:7a:4f:97:8d
```

### Windows adapter representation

```text
90086812831c
```

### Windows device representation

```text
9ab17a4f978d
```

### Raw Windows key

```text
28 D1 C4 99 18 90 09 A6 8E 84 C5 C3 6D 2A F0 DA
```

### Reversed bytes

```text
DA F0 2A 6D C3 C5 84 8E A6 09 90 18 99 C4 D1 28
```

### Linux key

```text
daf02a6dc3c5848ea609901899c4d128
```

### Linux configuration file

```text
/var/lib/bluetooth/90:08:68:12:83:1c/9a:b1:7a:4f:97:8d/info
```

### Required section

```text
[LinkKey]
Key=daf02a6dc3c5848ea609901899c4d128
```

---

# 25. Complete Manual Command Sequence

For the example setup, the Linux-side workflow can be summarized as:

```bash
# 1. Back up BlueZ configuration
sudo cp -a /var/lib/bluetooth /var/lib/bluetooth.backup

# 2. Inspect Bluetooth adapters
sudo ls -la /var/lib/bluetooth/

# 3. Inspect devices belonging to the adapter
sudo ls -la /var/lib/bluetooth/90:08:68:12:83:1c/

# 4. Stop Bluetooth
sudo systemctl stop bluetooth

# 5. Edit the target device configuration
sudo nano /var/lib/bluetooth/90:08:68:12:83:1c/9a:b1:7a:4f:97:8d/info

# 6. Start Bluetooth
sudo systemctl start bluetooth

# 7. Verify the service
systemctl status bluetooth

# 8. Verify the Link Key
sudo grep -A2 -B1 '\[LinkKey\]' \
/var/lib/bluetooth/90:08:68:12:83:1c/9a:b1:7a:4f:97:8d/info

# 9. Open bluetoothctl
bluetoothctl
```

Inside `bluetoothctl`:

```text
power on
agent on
default-agent
connect 9a:b1:7a:4f:97:8d
info 9a:b1:7a:4f:97:8d
quit
```

---

# 26. Final Workflow

```text
┌──────────────────────────────┐
│ Pair device in Linux         │
└──────────────┬───────────────┘
               ↓
        Complete shutdown
               ↓
┌──────────────────────────────┐
│ Pair device in Windows       │
└──────────────┬───────────────┘
               ↓
        Complete shutdown
               ↓
┌──────────────────────────────┐
│ Boot Linux                   │
└──────────────┬───────────────┘
               ↓
      Back up BlueZ database
               ↓
┌──────────────────────────────┐
│ Extract Windows Link Key     │
│ from SYSTEM registry hive    │
└──────────────┬───────────────┘
               ↓
      Reverse 16-byte value
               ↓
┌──────────────────────────────┐
│ Update BlueZ [LinkKey]       │
└──────────────┬───────────────┘
               ↓
       Restart Bluetooth
               ↓
       Test with bluetoothctl
               ↓
       Test Windows ↔ Linux
```

## Key Principle

The important part is not simply copying a hexadecimal string from Windows to Linux.

The workflow is:

```text
Windows registry
      ↓
Extract pairing bytes
      ↓
Reverse byte order
      ↓
Remove spaces / lowercase
      ↓
BlueZ [LinkKey]
      ↓
Restart bluetoothd
      ↓
Test both operating systems
```

For Classic Bluetooth devices, this can allow Windows and Linux to share the same pairing credential instead of repeatedly overwriting each other's pairing state.
