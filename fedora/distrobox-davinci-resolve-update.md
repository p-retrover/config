# Guide: Updating DaVinci Resolve on Fedora (via DavinciBox)

This guide walks you through manually updating DaVinci Resolve when the internal application updater fails, bypassing package dependency checks, and resolving common library conflicts.

---

## Prerequisites
* **Do not** use the built-in "Install" or "Download" buttons inside DaVinci Resolve. They do not work on Linux.
* Download the official Linux update archive (`.zip`) directly from the [Blackmagic Design Support Page](https://blackmagicdesign.com).
* Extract the archive to your **Downloads** directory to get the updated `.run` installer file.

---

## Step 1: Open Terminal and Enter DavinciBox
Open your terminal on your Fedora host machine, navigate to your downloads directory, and log into your container environment:

```bash
cd ~/Downloads
distrobox enter davincibox
```

---

## Step 2: Run the Installer (Bypassing the Zlib Check)
The installer script looks for an obsolete package naming convention (`zlib`), causing a false-positive failure on modern container bases. 

Because `sudo` strips out user environment flags by default, you must pass the bypass argument **after** the sudo command or use the built-in force flag. 

Run **either** of the following commands to launch the installer:

### Option A (Recommended)
```bash
sudo SKIP_PACKAGE_CHECK=1 ./DaVinci_Resolve_21.0_Linux.run
```

### Option B (Alternative)
```bash
sudo ./DaVinci_Resolve_21.0_Linux.run --force
```

Follow the graphical installation wizard instructions to complete the software upgrade.

---

## Step 3: Clean Up Conflicts (If App Fails to Open)
Many modern distributions use host libraries that conflict with older, proprietary libraries bundled inside DaVinci Resolve. If the app crashes immediately upon launching from your application menu, you must isolate the bundled dependencies.

While still inside your `davincibox` terminal, execute the following commands to move the conflicting files out of the application's runtime path:

```bash
# Navigate to the Resolve internal libraries folder
cd /opt/resolve/libs

# Create a backup folder for old files
sudo mkdir -p disabled-libraries

# Move conflicting GLib/GIO bundles
sudo mv libglib* disabled-libraries/
sudo mv libgio* disabled-libraries/
sudo mv libgmodule* disabled-libraries/
sudo mv libgobject* disabled-libraries/
```

This forces DaVinci Resolve to cleanly fall back on the container's modern, system-wide system libraries.

---

## Step 4: Verify Installation
Exit your container and launch DaVinci Resolve from your application dashboard. Your existing databases and project timelines will be preserved automatically.
