# OBS Replay Buffer Saver

A lightweight Windows utility designed for two-PC streaming setups. Run this app on your **Main (Gaming PC) machine** to remotely trigger a Replay Buffer save on your **Second (Streaming PC) Machine** via WebSockets.

---

## Key Features

- **Dual-PC Support**  
  Control OBS running on a separate PC over the network—all you need is OBS WebSocket enabled on the primary machine.
- **Global Hotkey**  
  Configure a custom hotkey (e.g. `Ctrl+Alt+S`) on the control PC to instantly save the Replay Buffer from the OBS PC, even if OBS is minimized or in another room.
- **System Tray Utility**  
  – Tray icon with **Save Replay** and **Quit**  
  – Automatically runs hidden in the background  
- **Windows Toast Notifications**  
  Instant feedback on success or failure, powered by `winotify`.  
- **Persistent Configuration**  
  First-run prompts store OBS host/IP, port, password, and hotkey in `config.ini` next to the EXE.  
- **Automatic Buffer Start**  
  If the Replay Buffer isn’t active on the OBS PC, the app will start it before saving—so you never miss a moment.

---

## Prerequisites

- **Primary PC (OBS)**
  - Windows OS  
  - OBS Studio with **obs-websocket** plugin installed and enabled  
  - WebSocket port (default `4444`) reachable from your network

- **Control PC**
  - Windows OS  
  - Python 3.7+ (if building from source) or the standalone EXE  
  - Network connectivity to the OBS PC

---

## Dependencies

If building from source on the control PC:
```bash
pip install obs-websocket-py pystray pillow keyboard winotify
````

---

## Building the EXE

1. Install PyInstaller (if needed):

   ```bash
   pip install pyinstaller
   ```
2. Place your icon (`obs_replay.ico`) and optional `version.txt` next to `toggle.py`.
3. Run:

   ```bash
   pyinstaller \
     --onefile \
     --noconsole \
     --icon=obs_replay.ico \
     --name OBSReplaySaver \
     --version-file version.txt \
     toggle.py
   ```
4. Your `OBSReplaySaver.exe` will appear in the `dist/` folder.

---

## Usage

1. Launch **OBSReplaySaver.exe** on the **control PC**.
2. Enter your **OBS PC’s** host/IP, WebSocket port (default 4444), password (if set), and desired hotkey.
3. The app minimizes to the tray.
4. Press the hotkey—or right-click the tray icon and choose **Save Replay**—to save the OBS Replay Buffer remotely.
5. Verify on the **OBS PC** that Replay Buffer is enabled (Settings → Output → Replay Buffer).

---

## Configuration File (`config.ini`)

Located next to the EXE after first run:

```ini
[OBS]
host     = 192.168.1.50
port     = 4444
password = yourPassword

[HOTKEY]
save     = ctrl+alt+s
```

Edit these values directly to change settings without rerunning prompts.

---

## Troubleshooting

* **No Response / Hotkey Fails**
  • Ensure the control PC can reach the OBS PC’s IP and port.
  • Run as administrator if OBS requires elevated permissions.
  • Pick a unique hotkey combination not used elsewhere.

* **Tray Icon Missing**
  • Confirm `obs_replay.ico` is next to the EXE, or rely on the fallback icon.
  • Check Windows’ “show hidden icons” overflow or notification area settings.

* **Notifications Absent**
  • Verify `winotify` is installed.
  • If toasts fail, the app will log to the console when run without `--noconsole`.

* **OBS Errors**
  • Double-check OBS WebSocket settings (port, password) on the primary PC.
  • Inspect the app’s console log for detailed errors.

---

## Contributing

1. Fork the repo.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Push and open a PR.

---

## License

MIT license, because it's superior.
```
Copyright (c) 2025 Alex

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
