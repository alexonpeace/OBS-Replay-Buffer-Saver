"""
OBS Replay Buffer Saver Tray App

Dependencies:
  - obs-websocket-py
  - pystray
  - pillow
  - keyboard
  - winotify

Pack with:
  pip install pyinstaller
  pyinstaller --onefile --noconsole --icon=obs_replay.ico --name OBSReplaySaver --version-file version.txt toggle.py
"""
import sys
import os
import time
import threading
import configparser
import keyboard
from obswebsocket import obsws, requests
import pystray
from PIL import Image, ImageDraw, ImageOps

# Use winotify for reliable Windows toast notifications
try:
    from winotify import Notification, audio
    def notify(title, msg, duration=5):
        toast = Notification(app_id="OBSReplaySaver",
                             title=title,
                             msg=msg,
                             icon=os.path.join(os.path.dirname(sys.argv[0]), "obs_replay.ico"))
        toast.set_audio(audio.Default, loop=False)
        toast.build().show()
except ImportError:
    def notify(title, msg, duration=5):
        print(f"{title}: {msg}")

# Config file path
CONFIG_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'config.ini')

# Global settings
HOST = PORT = PASSWORD = HOTKEY = None


def load_config():
    global HOST, PORT, PASSWORD, HOTKEY
    cfg = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        cfg.read(CONFIG_PATH)
        HOST = cfg.get('OBS','host',fallback=None)
        PORT = cfg.getint('OBS','port',fallback=None)
        PASSWORD = cfg.get('OBS','password',fallback=None)
        HOTKEY = cfg.get('HOTKEY','save',fallback=None)


def save_config():
    cfg = configparser.ConfigParser()
    cfg['OBS'] = {'host': HOST or '', 'port': str(PORT or ''), 'password': PASSWORD or ''}
    cfg['HOTKEY'] = {'save': HOTKEY or ''}
    with open(CONFIG_PATH,'w') as f:
        cfg.write(f)


def prompt_settings():
    global HOST, PORT, PASSWORD, HOTKEY
    if not HOST:
        HOST = input('Enter OBS host/IP: ').strip()
    if not PORT:
        PORT = int(input('Enter OBS port [4444]: ') or '4444')
    if PASSWORD is None:
        PASSWORD = input('Enter OBS password (leave blank if none): ')
    if not HOTKEY:
        HOTKEY = input('Enter hotkey (e.g. ctrl+alt+s): ').strip()
    save_config()


def save_replay():
    try:
        ws = obsws(HOST, PORT, PASSWORD)
        ws.connect()
        # ensure buffer
        try:
            ws.call(requests.StartReplayBuffer())
        except Exception:
            pass
        time.sleep(0.1)
        ws.call(requests.SaveReplayBuffer())
        notify('OBS Replay', 'Buffer saved successfully')
    except Exception as e:
        notify('OBS Replay Error', str(e))
    finally:
        try:
            ws.disconnect()
        except:
            pass


def make_icon():
    size = 64
    img = Image.new('RGBA',(size,size),(0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((16,16,48,48),fill=(255,255,255,255))
    return img


def setup_tray():
    # Determine base path
    base = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(sys.argv[0]))
    ico_path = os.path.join(base, 'obs_replay.ico')
    if os.path.exists(ico_path):
        icon_image = Image.open(ico_path)
        icon_image = ImageOps.contain(icon_image, (64,64))
    else:
        icon_image = make_icon()

    menu = (
        pystray.MenuItem('Save Replay', lambda icon, item: threading.Thread(target=save_replay,daemon=True).start()),
        pystray.MenuItem('Quit', lambda icon, item: (icon.stop(), sys.exit(0)))
    )
    icon = pystray.Icon('OBSReplaySaver', icon_image, 'OBS Replay Saver', menu)
    icon.run()


if __name__ == '__main__':
    load_config()
    prompt_settings()
    try:
        keyboard.add_hotkey(HOTKEY, lambda: threading.Thread(target=save_replay,daemon=True).start())
    except Exception as e:
        print(f"Failed to register hotkey: {e}")
        sys.exit(1)
    if os.name=='nt':
        import ctypes; ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
    setup_tray()
