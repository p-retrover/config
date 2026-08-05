# USB Opened File Auto-Copier (Windows Native)

A native Windows background monitoring setup that silently logs and copies files opened from a target USB drive (`D:`, `E:`, `F:`, etc.) to a local destination directory using relative paths.

---

## Directory Layout

Put these scripts together in the same directory:

```text
C:\Scripts\ (or any folder)
├── run_monitor.bat    # Detached background launcher (Run as Admin)
├── usb_monitor.ps1    # Core PowerShell WMI monitoring logic
├── usb_monitor.log    # Automatically generated execution log
└── CopiedFiles\       # Automatically generated destination folder

```

---

## 1. `run_monitor.bat` (Silent Detached Launcher)

This batch script launches PowerShell invisibly, detaches the process so the terminal window closes immediately, and redirects all output streams to `usb_monitor.log`.

```bat
@echo off
start "" powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -NoProfile -Command "& '%~dp0usb_monitor.ps1' *> '%~dp0usb_monitor.log'"

```

---

## 2. `usb_monitor.ps1` (Core Listener)

Monitors `Win32_Process` events via WMI, isolates file launches matching target USB drive letters, and copies opened files to the relative `CopiedFiles` folder.

```powershell
# --- CONFIGURATION ---
# Target drive letters to monitor
$targetDrives = @("D:", "E:", "F:", "G:", "H:", "I:", "J:")

$destinationFolder = Join-Path -Path $PSScriptRoot -ChildPath "CopiedFiles"  # Destination directory

# Create destination folder if missing
if (-not (Test-Path $destinationFolder)) {
    New-Item -ItemType Directory -Path $destinationFolder | Out-Null
}

# Construct an OR regex pattern: (D:|E:|F:|G:|H:|I:|J:)
$escapedDrives = $targetDrives | ForEach-Object { [regex]::Escape($_) }
$driveRegex = "(" + ($escapedDrives -join "|") + ")"
$pattern = "$driveRegex\\[^`"]+\.[a-zA-Z0-9]+"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " Active Monitoring on Drives: $($targetDrives -join ', ')" -ForegroundColor Cyan
Write-Host " Saving copies to: $destinationFolder" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Create WMI Event Watcher for process creation
$query = "SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_Process'"
$watcher = New-Object System.Management.ManagementEventWatcher($query)

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
    # Clean up event listener when stopped
    $watcher.Stop()
    $watcher.Dispose()
}

```

---

## 3. Usage & Operations

### Start the Background Monitor

Right-click `run_monitor.bat` $\rightarrow$ **Run as Administrator**. The terminal will pop up briefly and close automatically.

### Monitor Output in Real Time

Open a standard PowerShell terminal in the script directory and run:

```powershell
Get-Content -Path ".\usb_monitor.log" -Wait -Tail 20

```

### Stop the Background Process

To kill the background monitoring script without opening Task Manager:

```powershell
Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" | Where-Object { $_.CommandLine -like "*usb_monitor.ps1*" } | Invoke-CimMethod -MethodName Terminate

```

---

## 4. Technical Notes & Limitations

* **Execution Context:** Requires Administrator privileges to listen to WMI process events.
* **Compatibility:** Works with standard Win32 applications (MS Office, Acrobat, Paint, Notepad, media players, etc.).
* **UWP Apps:** Windows Photos and other UWP apps route launches via `ApplicationFrameHost.exe`. Change the default viewer for image files to Paint or a classic photo viewer if image tracking is needed.
