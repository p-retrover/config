# OBS Studio reference

## Configuration File Reference

Managing your "dotfiles" or configuration folders is the first step toward a portable and reproducible setup.

| Operating System | Configuration Directory Path | Notes |
| :--- | :--- | :--- |
| **Arch / Fedora** | `~/.config/obs-studio/` | Standard XDG path. |
| **Windows** | `%APPDATA%\obs-studio\` | Paste this into the File Explorer address bar. |
| **Portable (Any)** | `[OBS Root Folder]\config\` | Create a `portable_mode.txt` in the root folder to enable this. |

### Key Files to Backup

* **`basic/profiles/`**: Your encoding settings, bitrates, and stream keys.
* **`basic/scenes/`**: Your entire visual layout (sources, filters, transitions).
* **`global.ini`**: UI preferences, theme choices, and general settings.

-----

## OBS Studio Setup Process

### **Windows Setup**

1. **Installation**: Download the `.exe` installer from [obsproject.com](https://obsproject.com).
2. **Hardware Acceleration**: Ensure **GPU Scheduling** is enabled in *Windows Settings \> Display \> Graphics*.
3. **Run as Administrator**: Crucial for OBS to prioritize GPU resources over background games.

### **Arch Linux Setup**

1. **Core Installation**:

    ```bash
    sudo pacman -S obs-studio
    ```

2. **Hyprland/Wayland Support**: To capture your screen on Hyprland, you MUST have the portal installed:

    ```bash
    sudo pacman -S xdg-desktop-portal-hyprland pipewire wireplumber
    ```

3. **Plugins (AUR)**: Use `yay -S obs-vkcapture` for zero-latency Vulkan game capture.

### **Fedora Setup**

1. **Native Installation**:

    ```bash
    sudo dnf install obs-studio
    ```

2. **Flatpak (Recommended for Plugins)**: Fedora users often prefer the Flatpak for better plugin compatibility:

    ```bash
    flatpak install flathub com.obsproject.Studio
    ```

-----

## Optimal Encoding Settings

trend has shifted towards **AV1** and **Hybrid MP4**.

* **Recording Format**: Use **Hybrid MP4**. It provides the crash-safety of MKV (files won't corrupt if OBS crashes) but remains natively compatible with all video editors.
* **Encoder (AV1)**:
  * **NVIDIA (RTX 40/50 series)**: `NVENC AV1`.
  * **AMD (RX 7000+ series)**: `AMD HW AV1`.
  * **Intel (Arc/QuickSync)**: `QSV AV1`.
* **Bitrate Settings**:
  * **1080p 60FPS**: 8,000 - 10,000 Kbps.
  * **4K 60FPS**: 25,000 - 35,000 Kbps.
  * **Rate Control**: `CQP` (Level 18–22) for recording; `CBR` for streaming.

-----

## Low-Latency Streaming Setup

For real-time interaction, we are moving away from traditional RTMP.

### **The Protocol: WHIP & SRT**

* **WHIP (WebRTC):** The gold standard for sub-1-second latency. If your platform (like Cloudflare or a self-hosted instance) supports it, use it.
* **SRT (Secure Reliable Transport):** Better than RTMP for unstable connections. Set **Latency** to `200ms` for a fast response.

### **Encoder Tuning (Zero-Latency)**

Go to **Settings > Output > Output Mode: Advanced**:

* **Rate Control:** `CBR` (Constant Bitrate).
* **Keyframe Interval:** `2 s` (Critical for player sync).
* **Preset:** `P4: Medium` or `P5: Slow` (Since you have 32GB RAM and a solid CPU, don't go to P7; the latency cost isn't worth the tiny quality gain).
* **Tuning:** **Low-Latency** (This disables B-frames which cause delay).
* **Multipass Mode:** `Single Pass` (Multiple passes increase encoding delay).

-----

## Using Your Phone as a Webcam

### **DroidCam**

* **Windows**: Install the Windows Client. Enable **USB Debugging** on your phone (Developer Options) to use the more stable USB connection.
* **Arch Linux**:

    ```bash
    yay -S droidcam v4l2loopback-dkms
    sudo modprobe v4l2loopback exclusive_caps=1
    ```

* **Fedora**:

    ```bash
    sudo dnf install android-tools
    # Download the client from dev47apps.com and run the install script.
    ```

**Connection:** Use **USB (ADB)** instead of WiFi to eliminate network jitter.

### **Iriun Webcam (Simpler "Plug & Play")**

* **Windows**: Download and run the `.exe`. It appears as a standard camera in OBS.
* **Arch**: `yay -S iriunwebcam-bin`.
* **Fedora**: Download the Beta RPM from [iriun.com](https://iriun.com).

### **Camo (The "Ultra-Quality" Choice)**

* **Setup:** Install the Camo Studio desktop app (Windows/Linux via AUR).
* **Pro Tip:** It provides a "Virtual Camera" source in OBS that is remarkably stable on Fedora.

-----

## Hyprland & Linux Specifics

On a Wayland-based WM (Hyprland), standard "Screen Capture" won't work without portals.

* **Portal Check:** Ensure `xdg-desktop-portal-hyprland` is running.
* **PipeWire Latency:** To force low latency in the audio stack, launch OBS with:
    `PIPEWIRE_LATENCY="128/48000" obs`
* **Vulkan Capture:** Use `obs-vkcapture` (AUR/DNF) for recording high-performance applications with zero overhead.

-----

## References

### **YouTube Tutorials**

* **[OBS 2026: The Ultimate Crash-Proof Setup](https://www.youtube.com/watch?v=3ZTl2YJEeT4)** – Focuses on Hybrid MP4 and AV1 encoding.
* **[Phone as Webcam on Linux (Fedora/Arch)](https://www.youtube.com/watch?v=t8m-Dxk_A8s)** – A technical walkthrough of `v4l2loopback` drivers.
* **[Stop Using Default OBS Settings](https://www.youtube.com/watch?v=J3D4X0NEsXs)** – Essential filter and bitrate tweaks for 2026.

* **[OBS Studio 2026: Zero Lag Setup](https://www.youtube.com/watch?v=3ZTl2YJEeT4)** – Focuses on the new "Hybrid MP4" and low-latency encoding.
* **[WHIP & WebRTC: The End of RTMP?](https://www.youtube.com/watch?v=t8m-Dxk_A8s)** – Deep dive into setting up ultra-low latency streams.
* **[DroidCam on Linux (2026 Setup)](https://www.youtube.com/watch?v=OKRBJNJigSM)** – Step-by-step for Fedora and Arch users.

### **Technical Articles**

* **[ArchWiki: OBS Studio](https://wiki.archlinux.org/title/Open_Broadcaster_Software)** – Best resource for PipeWire and Wayland troubleshooting.
* **[DroidCam Help & FAQ](https://www.dev47apps.com/droidcam/linux/)** – Detailed steps for getting USB/ADB connections working on Linux.
* **[Baeldung: V4L2 Virtual Cameras](https://www.google.com/search?q=https://www.baeldung.com/linux/v4l2loopback-virtual-camera)** – A deep dive for Linux users on how virtual video devices work.
* **[OBS Project: WHIP Streaming Guide](https://obsproject.com/kb/whip-streaming-guide)** – Official documentation for WebRTC integration.
* **[Dev47Apps: DroidCam Linux Install](https://www.dev47apps.com/droidcam/linux/)** – Detailed driver installation for non-standard kernels.
