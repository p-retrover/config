# USB Opened File Auto-Copier (Windows Native)

A lightweight, native Windows solution to automatically detect and copy files from a target USB drive the moment they are opened by any application.

---

## 1. Architecture Overview

* **Detection Mechanism:** Windows WMI Event Watcher (`Win32_Process` creation).
* **Target Isolation:** Uses regex targeting files strictly on drive `F:\` (`F:\...`).
* **Execution Mode:** Runs invisibly in the background via a VBScript wrapper.
* **Destination Path:** `C:\CopiedFiles`

---

## 2. File 1: `usb_monitor.ps1`

Save the following code as `C:\Scripts\usb_monitor.ps1`:

```powershell
# --- CONFIGURATION ---
$usbLetter = "F:"                     # Target USB drive letter
$destinationFolder = "C:\CopiedFiles"  # Destination directory

# Create destination folder if missing
if (-not (Test-Path $destinationFolder)) {
    New-Item -ItemType Directory -Path $destinationFolder | Out-Null
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " Active Monitoring on Drive $usbLetter" -ForegroundColor Cyan
Write-Host " Saving copies to: $destinationFolder" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Create WMI Event Watcher for new processes
$query = "SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_Process'"
$watcher = New-Object System.Management.ManagementEventWatcher($query)

# Target ONLY paths that start with the USB drive letter (e.g., F:\...)
$escapedLetter = [regex]::Escape($usbLetter)
$pattern = "$escapedLetter\\[^`"]+\.[a-zA-Z0-9]+"

try {
    while ($true) {
        $eventParam = $watcher.WaitForNextEvent()
        $cmdLine = $eventParam.TargetInstance.CommandLine

        if ($cmdLine -and $cmdLine -match $pattern) {
            # Extract the exact USB file path
            $filePath = $matches[0].Trim().Trim('"')

            # Verify path exists and is a file (not a folder or C: binary)
            if ((Test-Path $filePath) -and (-not (Test-Path -Path $filePath -PathType Container))) {
                Write-Host "[MATCH FOUND] File opened: $filePath" -ForegroundColor Yellow
                Copy-Item -Path $filePath -Destination $destinationFolder -Force
                Write-Host "[SUCCESS] Copied to $destinationFolder`n" -ForegroundColor Green
            }
        }
    }
}
finally {
    $watcher.Stop()$watcher.Dispose()
}

```

---

## 3. File 2: `run_usb_monitor.vbs` (Silent Launcher)

Save the following code as `C:\Scripts\run_usb_monitor.vbs` to execute the PowerShell script silently without opening a terminal window:

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Scripts\usb_monitor.ps1""", 0, False

```

---

## 4. Usage & Execution

### Start the Background Process

Double-click `run_usb_monitor.vbs`. The script will immediately begin monitoring drive `F:` in the background.

### Stop the Background Process

Run this command in PowerShell to locate and terminate the background instance:

```powershell
Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" | Where-Object { $_.CommandLine -like "*usb_monitor.ps1*" } | Invoke-CimMethod -MethodName Terminate

```

Alternatively, open **Task Manager** (`Ctrl + Shift + Esc`) and terminate the relevant `powershell.exe` background process.

---

## 5. Notes & Technical Limitations

1. **Win32 Applications:** Works with native desktop software (e.g., MS Paint, Notepad, Acrobat Reader, MS Office, Photoshop, VLC).
2. **UWP Apps:** Universal Windows Platform apps (like the default Windows Photos app) route launches through `ApplicationFrameHost.exe` without passing command-line arguments. To capture images, set the default image viewer to a traditional app (e.g., Paint).
3. **Trigger Event:** Triggers on application launch containing the target file path. Opening files within an already open application via `File > Open` is not captured by process creation monitoring.
