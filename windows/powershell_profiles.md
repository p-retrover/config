# about_Profiles

**Article Date:** 07/17/2023

## Short Description

Describes how to create and use a PowerShell profile.

## Long Description

You can create a PowerShell profile to customize your environment and add session-specific elements to every PowerShell session that you start.

A PowerShell profile is a script that runs when PowerShell starts. You can use the profile as a startup script to customize your environment. You can add commands, aliases, functions, variables, modules, PowerShell drives and more. You can also add other session-specific elements to your profile so they're available in every session without having to import or re-create them.

PowerShell supports several profiles for users and host programs. However, it doesn't create the profiles for you.

## Profile Types and Locations

PowerShell supports several profile files that are scoped to users and PowerShell hosts. You can have any or all these profiles on your computer.

The profiles are listed in the **order that they're executed**. This means that changes made in the *All Users, All Hosts* profile can be overridden by any of the other profile scripts. The *Current User, Current Host* profile always runs last.

### 1. All Users, All Hosts

* **Windows:** `$PSHOME\Profile.ps1`
* **Linux:** `/opt/microsoft/powershell/7/profile.ps1`
* **macOS:** `/usr/local/microsoft/powershell/7/profile.ps1`

### 2. All Users, Current Host

* **Windows:** `$PSHOME\Microsoft.PowerShell_profile.ps1`
* **Linux:** `/opt/microsoft/powershell/7/Microsoft.PowerShell_profile.ps1`
* **macOS:** `/usr/local/microsoft/powershell/7/Microsoft.PowerShell_profile.ps1`

### 3. Current User, All Hosts

* **Windows:** `$HOME\Documents\PowerShell\Profile.ps1`
* **Linux:** `~/.config/powershell/profile.ps1`
* **macOS:** `~/.config/powershell/profile.ps1`

### 4. Current User, Current Host

* **Windows:** `$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`
* **Linux:** `~/.config/powershell/Microsoft.PowerShell_profile.ps1`
* **macOS:** `~/.config/powershell/Microsoft.PowerShell_profile.ps1`

### Host-Specific Profiles (Examples)

Other programs that host PowerShell (like VS Code) can support their own profiles:

* **All users, Current Host:** `$PSHOME\Microsoft.VSCode_profile.ps1`
* **Current user, Current Host:** `$HOME\Documents\PowerShell\Microsoft.VSCode_profile.ps1`

### Key Variables

* **`$PSHOME`**: Stores the installation directory for PowerShell.
* **`$HOME`**: Stores the current user's home directory.

> [!IMPORTANT]
> **Note for Windows Users:** The location of the Documents folder can be changed by folder redirection or OneDrive. It is **not recommended** to redirect the Documents folder to a network share or OneDrive, as it can cause modules to fail to load and create errors in your profile scripts.

## The $PROFILE Variable

The `$PROFILE` automatic variable stores the paths to the PowerShell profiles available in the current session.

* `$PROFILE`: Stores the path to the "Current User, Current Host" profile.
* The other profiles are saved as **note properties**:
* `$PROFILE.CurrentUserCurrentHost`
* `$PROFILE.CurrentUserAllHosts`
* `$PROFILE.AllUsersCurrentHost`
* `$PROFILE.AllUsersAllHosts`



To see the current values for your host:

```powershell
$PROFILE | Select-Object *

```

## Profile Management

### How to Create a Profile

Use the following format to ensure you do not overwrite an existing profile:

```powershell
if (!(Test-Path -Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}

```

*Note: To create "All Users" profiles in Windows, you must start PowerShell with the **Run as administrator** option.*

### How to Edit a Profile

You can open your profile in any text editor. To open the current profile in Notepad:

```powershell
notepad $PROFILE

```

To open the *All Users, All Hosts* profile:

```powershell
notepad $PROFILE.AllUsersAllHosts

```

*Changes take effect after you save the file and **restart PowerShell**.*

### How to Choose a Profile

* **Specific User, All Hosts:** Use `$PROFILE.CurrentUserAllHosts` for items you want in every terminal (VS Code, Console, etc.).
* **Host Specific:** Use `$PROFILE.CurrentUserCurrentHost` for host-specific items (like background colors).
* **Administrator Guidelines:**
* Store common items in `$PROFILE.AllUsersAllHosts`.
* Store host-specific items for all users in `$PROFILE.AllUsersCurrentHost`.



## Profile Content Examples

### 1. List Aliases for a Cmdlet

```powershell
function Get-CmdletAlias ($cmdletname) {
    Get-Alias |
    Where-Object -FilterScript {$_.Definition -like "$cmdletname"} |
    Format-Table -Property Definition, Name -AutoSize
}

```

### 2. Customize Console Title

```powershell
function CustomizeConsole {
    $hosttime = (Get-ChildItem -Path $PSHOME\pwsh.exe).CreationTime
    $hostversion = "$($Host.Version.Major).$($Host.Version.Minor)"
    $Host.UI.RawUI.WindowTitle = "PowerShell $hostversion ($hosttime)"
    Clear-Host
}
CustomizeConsole

```

### 3. Custom Prompt

```powershell
function Prompt {
    $env:COMPUTERNAME + "\" + (Get-Location) + "> "
}

```

## Advanced Usage and Troubleshooting

### The NoProfile Parameter

To start PowerShell without loading profiles (useful for troubleshooting or automated scripts):

```powershell
pwsh -NoProfile

```

### Execution Policy

The execution policy determines if scripts/profiles can run.

* The **Restricted** policy is the default and prevents profiles from running.
* Use `Set-ExecutionPolicy` to change this. This value is saved in the registry and applies to all sessions.

### Remote Sessions

PowerShell profiles are **not** run automatically in remote sessions. The `$PROFILE` variable is not populated.

**To run a local profile in a remote session:**

```powershell
Invoke-Command -Session $s -FilePath $PROFILE

```

**To run a profile stored on the remote computer (using dot sourcing):**

```powershell
Invoke-Command -Session $s -ScriptBlock {
    . "$HOME\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
}

```

## Further Study & Resources

For deeper dives into the concepts mentioned in this guide, refer to the following internal PowerShell documentation topics:

* **`about_Automatic_Variables`**: For more on `$PROFILE`, `$PSHOME`, and `$HOME`.
* **`about_Execution_Policies`**: Understanding the security layers for script execution.
* **`about_Functions`**: Learning how to write robust tools for your profile.
* **`about_Prompts`**: Advanced customization of the command prompt.
* **`about_Remote`**: Handling sessions on remote machines.
* **`about_Scopes`**: Understanding how variables and functions persist across scopes.
* **`about_Signing`**: Security best practices for signing your scripts.

### Community & Feedback

PowerShell is an open-source project. You can collaborate or provide feedback via:

* [PowerShell GitHub Repository](https://github.com/PowerShell/PowerShell)
* GitHub Documentation Issues
* Official Product Feedback channels