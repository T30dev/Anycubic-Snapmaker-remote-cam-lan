# Remote Cam — 3D Printer Dashboard

Modern web interface to view FLV camera streams from 3D printers over LAN, with multi-printer support, recording tools, and filament stock tracking.

## ✨ Features

### 🎥 Multi-Printer Dashboard (`Remote-cam-multi.html`)
- **Unlimited printer cards** — add or remove printers dynamically at runtime
- **Per-printer color coding** — 8 unique accent color schemes for quick visual identification
- **Live FLV video playback** via `flv.js` with 16:9 aspect ratio and fullscreen support
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
| `Remote-cam-multi.html` | **Multi-printer dashboard** — main file, all features included |
| `Remote-cam.html` | Legacy single-camera viewer (kept for reference) |

---

## 🚀 How to Use

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
| Chrome (desktop/Android) | ✅ Full support including recording |
| Edge (desktop/Android) | ✅ Full support |
| Firefox (desktop/Android) | ✅ Full support |
| Safari / iPad | ⚠️ Streaming works; recording/timelapse not supported (FLV + MediaRecorder limitations) |
| iPhone (Safari/Chrome) | ❌ FLV not supported |

Tested with:
- ✅ Anycubic Kobra S1
- ⚠️ Should work with any printer that streams FLV over LAN

---

## ⚙️ Technologies Used

- HTML5 + CSS3 (custom design tokens, responsive grid)
- Vanilla JavaScript — no heavy frameworks
- [`flv.js`](https://github.com/bilibili/flv.js) via CDN — FLV live stream playback
- `MediaRecorder` API — in-browser video recording
- `localStorage` — configuration and filament data persistence

---

## ❗ Disclaimer

> This project is an open-source tool and is **not affiliated with or endorsed by Anycubic** or any other manufacturer.
> "Anycubic" and "Kobra S1" are trademarks of their respective owners.
> This software is intended for personal and educational use only.

---

## 🛡️ License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

You are free to use, copy, and modify the code for personal and non-commercial purposes.
You may not sell, license, or monetize this software or its derivatives.

[Read full license](https://creativecommons.org/licenses/by-nc/4.0/)

---

Developed by Teo · [GitHub](https://github.com/T30dev/Anycubic-remote-cam-lan)
