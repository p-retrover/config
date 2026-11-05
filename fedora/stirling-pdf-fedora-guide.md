# Stirling PDF on Fedora

A practical guide for managing my Stirling PDF installation on Fedora.

## 1. Installation overview

Stirling PDF is installed as a **standalone Java application**, managed
by a user-level `systemd` service. It is **not running in Podman or
Docker**.

  -------------------------------------------------------------------------------------
  Item                                Current configuration
  ----------------------------------- -------------------------------------------------
  Application directory               `/opt/Stirling-PDF/`

  JAR filename                        `Stirling-PDF-with-login.jar`

  Full JAR path                       `/opt/Stirling-PDF/Stirling-PDF-with-login.jar`

  Java executable                     `/usr/bin/java`

  systemd unit                        `~/.config/systemd/user/stirling.service`

  Service name                        `stirling.service`

  Service scope                       User (`systemctl --user`)

  Startup policy                      Enabled; starts with the user's systemd session

  Download location used for updates  `~/Downloads/Stirling-PDF-with-login.jar`
  -------------------------------------------------------------------------------------

The service unit currently contains:

``` ini
[Unit]
Description=Stirling PDF Server

[Service]
ExecStart=/usr/bin/java -jar /opt/Stirling-PDF/Stirling-PDF-with-login.jar
Restart=always

[Install]
WantedBy=default.target
```

The service file is located at:

``` text
~/.config/systemd/user/stirling.service
```

## 2. Accessing Stirling PDF

Open the local web address configured for the application in a browser.

The usual default port is `8080`, so the address is commonly:

``` text
http://localhost:8080
```

If that address does not work, check the application logs and
configuration for the actual listening port.

## 3. Managing the service

All commands below operate on the **user-level** service. Do not use
`sudo` with `systemctl --user`.

### Check status

``` bash
systemctl --user status stirling.service
```

### Start

``` bash
systemctl --user start stirling.service
```

### Stop

``` bash
systemctl --user stop stirling.service
```

### Restart

``` bash
systemctl --user restart stirling.service
```

### Enable automatic startup

``` bash
systemctl --user enable stirling.service
```

### Disable automatic startup

``` bash
systemctl --user disable stirling.service
```

### View recent logs

``` bash
journalctl --user -u stirling.service -n 50 --no-pager
```

Follow logs live:

``` bash
journalctl --user -u stirling.service -f
```

To leave the live log view, press `Ctrl+C`.

## 4. Updating Stirling PDF

The update process is to download the new official JAR, stop the
service, back up the existing installation, replace the JAR, and start
the service again.

### Step 1: Download the new JAR

Download the appropriate **with-login** JAR from the official Stirling
PDF release/download source.

The downloaded file used in this setup is expected at:

``` text
~/Downloads/Stirling-PDF-with-login.jar
```

Check that it exists:

``` bash
ls -lh ~/Downloads/Stirling-PDF-with-login.jar
```

### Step 2: Back up the current installation

Create a timestamped backup of the application directory:

``` bash
mkdir -p ~/backups/stirling-pdf
backup="$HOME/backups/stirling-pdf/$(date +%F-%H%M%S)"
mkdir -p "$backup"
sudo cp -a /opt/Stirling-PDF "$backup/"
```

This preserves the existing installation directory before the JAR is
replaced. Keep backups until the new version has been tested.

### Step 3: Stop the service

``` bash
systemctl --user stop stirling.service
```

### Step 4: Replace the JAR

The service expects the JAR to retain its existing filename:

``` bash
sudo install -o root -g root -m 0644 \
  ~/Downloads/Stirling-PDF-with-login.jar \
  /opt/Stirling-PDF/Stirling-PDF-with-login.jar
```

This replaces the application JAR without changing the systemd unit or
the other files in `/opt/Stirling-PDF/`.

### Step 5: Start the service

``` bash
systemctl --user start stirling.service
```

### Step 6: Verify the update

``` bash
systemctl --user status stirling.service
```

Inspect startup logs:

``` bash
journalctl --user -u stirling.service -n 50 --no-pager
```

Then open Stirling PDF in the browser and verify that: - The web
interface loads. - Login works. - Existing settings and configuration
are present. - The expected features work.

If the new version fails, see [Troubleshooting](#7-troubleshooting).

## 5. Backing up configuration and data

Before an update, back up the complete application directory:

``` bash
mkdir -p ~/backups/stirling-pdf
backup="$HOME/backups/stirling-pdf/$(date +%F-%H%M%S)"
mkdir -p "$backup"
sudo cp -a /opt/Stirling-PDF "$backup/"
```

The application may also use directories outside `/opt/Stirling-PDF`,
depending on its configuration. Check the startup logs and configuration
files to identify any external data paths, mounted directories, or
database locations, and back those up separately.

Do not assume that replacing the JAR also backs up or preserves data
stored elsewhere.

## 6. Inspecting the installation

### Inspect the service definition

``` bash
systemctl --user cat stirling.service
```

### Inspect the service process

``` bash
ps aux | grep -i '[s]tirling'
```

### Inspect the installation directory

``` bash
ls -lah /opt/Stirling-PDF/
```

### Check Java

``` bash
java -version
```

Use a Java version supported by the specific Stirling PDF release being
installed. Requirements can change between releases; consult that
release's official documentation if startup fails after an upgrade.

## 7. Troubleshooting

### Service does not start

Check its status and logs:

``` bash
systemctl --user status stirling.service
journalctl --user -u stirling.service -n 100 --no-pager
```

Common things to check: - The JAR exists at
`/opt/Stirling-PDF/Stirling-PDF-with-login.jar`. - The JAR is a valid
download and is not an HTML error page or incomplete file. - The
installed Java version is compatible with the new release. - The
application can read its configuration and data directories. - The
configured web port is not already in use.

### Check whether the JAR exists

``` bash
ls -lh /opt/Stirling-PDF/Stirling-PDF-with-login.jar
```

### Service is active but the browser cannot connect

Inspect the logs for the listening port and startup errors:

``` bash
journalctl --user -u stirling.service -n 100 --no-pager
```

Check whether a process is listening on the expected port (replace
`8080` if the configured port differs):

``` bash
ss -ltnp | grep ':8080'
```

### Reload systemd after editing the service file

A JAR replacement does not require a systemd daemon reload. If the
service unit itself is edited, run:

``` bash
systemctl --user daemon-reload
systemctl --user restart stirling.service
```

## 8. Useful notes

-   This installation is a Java JAR managed by systemd, not a Podman or
    Docker container.
-   Use `systemctl --user`, not the system-wide `systemctl` service
    commands.
-   A normal JAR update does not require recreating the service.
-   Keep the JAR filename `Stirling-PDF-with-login.jar`, unless you also
    update `ExecStart` in the service file.
-   Back up configuration and data before upgrading, especially before
    major-version upgrades.
-   Do not delete old backups until the updated installation has been
    tested.

## 9. Quick update checklist

``` bash
# 1. Confirm the new JAR is present
ls -lh ~/Downloads/Stirling-PDF-with-login.jar

# 2. Back up the current installation
mkdir -p ~/backups/stirling-pdf
backup="$HOME/backups/stirling-pdf/$(date +%F-%H%M%S)"
mkdir -p "$backup"
sudo cp -a /opt/Stirling-PDF "$backup/"

# 3. Stop Stirling PDF
systemctl --user stop stirling.service

# 4. Install the new JAR at the path expected by systemd
sudo install -o root -g root -m 0644 \
  ~/Downloads/Stirling-PDF-with-login.jar \
  /opt/Stirling-PDF/Stirling-PDF-with-login.jar

# 5. Start Stirling PDF
systemctl --user start stirling.service

# 6. Verify status and logs
systemctl --user status stirling.service
journalctl --user -u stirling.service -n 50 --no-pager
```
