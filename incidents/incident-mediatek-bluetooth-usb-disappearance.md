# Incident: MediaTek Bluetooth USB Controller Disappears

**System:** HP Pavilion x360 14-dy1xxx  
**OS:** Fedora 45  
**Kernel observed:** `7.3.4-300.fc45.x86_64`  
**Date observed:** 2026-11-21  
**Status:** Diagnosed to the Bluetooth USB device / enumeration path; root cause not yet established

## Summary

The internal MediaTek Bluetooth controller (`13d3:3567`, reported as `Wireless_Device`) initially enumerates on USB bus 3, port 10, and the Bluetooth HCI controller (`hci0`) starts successfully. During a later suspend-related operation, HCI commands begin timing out. The kernel then fails to communicate with the USB device and repeatedly fails to re-enumerate it.

After the failures, the Bluetooth USB device is absent from the USB device tree, `/sys/class/bluetooth/` contains no controller, `rfkill` lists only WLAN, and `bluetoothctl list` returns no controller. The Bluetooth service itself remains running, but there is no hardware controller for it to manage.

The available evidence localizes the immediate failure to the MediaTek Bluetooth USB function or its USB communication path. It does **not** yet establish whether the underlying cause is device firmware, power management, the USB host-controller interaction, a kernel regression, or hardware.

## Hardware and topology

- Wi-Fi adapter: MediaTek MT7921, PCI ID `14c3:7961`, using `mt7921e`.
- Bluetooth function: MediaTek USB device, USB ID `13d3:3567`, product string `Wireless_Device`.
- Bluetooth USB path when enumerated: `3-10`.
- USB host controller for bus 3: Intel xHCI, PCI address `0000:00:14.0`.
- Other devices on bus 3 observed working:
  - HP Wide Vision camera, `05c8:03df`, path `3-4`.
  - ELAN input controller, `04f3:0c00`, path `3-5`.

The Wi-Fi function is PCIe and remains operational. Bluetooth is a separate USB function of the combo wireless card; a working Wi-Fi interface does not imply that the Bluetooth USB function is healthy.

## Relevant observations

### Initial enumeration

At approximately `06:34:34`, the kernel detected the MediaTek USB device:

```text
usb 3-10: new high-speed USB device
idVendor=13d3, idProduct=3567
Product: Wireless_Device
Manufacturer: MediaTek Inc.
```

The `btusb` driver registered and the Bluetooth HCI controller initialized. `hci0` setup completed at approximately `06:34:42`.

### Failure during suspend-related activity

At approximately `06:38:42`, the kernel logged:

```text
Bluetooth: hci0: Opcode 0x0c1a failed: -110
Bluetooth: hci0: command 0x0c1a tx timeout
Bluetooth: hci0: Failed to read uhw reg(-113)
```

The kernel then attempted to reset the USB device:

```text
Bluetooth: hci0: last usb reset failed? Resetting again
usb 3-10: reset high-speed USB device number 4 using xhci_hcd
usb 3-10: device descriptor read/64, error -110
```

Further attempts produced repeated descriptor-read timeouts and host-controller setup-command timeouts:

```text
usb 3-10: device descriptor read/64, error -110
xhci_hcd ...: Timeout while waiting for setup device command
usb 3-10: device not accepting address ... error -62
```

The device was subsequently disconnected and repeated re-enumeration attempts failed.

### State after failure

Checks performed after the failure showed:

- `/sys/class/bluetooth/` had no `hci0`.
- `readlink -f /sys/class/bluetooth/hci0/device` returned no path.
- `bluetoothctl list` returned no controller.
- `rfkill list` showed WLAN only, with no Bluetooth radio.
- `lsusb` and `lsusb -t` no longer showed `13d3:3567`.
- `/sys/bus/usb/devices/` contained the camera (`3-4`) and ELAN device (`3-5`), but not `3-10`.
- The `btusb` driver directory existed, but no Bluetooth USB device was bound to it.
- `bluetooth.service` remained active. This only confirms that the daemon is running; it does not confirm that a Bluetooth controller is present.

The camera and ELAN device remained visible on the same USB bus. Therefore, the evidence does not indicate that the entire USB host controller or bus had stopped functioning.

## Interpretation and error codes

| Log value | Meaning | Interpretation in this incident |
|---|---|---|
| `-110` | `ETIMEDOUT` | HCI command or USB communication timed out. |
| `-113` | `EHOSTUNREACH` | The Bluetooth driver could not reach/read the device register. |
| `-62` | `ETIME` / communication timeout-related error | USB device setup/addressing failed. |

The sequence is significant: the Bluetooth HCI controller first becomes unresponsive, then USB reset and descriptor requests fail, and finally the device disappears from the USB device tree.

The xHCI messages show that setup commands for this device are timing out. They do not, by themselves, prove that the xHCI controller is defective. The controller continues to expose other devices on bus 3.

## Suspend timing caveat

One log excerpt included:

```text
PM: suspend devices took 55.477 seconds
WARNING: kernel/power/suspend_test.c:53 at suspend_test_finish...
Component: suspend devices, time: 55477
```

The warning originates from the kernel's suspend-test code. This can occur when `/sys/power/pm_test` is set to a diagnostic stage, such as `devices`. Until the current value of `/sys/power/pm_test` is checked, the 55.477-second figure must **not** be treated as proof that a normal suspend operation took 55 seconds.

The following value was requested but has not yet been recorded:

```bash
cat /sys/power/pm_test
```

Also record the supported and selected sleep modes:

```bash
cat /sys/power/mem_sleep
cat /sys/power/state
```

Earlier, `/sys/power/mem_sleep` showed:

```text
[s2idle] deep
```

This means `s2idle` was selected at that time. A previous attempt to use `deep` did not resume successfully, but the available logs do not establish why. Do not switch to `deep` again as a presumed fix without a controlled test and supporting evidence.

## Current assessment

**Established by logs and system state:**

1. The MediaTek Bluetooth USB device initially enumerates successfully.
2. The Bluetooth HCI controller initializes.
3. HCI commands subsequently time out and a device-register read fails.
4. USB reset and re-enumeration attempts fail with repeated timeouts.
5. The Bluetooth USB device disappears from the USB device tree.
6. The Wi-Fi PCIe function and other observed USB devices remain available.

**Not established yet:**

- Whether the failure is caused by a MediaTek Bluetooth firmware/initialization problem.
- Whether runtime power management or suspend-time power sequencing contributes.
- Whether this is a regression in the running kernel or its `btusb`/`btmtk` support.
- Whether the USB host-controller interaction or the Bluetooth hardware itself is at fault.
- Whether the 55.477-second suspend-test measurement reflects a diagnostic `pm_test` run rather than a real suspend.

## Next diagnostic checks

Run these checks before changing driver options or kernel parameters.

### 1. Confirm the power-management test stage

```bash
cat /sys/power/pm_test
```

`none` means no suspend test stage is selected. If the value is not `none`, record it before changing anything; determine what enabled the test stage and why.

### 2. Record available sleep states

```bash
cat /sys/power/mem_sleep
cat /sys/power/state
```

### 3. Check whether the Bluetooth USB device currently exists

```bash
if [ -d /sys/bus/usb/devices/3-10 ]; then
    echo "USB device 3-10 exists"
    cat /sys/bus/usb/devices/3-10/{idVendor,idProduct,power/control,power/runtime_status}
else
    echo "USB device 3-10 is absent"
fi
```

Only inspect the device's sysfs attributes when the device directory exists. Do not run `udevadm` against a missing `hci0` path.

### 4. Record xHCI runtime-power state

```bash
for f in /sys/bus/pci/devices/0000:00:14.0/power/{control,runtime_status,runtime_suspended_time,runtime_active_time}; do
    [ -f "$f" ] && printf '%s: ' "$f" && cat "$f"
done
```

### 5. Capture USB topology and device presence

Run when Bluetooth is expected to be available, and again after a failure:

```bash
lsusb
lsusb -t
```

If the controller is absent, preserve the kernel log around the failure:

```bash
sudo journalctl -b -k --no-pager -o short-precise \
  | grep -Ei 'Bluetooth|btusb|btmtk|mt7921|usb 3-10|xhci|suspend|resume'
```

For a previous boot, replace `-b` with the appropriate boot selector, such as `-b -1`.

## Change-control notes

Do not apply multiple speculative changes at once. In particular:

- Do not assume that changing `btusb` module parameters will fix a device that is no longer responding at the USB enumeration level.
- Do not disable USB autosuspend globally without evidence that runtime power management is involved.
- Do not unload or blacklist `btusb`, `btmtk`, or `mt7921e` as a first-line response.
- Do not attribute the failure to the Wi-Fi driver merely because Wi-Fi and Bluetooth share a combo card.
- Do not conclude that the xHCI controller is faulty solely from setup-command timeouts affecting this one device.

After collecting the checks above, useful controlled comparisons would be to test the Bluetooth function after a full shutdown/cold start, and to compare behavior under another known-good kernel or operating system. These comparisons can help distinguish a kernel/firmware regression from a persistent device or platform problem.

## Incident status

**Open — root cause undetermined.**

The immediate failure mode is a loss of communication with the MediaTek Bluetooth USB function, followed by failed USB re-enumeration. The next step is to establish the `pm_test` state and collect the remaining power-management information before making configuration changes.
