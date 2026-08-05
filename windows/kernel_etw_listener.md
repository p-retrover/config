# USB Opened File Auto-Copier (Kernel ETW Listener)

A native Windows background monitoring setup using **Event Tracing for Windows (ETW)** and the `Microsoft-Windows-Kernel-File` provider to silently log and copy files opened from monitored USB drives (`D:`, `E:`, `F:`, etc.) to a destination folder.

This setup hooks directly into kernel I/O request packets (`IRP_MJ_CREATE`), catching files opened via **already-running applications**, **`File > Open` dialogs**, **drag-and-drop actions**, and **UWP applications** without requiring drive SACLs or security log configuration.

---

## Directory Layout

Place all files together in your script folder:

```text
C:\Scripts\ (or any folder)
├── run_monitor.bat        # Self-elevating background launcher
├── etw_usb_monitor.ps1    # Production ETW Kernel trace listener
├── stop.bat               # Self-elevating stop script
├── usb_monitor.log        # Automatically generated execution log
└── CopiedFiles\           # Base destination folder for copied files
    ├── Drive_D\           # Drive-isolated subfolders
    ├── Drive_E\
    └── ...

```

---

## Prerequisites

Run this once in an elevated PowerShell terminal to install the official Microsoft `TraceEvent` library:

```powershell
Install-Package -Name "Microsoft.Diagnostics.Tracing.TraceEvent" -Source "nuget.org" -Scope CurrentUser -Force

```

---

## 1. `run_monitor.bat` (Self-Elevating Background Launcher)

Requests Administrator privileges via UAC if required, launches PowerShell invisibly in the background, and detaches immediately.

```bat
@echo off
:: Self-elevate to Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

:: Launch detached background process
start "" powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -NoProfile -File "%~dp0etw_usb_monitor.ps1"

```

---

## 2. `etw_usb_monitor.ps1` (Production ETW Kernel Listener)

```powershell
param(
    [string]$TraceEventDllPath
)

# --- INTERNAL TRANSCRIPT LOGGING ---
$logPath = Join-Path -Path$PSScriptRoot -ChildPath "usb_monitor.log"
Start-Transcript -Path $logPath -Append -Force | Out-Null

# --- WIN32 API FOR DOS DEVICE MAPPING ---
$win32Api = @'
using System;
using System.Text;
using System.Runtime.InteropServices;

public class NativeMethods {
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern uint QueryDosDevice(string lpDeviceName, StringBuilder lpTargetPath, uint ucchMax);
}
'@
Add-Type -TypeDefinition $win32Api -ErrorAction SilentlyContinue

function Get-DosDeviceMap {
    $map = @{}
    Get-CimInstance Win32_Volume | Where-Object { $_.DriveLetter } \vert{} ForEach-Object {$drive = $_.DriveLetter.TrimEnd(':')$sb = New-Object System.Text.StringBuilder 512
        $res = [NativeMethods]::QueryDosDevice($drive, $sb,$sb.Capacity)
        if ($res -gt 0) {
            $devicePath =$sb.ToString().Trim().Split("`0")[0].ToLower()
            $map[$devicePath] = $_.DriveLetter
        }
    }
    return $map
}

# --- ASSEMBLY RESOLUTION ---
if (-not $TraceEventDllPath) {
    $searchPaths = @(
        "$env:LOCALAPPDATA\PackageManagement\NuGet\Packages",
        "$PSScriptRoot\lib",
        "$env:USERPROFILE\.nuget\packages"
    )
    $pkg = Get-ChildItem -Path $searchPaths -Filter "Microsoft.Diagnostics.Tracing.TraceEvent.dll" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($pkg) { $TraceEventDllPath = $pkg.FullName }
}

if (-not ($TraceEventDllPath -and (Test-Path $TraceEventDllPath))) {
    Write-Error "TraceEvent.dll not found. Specify -TraceEventDllPath or run: Install-Package Microsoft.Diagnostics.Tracing.TraceEvent"
    Stop-Transcript
    exit
}
Add-Type -Path $TraceEventDllPath

# --- CONFIGURATION & CACHE STATE ---
$targetDrives = @("D:", "E:", "F:", "G:", "H:", "I:", "J:")
$baseDestination = "C:\CopiedFiles"
$global:copyCache = @{} # Deduplication cache: [path] = DateTime
$cacheTimeoutSeconds = 15
$global:volumeMap = Get-DosDeviceMap

# --- DYNAMIC DEVICE RESOLUTION WITH HOT-PLUG FALLBACK ---
function Resolve-KernelDevicePath {
    param([string]$RawPath)

    if ([string]::IsNullOrWhiteSpace($RawPath)) { return $null }
    $rawLower = $RawPath.ToLower()

    # Attempt 1: Resolve against current volume map
    foreach ($devPath in $global:volumeMap.Keys) {
        if ($rawLower.StartsWith($devPath)) {
            $driveLetter = $global:volumeMap[$devPath]
            return "$driveLetter$($RawPath.Substring($devPath.Length))"
        }
    }

    # Attempt 2: Refresh volume map for newly inserted USB drives (Cache Miss)
    $global:volumeMap = Get-DosDeviceMap
    foreach ($devPath in $global:volumeMap.Keys) {
        if ($rawLower.StartsWith($devPath)) {
            $driveLetter = $global:volumeMap[$devPath]
            return "$driveLetter$($RawPath.Substring($devPath.Length))"
        }
    }

    return $RawPath
}

# --- STREAM-SAFE COPY HELPER WITH RETRIES & GUARANTEED DISPOSAL ---
function Copy-FileWithRetry {
    param(
        [string]$Source,
        [string]$Destination,
        [int]$MaxRetries = 5,
        [int]$DelayMs = 400
    )

    $destDir = Split-Path -Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    # Delay briefly for file write stabilization
    Start-Sleep -Milliseconds 150

    for ($i = 0; $i -lt $MaxRetries; $i++) {
        try {
            Copy-Item -Path $Source -Destination $Destination -Force -ErrorAction Stop
            return $true
        }
        catch {
            $srcStream = $null
            $destStream = $null
            try {
                # Fallback read-stream copy using permissive FileShare flags
                $srcStream = [System.IO.File]::Open($Source, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite -bor [System.IO.FileShare]::Delete)
                $destStream = [System.IO.File]::Create($Destination)
                $srcStream.CopyTo($destStream)
                return $true
            }
            catch {
                Start-Sleep -Milliseconds $DelayMs
            }
            finally {
                # Guaranteed handle cleanup to prevent resource leaks
                if ($null -ne $srcStream) { $srcStream.Dispose() }
                if ($null -ne $destStream) { $destStream.Dispose() }
            }
        }
    }
    return $false
}

# --- ETW SESSION INITIALIZATION ---
$sessionName = "UsbEtwKernelMonitor"

# Force cleanup of any orphan session using logman CLI
& logman stop $sessionName -ets 2>$null | Out-Null

$session = [Microsoft.Diagnostics.Tracing.Session.TraceEventSession]::new($sessionName)

# Robust version-agnostic Keyword Enum Resolution
$keywordsType = [Microsoft.Diagnostics.Tracing.Parsers.KernelTraceEventParser].GetNestedType("Keywords")
if ($null -ne $keywordsType) {
    $fileIoKeyword = [Enum]::Parse($keywordsType, "FileIO")
    $session.EnableKernelProvider($fileIoKeyword)
} else {
    # Fallback for older TraceEvent assemblies
    $session.EnableKernelProvider([Microsoft.Diagnostics.Tracing.Parsers.KernelTraceEventParserKeywords]::FileIO)
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " ETW Kernel Trace Monitor Active" -ForegroundColor Cyan
Write-Host " Monitored Drives: $($targetDrives -join ', ')" -ForegroundColor Cyan
Write-Host " Base Destination: $baseDestination" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# --- EVENT HANDLER SUBSCRIPTION ---
$parser = $session.Source.Kernel

# Generic delegate wrapper supporting version variations in FileIOCreate signatures
$action = [Action[Microsoft.Diagnostics.Tracing.Parsers.KernelTraceEventParser+FileIOCreateTraceData]]{
    param($data)

    try {
        $rawPath = $data.FileName
        if ([string]::IsNullOrWhiteSpace($rawPath)) { return }

        $resolvedPath = Resolve-KernelDevicePath -RawPath $rawPath
        if (-not $resolvedPath) { return }

        # Check drive match
        $matchedDrive = $targetDrives | Where-Object { $resolvedPath.StartsWith($_, [StringComparison]::OrdinalIgnoreCase) }

        if ($matchedDrive) {
            $now = Get-Date

            # Cache pruning & deduplication check
            if ($global:copyCache.ContainsKey($resolvedPath)) {
                if (($now - $global:copyCache[$resolvedPath]).TotalSeconds -lt $cacheTimeoutSeconds) {
                    return
                }
            }

            # Periodic cache garbage collection (prevents memory leak)
            if ($global:copyCache.Count -gt 100) {
                $expiredKeys = $global:copyCache.Keys | Where-Object { ($now - $global:copyCache[$_]).TotalSeconds -ge $cacheTimeoutSeconds }
                foreach ($key in $expiredKeys) { $global:copyCache.Remove($key) }
            }

            # Verify target exists and is a file
            if ((Test-Path -Path $resolvedPath) -and (-not (Test-Path -Path $resolvedPath -PathType Container))) {
                $global:copyCache[$resolvedPath] = $now

                # Prevent name collisions by placing files in drive-specific subfolders
                $driveSubfolder = "Drive_" + $matchedDrive.TrimEnd(':')
                $relativeFilePath = $resolvedPath.Substring($matchedDrive.Length).TrimStart('\', '/')
                $destFilePath = Join-Path -Path (Join-Path -Path $baseDestination -ChildPath $driveSubfolder) -ChildPath $relativeFilePath

                Write-Host "[KERNEL EVENT] File Access: $resolvedPath" -ForegroundColor Yellow

                if (Copy-FileWithRetry -Source $resolvedPath -Destination $destFilePath) {
                    Write-Host "[SUCCESS] Copied to $destFilePath`n" -ForegroundColor Green
                } else {
                    Write-Warning "[LOCK ERROR] Could not copy $resolvedPath (File in use or restricted)."
                }
            }
        }
    }
    catch {
        Write-Warning "Callback processing exception: $_"
    }
}

# Attach to typed Kernel FileIOCreate event
$parser.add_FileIOCreate($action)

try {
    $session.Source.Process()
}
finally {
    Write-Host "Cleaning up ETW Session..." -ForegroundColor Gray
    $session.Stop()$session.Dispose()
    Stop-Transcript | Out-Null
}

```

---

## 3. `stop.bat` (Self-Elevating Stop Script)

Stops the active ETW session via Windows `logman` and safely kills the background monitoring process.

```bat
@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

echo ==================================================
echo Stopping USB ETW Kernel Monitor
echo ==================================================

echo [1/2] Stopping ETW session 'UsbEtwKernelMonitor'...
logman stop UsbEtwKernelMonitor -ets >nul 2>&1

echo [2/2] Terminating background PowerShell process...
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name = 'powershell.exe'\" | Where-Object { $_.CommandLine -like '*etw_usb_monitor.ps1*' } | Invoke-CimMethod -MethodName Terminate | Out-Null"

echo ==================================================
echo SUCCESS: ETW Session stopped and process killed.
echo ==================================================
timeout /t 3 >nul

```

---

## 4. Usage & Operations

### Start the Background Monitor

Double-click `run_monitor.bat` and click **Yes** on the UAC prompt. The process will detach and run invisibly.

### Monitor Output in Real Time

Open a standard PowerShell terminal in the script directory and run:

```powershell
Get-Content -Path ".\usb_monitor.log" -Wait -Tail 20

```

### Stop the Background Process

Double-click `stop.bat` and accept the UAC prompt.

---

## 5. Technical Notes & Mechanics

* **Win32 `QueryDosDevice` P/Invoke:** Converts low-level NT device strings (`\Device\HarddiskVolumeX`) to drive letters (`F:\`).
* **Hot-Plug Re-Indexing:** Automatically refreshes the volume map whenever an unmapped drive path is detected.
* **Lock Safety & File Streams:** Includes a fallback stream copy (`FileShare.ReadWrite`) with retry mechanisms to bypass exclusive file locks held by opening applications.
* **Path Collision Isolation:** Separates saved files into `Drive_D`, `Drive_E`, etc., matching the drive letter to prevent files with identical names from overwriting each other.
* **Bounded Deduplication:** Ignores repeated access events for the same file within 15 seconds and automatically purges old cache keys to prevent memory growth.
