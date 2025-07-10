# OBS Replay Buffer Saver

System‑tray utility for Windows that lets you bind a global hotkey to save OBS’s Replay Buffer via obs-websocket, complete with toast notifications and persistent config.

---

## Features

* **Global Hotkey**: Press your custom hotkey (e.g. `Ctrl+Alt+S`) to trigger an OBS Replay Buffer save, even when OBS is in the background.
* **System Tray Icon**: Access the app via a tray icon with menu items:

  * *Save Replay* — manually trigger buffer save
  * *Quit* — exit the app
* **Toast Notifications**: Windows toast pop-ups confirm success or report errors.
* **Persistent Configuration**: Stores OBS connection details and hotkey in a `config.ini` next to the EXE for future runs.
* **Automatic Replay Buffer Start**: If the buffer isn’t already running, the app will start it briefly before saving.

---

## Dependencies

* Python 3.7+ (Windows)
* [obs-websocket-py](https://github.com/obsproject/obs-websocket)
* [pystray](https://github.com/moses-palmer/pystray)
* [Pillow](https://python-pillow.org/)
* [keyboard](https://github.com/boppreh/keyboard)
* [winotify](https://github.com/dekellum/winotify)

---

## Installation & Packaging

1. **Clone or download** this repository.
2. **Install Python dependencies**:

   ```bash
   pip install obs-websocket-py pystray pillow keyboard winotify
   ```
3. **Install PyInstaller** (if not already):

   ```bash
   pip install pyinstaller
   ```
4. **Place an icon** named `obs_replay.ico` alongside `toggle.py` (optional; fallback icon is included).
5. **(Optional)** Create a `version.txt` resource if you want custom file metadata.
6. **Build the single EXE**:

   ```bash
   pyinstaller \
     --onefile \
     --noconsole \
     --icon=obs_replay.ico \
     --name OBSReplaySaver \
     --version-file version.txt \
     toggle.py
   ```
7. Find `OBSReplaySaver.exe` in the `dist/` directory.

---

## Usage

1. **Run** `OBSReplaySaver.exe` once.
2. **Enter** your OBS WebSocket host/IP, port (default `4444`), password (if any), and desired hotkey when prompted.
3. The app will minimize to the system tray. Press your hotkey or use the tray menu to save the Replay Buffer.
4. OBS must have Replay Buffer enabled (Settings → Output → Replay Buffer) prior to saving.

---

## Configuration File (`config.ini`)

Located next to the EXE after first run. Sample structure:

```ini
[OBS]
host = 192.168.1.100
port = 4444
password = mySecret

[HOTKEY]
save = ctrl+alt+s
```

Edit this file directly to change OBS details or hotkey without re-running the prompts.

---

## Troubleshooting

* **Hotkey not working**: Make sure the chosen combination isn’t reserved by Windows or other apps. Run as administrator if needed.
* **No tray icon**: Verify `obs_replay.ico` is next to the EXE, or allow the fallback icon via the script.
* **Notifications missing**: Ensure `winotify` is installed. Otherwise, errors and confirmations will print to the console.
* **OBS connection errors**: Double-check WebSocket port, host/IP, and password in OBS’s settings.

---

## Contributing

1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m "Add YourFeature"`).
4. Push to your branch and open a Pull Request.

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
