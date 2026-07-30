# Zen Browser: Restore Lost Session & Tabs After Update (Flatpak / Fedora)

If Zen Browser updates and reopens with a clean slate—wiping your tabs and spaces even though **"Open previous windows and tabs"** is enabled—your previous session data is usually safe. On Flatpak installs, the session files are sandboxed and hidden inside a deep directory structure.

---

## Prerequisites

* **Close Zen Browser completely** before attempting any file operations, or active browser processes will overwrite your changes.

---

## Step 1: Open Your Sandboxed Flatpak Profile Directory

Because Flatpak runs in a sandbox, your profile folder is not located at `~/.zen/`.

1. Open your terminal and run:

```bash
xdg-open ~/.var/app/app.zen_browser.zen/.zen/*default*/

```

*(Note: If your flatpak ID uses the alternative namespace, try `io.github.zen_browser.zen` instead).*
2. **Alternative Method:** If terminal access fails, open Zen, type `about:support` in the address bar, find **Profile Directory**, and click **Open Directory**. (Be sure to close the browser after finding the folder).

---

## Step 2: Swap the Session Backup File

1. Navigate to the profile directory you just opened.
2. Open the backup folder named **`zen-sessions-backup`** (or **`sessionstore-backups`**).
3. Locate the snapshot file created right before the update or crash (e.g., `zen-sessions-<timestamp>.jsonlz4`) and **copy it**.
4. Go back to the main profile folder.
5. Find the current empty session file, **`zen-sessions.jsonlz4`**, and rename it to `zen-sessions.jsonlz4.bak` to preserve it.
6. Paste your copied backup file into the main profile folder and rename it exactly to:

```text
zen-sessions.jsonlz4

```

*(Note: If your build relies on Firefox-legacy file structures, repeat this exact process using `sessionstore.jsonlz4` instead).*

---

## Step 3: Relaunch and Verify

1. Start **Zen Browser**.
2. Your previous windows, workspaces, pinned tabs, and session history should automatically restore.

---

### Troubleshooting

If tabs still fail to load:

* Verify whether your backup folder contained `zen-sessions` or `sessionstore` formatted files.
* Check if an automatic Flatpak system update replaced the default profile path or generated a duplicate profile directory.
