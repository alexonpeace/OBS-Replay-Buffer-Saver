import sys
import os
import time
import threading
import configparser
import keyboard
from obswebsocket import obsws, requests
import pystray
from PIL import Image, ImageDraw, ImageOps
import tkinter as tk
from tkinter.simpledialog import askstring, askinteger

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
    """
    Pop up GUI dialogs to gather OBS connection settings and hotkey.
    """
    global HOST, PORT, PASSWORD, HOTKEY
    root = tk.Tk()
    root.withdraw()  # hide blank main window

    if not HOST:
        HOST = askstring("OBS Replay Saver", "Enter OBS host/IP:")
    if not PORT:
        PORT = askinteger("OBS Replay Saver", "Enter OBS port [4444]:", initialvalue=4444)
    if PASSWORD is None:
        PASSWORD = askstring("OBS Replay Saver", "Enter OBS password (leave blank if none):")
    if not HOTKEY:
        HOTKEY = askstring("OBS Replay Saver", "Enter save hotkey (e.g. ctrl+alt+s):")

    root.destroy()
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
    # If no config file or missing settings, prompt user via GUI
    if not (HOST and PORT and HOTKEY is not None):
        prompt_settings()

    try:
        keyboard.add_hotkey(HOTKEY, lambda: threading.Thread(target=save_replay,daemon=True).start())
    except Exception as e:
        notify('OBSReplaySaver Error', f'Failed to register hotkey: {e}')
        sys.exit(1)

    # Hide console window on Windows when frozen
    if os.name == 'nt' and getattr(sys, 'frozen', False):
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    setup_tray()
