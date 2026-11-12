In Fedora 44, dnf uses DNF5, which requires --showduplicates to be placed after the list subcommand rather than before it.

1. List Available Versions Using DNF5 Syntax

Run the command with --showduplicates placed after list:
bash
sudo dnf list --showduplicates megasync
Use code with caution.

2. If an Older Version Appears

If an older 6.6.x build is listed in the output, run:
bash
sudo dnf downgrade megasync
Use code with caution.
Then lock it so future system updates do not overwrite it with the broken build:
bash
sudo dnf versionlock add megasync
Use code with caution.

3. If Only 6.7.0.3 Is Listed in Fedora 44

If no older version is kept in the Fedora 44 repository, remove the broken package and install the working Fedora 43 RPM directly from MEGA's archive:
bash
sudo dnf remove megasync
sudo dnf install https://mega.nz
Use code with caution.
Run the updated dnf list command above and let me know if an older build appears or if you install the Fedora 43 RPM.

megasync.x86_64 5.2.1.0-7.fc44 is available in the base rpmfusion-nonfree repository. Version 5.2.1.0 was built before MEGA added the WebSocket upload requirement, so downgrading to it will resolve the libcurl crash immediately.

1. Downgrade to 5.2.1.0-7.fc44

Run the downgrade command in your terminal:
bash
sudo dnf downgrade megasync
Use code with caution.
Confirm with y when prompted to replace 6.7.0.3-1.fc44 with 5.2.1.0-7.fc44.

2. Lock the Version (So Updates Don't Break It Again)

Because 6.7.0.3-1.fc44 sits in rpmfusion-nonfree-updates, your next sudo dnf upgrade will try to reinstall the broken version unless you lock it. Run:
bash
sudo dnf versionlock add megasync
Use code with caution.
(When a future 6.7.x or 6.8.x update fixes the libcurl issue, you can unlock it later with sudo dnf versionlock delete megasync.)

3. Launch MEGAsync

Start the app normally from your application menu or terminal:
bash
megasync
Use code with caution.
If you run into any dependency prompts during the downgrade or versionlock step, paste the output here and I will help you resolve it.
