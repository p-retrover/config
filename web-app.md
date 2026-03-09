# Web Apps Reference (Windows & Linux)

A reference for creating **site-specific browser apps (SSB)** or **web apps** on Linux and Windows.
These methods allow websites to behave like standalone applications with their own window, icon, and launcher.

---

# Table of Contents

1. Concepts
2. Linux Methods

   * Chromium App Mode + `.desktop` file
   * Firefox launcher
   * WebApp Manager (Linux Mint)
   * Nativefier
3. Windows Methods

   * Chromium App Mode shortcut
   * Firefox shortcut
   * Nativefier
4. Comparison
5. Maintenance (Updating / Removing)
6. Recommended setups
7. Useful directories

---

# 1. Concepts

A **Web App** or **SSB (Site Specific Browser)** is a launcher that:

* Opens a website in its own window
* Optionally removes browser UI
* Has its own icon
* Appears in system menus or launchers

Common features:

* Dedicated storage/profile
* Standalone window
* Desktop / Start Menu launcher
* Optional sandboxing

---

# 2. Linux Methods

## 2.1 Chromium App Mode + `.desktop` File

Works with:

* Chromium
* Google Chrome
* Brave
* Ungoogled Chromium
* Vivaldi

Command:

```
chromium --app=https://example.com
```

Example desktop entry:

File location:

```
~/.local/share/applications/example.desktop
```

Contents:

```
[Desktop Entry]
Name=Example App
Exec=chromium --app=https://example.com
Terminal=false
Type=Application
Icon=example
Categories=Network;
```

Optional isolated storage:

```
Exec=chromium --app=https://example.com --user-data-dir=$HOME/.local/share/webapps/example
```

Benefits:

* Lightweight
* Native desktop integration
* Easy to maintain
* No extra dependencies

---

## 2.2 Firefox Launcher (.desktop)

Firefox does **not support true app mode**, but kiosk mode can approximate it.

Command:

```
firefox --kiosk https://example.com
```

Desktop entry:

```
[Desktop Entry]
Name=Example App
Exec=firefox --kiosk https://example.com
Terminal=false
Type=Application
Icon=example
Categories=Network;
```

Optional dedicated profile:

```
firefox -P example https://example.com
```

Create profile manager:

```
firefox -P
```

Limitations:

* No real site-specific browser mode
* UI control is limited

---

## 2.3 WebApp Manager (Linux Mint)

Open-source GUI tool that creates web apps automatically.

Repository:

[https://github.com/linuxmint/webapp-manager](https://github.com/linuxmint/webapp-manager)

Install:

```
sudo apt install webapp-manager
```

Features:

* Graphical interface
* Supports Chromium and Firefox
* Automatically creates desktop entries
* Isolated browser profiles
* Integrated icons

Launchers are created in:

```
~/.local/share/applications
```

---

## 2.4 Nativefier (Electron Wrapper)

Nativefier packages websites as **standalone Electron applications**.

Repository:

[https://github.com/nativefier/nativefier](https://github.com/nativefier/nativefier)

Install:

```
npm install -g nativefier
```

Create app:

```
nativefier https://example.com
```

Optional flags:

```
nativefier https://example.com \
  --name "ExampleApp" \
  --icon icon.png
```

Output example:

```
ExampleApp-linux-x64/
ExampleApp
resources/
```

Advantages:

* Works offline once packaged
* Fully standalone
* Same behavior across OS

Disadvantages:

* Larger applications (Electron runtime)
* Uses Chromium engine internally

---

# 3. Windows Methods

## 3.1 Chromium App Mode Shortcut (Recommended)

Works with:

* Chromium
* Chrome
* Brave
* Edge

Command:

```
chrome.exe --app="https://example.com"
```

Example shortcut target:

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --app="https://example.com"
```

Optional dedicated storage:

```
--user-data-dir="%LOCALAPPDATA%\WebApps\example"
```

Full example:

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --app="https://example.com" --user-data-dir="%LOCALAPPDATA%\WebApps\example"
```

To integrate with the Start Menu place the shortcut in:

```
%APPDATA%\Microsoft\Windows\Start Menu\Programs
```

Advantages:

* Lightweight
* Uses installed browser
* Easy to maintain

---

## 3.2 Firefox Shortcut

Firefox has **no official web-app mode**, but kiosk mode can approximate one.

Command:

```
firefox.exe --kiosk https://example.com
```

Example shortcut target:

```
"C:\Program Files\Mozilla Firefox\firefox.exe" --kiosk https://example.com
```

Optional dedicated profile:

```
firefox.exe -P example --kiosk https://example.com
```

Create profiles:

```
firefox.exe -P
```

Limitations:

* No standalone window UI
* Kiosk removes most controls

---

## 3.3 Nativefier (Cross-Platform)

Nativefier works the same on Windows and Linux.

Install:

```
npm install -g nativefier
```

Create application:

```
nativefier https://example.com
```

Example output:

```
ExampleApp-win32-x64/
ExampleApp.exe
resources/
```

Run with:

```
ExampleApp.exe
```

Uninstall:

Delete the application folder.

---

# 4. Comparison

| Method            | Engine              | Platform        | Isolation | Notes           |
| ----------------- | ------------------- | --------------- | --------- | --------------- |
| Chromium App Mode | Chromium            | Linux / Windows | Optional  | Lightweight     |
| Firefox kiosk     | Gecko               | Linux / Windows | Optional  | Limited UI      |
| WebApp Manager    | Chromium / Firefox  | Linux           | Automatic | GUI             |
| Nativefier        | Chromium (Electron) | Linux / Windows | Built-in  | Standalone apps |

---

# 5. Maintenance

## Removing apps

Chromium shortcut:

Delete the shortcut and optional data directory.

Nativefier:

Delete the generated application folder.

Linux desktop entry:

Remove:

```
~/.local/share/applications/example.desktop
```

Optional storage:

```
~/.local/share/webapps/example
```

---

## Updating Nativefier apps

Rebuild the application:

```
nativefier https://example.com
```

Replace the previous folder with the new build.

---

# 6. Recommended Setup

### Linux

Best lightweight approach:

Chromium app mode + desktop file

Best GUI solution:

WebApp Manager

---

### Windows

Best open solution:

Chromium app-mode shortcut

Best standalone apps:

Nativefier

---

# 7. Useful Directories

Linux

```
~/.local/share/applications
~/.local/share/webapps
```

Windows

```
%APPDATA%\Microsoft\Windows\Start Menu\Programs
%LOCALAPPDATA%\WebApps
```

---
