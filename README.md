# Remote Cam — 3D Printer Dashboard

Modern web interface to view FLV camera streams from 3D printers over LAN, with multi-printer support, recording tools, and filament stock tracking.

> **Supported printers:** Anycubic Kobra S1 · Snapmaker U1 (and any printer that streams FLV over LAN)

## ✨ Features

<img width="1424" height="928" alt="image" src="https://github.com/user-attachments/assets/76cbef77-e3ad-408b-9fde-86e1ad026180" />

### 🎥 Multi-Printer Dashboard (`Remote-cam-multi.html`)

- **Unlimited printer cards** — add or remove printers dynamically at runtime
- **Per-printer color coding** — 8 unique accent color schemes for quick visual identification
- **Live FLV video playback** via `flv.js` with 16:9 aspect ratio and fullscreen support
- **🔍 Video zoom** — zoom in on any camera feed up to 8× with mouse wheel, pinch-to-zoom (touch) or +/− buttons; pan by dragging while zoomed; double-click/tap to reset
- **Recording** — capture live video as `.webm` directly from the browser
- **Timelapse** — capture frames at a configurable interval (seconds/frame) and export as `.webm`
- **Snapshot** — save a `.jpg` still from any camera with one click
- **Filament stock tracker** — register spools by type, brand, color and weight with a visual spool indicator
- **Layout toggle** — switch between side-by-side and stacked grid view (persisted across sessions)
- **Toast notifications** — non-intrusive feedback for every action
- **Per-printer debug log** — real-time log with severity levels, toggleable per card

### 📡 Connection & Streaming

- Custom configuration of protocol, IP, port/path per printer
- Preset port options (`18088/flv`, `/flv`) plus free-form custom entry
- Auto-reconnect on error (3 s delay)
- Real-time speed (KB/s) and latency monitoring with automatic buffer cleanup when latency > 3 s

### 💾 Persistence

- All printer configurations and filament data saved in `localStorage`
- Layout preference persisted across sessions
- Printer list restores automatically on page reload

### 📱 Responsive Design

- Desktop, tablet and mobile friendly
- Compact horizontal layout optimised for viewing multiple streams on smaller screens

---

## 📂 Files

| File | Description |
|------|-------------|
| `Remote-cam-multi-v2.html` | **Multi-printer dashboard v2** — themes, native Snapmaker support, all features |
| `Remote-cam-multi.html` | Previous version (kept for reference) |
| `Remote-cam.html` | Legacy single-camera viewer (kept for reference) |

---

## 🚀 How to Use

### 🟠 Anycubic Kobra S1

1. Enable **LAN mode** on your 3D printer (Settings → Network → LAN Mode)
2. Open Anycubic Slicer and activate the camera live view (Device → Camera)
3. Open `Remote-cam-multi.html` in a browser
4. Click **+ Add Printer** in the header
5. In the configuration modal, enter:
   - Printer name (optional)
   - Protocol (`http` / `https`)
   - Printer IP address (e.g. `192.168.1.6`)
   - Port/path — select `18088/flv` (default) or enter a custom value
6. Click **Connect** — the stream starts automatically

To add more printers, repeat from step 4. Each printer gets its own card with independent controls.

---


### 📡 Native Snapmaker U1 Support (no Python script required)

In v2, the dashboard includes a **built-in keep-alive** via WebSocket and a **JPEG image-refresh stream**, so no external Python script is needed for basic monitoring:

1. Select port `/server/files/camera/monitor.jpg` in the printer config modal
2. The dashboard automatically sends `camera.start_monitor` commands every 2 s via WebSocket
3. The camera image refreshes at ~10 fps

> **Note:** The Python `keepalive_snapmaker.py` script remains available for environments where the browser cannot establish a WebSocket connection directly.

### 🟢 Snapmaker U1 (Legacy — Python script)

The Snapmaker U1 camera automatically stops streaming after a short period of inactivity. A lightweight Python keep-alive script must run alongside the dashboard to send a `camera.start_monitor` command periodically via the printer WebSocket API.

#### 🔑 Get the API Token

1. Open the Snapmaker U1 web panel: `http://PRINTER_IP`
2. Go to **Settings → Authentication**
3. Copy the **API Key** value

> **Important:** treat the API token as sensitive data. Do not publish it.

#### ⚙️ Requirements

Python 3.8+

```bash
python3 --version
```

Install if needed:

```bash
sudo apt update && sudo apt install python3 python3-pip -y
```

Install the dependency:

```bash
python3 -m pip install websocket-client
```

#### 🛠️ Configuration

Edit the script with your values:

```python
PRINTER_IP = "192.168.X.X"
TOKEN      = "YOUR_API_TOKEN"
INTERVAL   = 2
```

#### ▶️ Run manually

```bash
python3 keepalive_snapmaker.py
```

Expected output:

```
Snapmaker U1 Camera KeepAlive
Printer: 192.168.X.X
Interval: 2 seconds
Starting...

16:42:01 camera alive
16:42:05 camera alive
16:42:09 camera alive
```

#### 🔄 Run as a background service (systemd)

```bash
sudo nano /etc/systemd/system/snapmaker-camera.service
```

```ini
[Unit]
Description=Snapmaker Camera KeepAlive
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/snapmaker
ExecStart=/usr/bin/python3 /opt/snapmaker/keepalive_snapmaker.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable snapmaker-camera
sudo systemctl start snapmaker-camera
sudo systemctl status snapmaker-camera
```

View logs:

```bash
journalctl -u snapmaker-camera -f
```

#### 📡 Connect the dashboard

Once the keep-alive script is running:

1. Open `Remote-cam-multi.html` in a browser
2. Click **+ Add Printer**
3. Enter your Snapmaker U1 IP and the appropriate stream port/path
4. Click **Connect**

---

## 🔍 Video Zoom

Each camera feed supports interactive zoom without leaving the dashboard:

| Interaction | Action |
|-------------|--------|
| **Scroll wheel** | Zoom in / out centred on cursor position |
| **Pinch gesture** (touch) | Zoom in / out centred on pinch midpoint |
| `+` / `−` **buttons** | Step zoom in / out by 0.5× |
| **Click and drag** | Pan the view while zoomed in |
| **`1×` button** | Reset zoom to fit (only visible when zoomed) |
| **Double-click / double-tap** | Reset zoom to fit |

- Zoom range: **1× – 8×**
- A live zoom indicator (e.g. `2.5×`) appears on the video while zoomed
- Each printer card has its own independent zoom state


### 🎨 Visual Themes

Switch between built-in themes using the palette button (🎨) in the header:

| Theme | Description |
|-------|-------------|
| **Modern Dark** | Default dark theme with orange and blue accents |
| **Cyberpunk** | Cyan neon tones with a monospace grid overlay |
| **Midnight Purple** | Deep purple palette |
| **Forest Green** | Dark green tones |
| **Custom Image** | Upload your own background photo |

Theme choice is saved in `localStorage` and restored on next load.

---

## 🎬 Recording, Timelapse & Snapshots

Each printer card includes:

| Button | Action |
|--------|--------|
| 🔴 **Rec** | Start/stop video recording → downloads as `.webm` |
| ⏱ **TL** | Start/stop timelapse → compiles and downloads frames as `.webm` |
| 📸 | Save a JPEG snapshot instantly |
| Input field | Interval in seconds per frame for timelapse (default: 5 s) |

> **Note:** Recording and timelapse use the browser's `MediaRecorder` API. Supported on Chrome, Edge and Firefox. Not available on Safari/iOS.

---

## 🧵 Filament Stock Tracker

Located at the bottom of the dashboard. Click **+** to register a spool:

- **Material type** — PLA, ABS, PETG, ASA, TPU, Nylon, PC, or custom
- **Brand** — preset list or custom
- **Color** — preset swatches or color picker with custom name
- **Weight** — grams remaining (shown as a circular fill indicator)

Click any spool card to edit it. Long-press the delete option to remove it.

---

## ⚙️ Local Deployment

Place the HTML file in any directory and serve it with a lightweight HTTP server:

```bash
python3 -m http.server 8000
```

Then open `http://<your-machine-ip>:8000/Remote-cam-multi.html` in your browser.

### ⏱️ Persistent Hosting (systemd)

```ini
[Unit]
Description=Remote Cam Web Server
After=network.target

[Service]
WorkingDirectory=/path/to/your/html
ExecStart=/usr/bin/python3 -m http.server 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Save as `/etc/systemd/system/remotecam.service`, then:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable remotecam
sudo systemctl start remotecam
```

### pm2 (cross-platform)

```bash
npm install -g pm2
pm2 start "python3 -m http.server 8000" --name remote-cam
pm2 save
pm2 startup
```

---

## 📦 Deployment Options

| Environment | Notes |
|-------------|-------|
| 🐳 **Docker / Proxmox LXC** | Place the HTML in a shared volume and serve via a lightweight HTTP server |
| 🌐 **Nginx Proxy Manager** | Point a custom domain to the server hosting this file; ensure the printer stream at `http://192.168.1.X:18088` is accessible from the proxy |
| 🏠 **Home Assistant** | Embed with a **Web Page card**, providing the full local or external URL |

---

## 🧪 Compatibility

| Browser | Status |
|---------|--------|
| Chrome (desktop/Android) | ✅ Full support including recording and zoom |
| Edge (desktop/Android) | ✅ Full support |
| Firefox (desktop/Android) | ✅ Full support |
| Safari / iPad | ⚠️ Streaming and zoom work; recording/timelapse not supported (FLV + MediaRecorder limitations) |
| iPhone (Safari/Chrome) | ❌ FLV not supported |

Tested with:

- ✅ Anycubic Kobra S1
- ✅ Snapmaker U1
- ⚠️ Should work with any printer that streams FLV over LAN

---

## ⚙️ Technologies Used

- HTML5 + CSS3 (custom design tokens, responsive grid)
- Vanilla JavaScript — no heavy frameworks
- [`flv.js`](https://github.com/bilibili/flv.js) via CDN — FLV live stream playback
- `MediaRecorder` API — in-browser video recording
- `localStorage` — configuration and filament data persistence
- `websocket-client` (Python) — Snapmaker U1 camera keep-alive

---

## ❗ Disclaimer

> This project is an open-source tool and is **not affiliated with or endorsed by Anycubic or Snapmaker** or any other manufacturer.
> "Anycubic", "Kobra S1", "Snapmaker" and "U1" are trademarks of their respective owners.
> This software is intended for personal and educational use only.

---

## 🛡️ License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

You are free to use, copy, and modify the code for personal and non-commercial purposes. You may not sell, license, or monetize this software or its derivatives.

[Read full license](https://creativecommons.org/licenses/by-nc/4.0/)

---

Developed by Teo · [GitHub](https://github.com/T30dev/Anycubic-Snapmaker-remote-cam-lan)
