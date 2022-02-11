import os
import time
from datetime import datetime
import webbrowser
import check_update
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import urllib.request
from appdirs import *
import json
import shutil

THIS_VERSION_NUMBER = '0.0.1'
MAIN_WINDOW_WIDTH = 800
MAIN_WINDOW_HEIGHT = 600
PADDING = 10
HEIGHT_CONNECT_LF = 60

default_button_color = 'SystemButtonFace'
if 'linux' in sys.platform:
    default_button_color = 'grey'

def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

appname = 'usb4vc_config'
appauthor = 'dekuNukem'
save_path = user_data_dir(appname, appauthor, roaming=True)
backup_path = os.path.join(save_path, 'backups')
temp_path = os.path.join(save_path, 'temp')

try:
    shutil.rmtree(temp_path)
    time.sleep(0.1)
except Exception:
    pass
ensure_dir(save_path)
ensure_dir(backup_path)
ensure_dir(temp_path)

root = Tk()
root.title("USB4VC Configurator v" + THIS_VERSION_NUMBER)
root.geometry(str(MAIN_WINDOW_WIDTH) + "x" + str(MAIN_WINDOW_HEIGHT))
root.resizable(width=FALSE, height=FALSE)

connection_lf = LabelFrame(root, text="Dashboard", width=MAIN_WINDOW_WIDTH - PADDING*2, height=HEIGHT_CONNECT_LF)
connection_lf.place(x=PADDING, y=0)

def open_user_manual_url():
    webbrowser.open('https://github.com/dekuNukem/usb4vc-configurator/blob/master/README.md')

def open_discord_link():
    webbrowser.open('https://discord.gg/HAuuh3pAmB')

def backup_button_click():
    messagebox.showinfo("Backups", "All your backups are here!")
    if 'darwin' in sys.platform:
        subprocess.Popen(["open", backup_path])
    elif 'linux' in sys.platform:
        subprocess.Popen(["xdg-open", backup_path])
    else:
        webbrowser.open(backup_path)

INVALID_ROOT_FOLDER_STRING = "<-- Press & Select Your Flash Drive"
dp_root_folder_display = StringVar()
dp_root_folder_display.set(INVALID_ROOT_FOLDER_STRING)

root_folder_path_label = Label(master=connection_lf, textvariable=dp_root_folder_display, foreground='navy')
root_folder_path_label.place(x=100, y=6)

user_manual_button = Button(connection_lf, text="User Manual", command=open_user_manual_url)
user_manual_button.place(x=500, y=5, width=90)

discord_button = Button(connection_lf, text="Discord", command=open_discord_link)
discord_button.place(x=600, y=5, width=80)

discord_button = Button(connection_lf, text="Backups", command=backup_button_click)
discord_button.place(x=690, y=5, width=80)

dp_root_folder_path = ''
def select_root_folder(root_path=None):
    global dp_root_folder_path
    if root_path is None:
        root_path = filedialog.askdirectory()
    if len(root_path) <= 0:
        return
    dp_root_folder_path = root_path
    dp_root_folder_display.set("Selected: " + root_path)
    copy_button.config(state=NORMAL)

open_button = Button(connection_lf, text="Open...", command=select_root_folder)
open_button.place(x=10, y=5, width=80)

updates_lf = LabelFrame(root, text="Updates", width=MAIN_WINDOW_WIDTH - PADDING*2, height=85)
updates_lf.place(x=PADDING, y=70)

pc_app_update_label = Label(master=updates_lf)
pc_app_update_label.place(x=10, y=40)
pc_app_update_label.config(text='This app (' + str(THIS_VERSION_NUMBER) + '): Unknown', fg='black', bg=default_button_color)
pc_app_update_label.unbind("<Button-1>")

def update_copy_button_click():
    rcode, msg = check_update.get_usb4vc_update(temp_path)
    if rcode != 0:
        messagebox.showerror("Error", "Unable to fetch update: \n\n"+str(msg))
        return
    try:
        dest_dir = os.path.join(dp_root_folder_path, 'usb4vc')
        shutil.rmtree(dest_dir)
        time.sleep(0.05)
    except Exception as e:
        pass
    try:
        shutil.copytree(msg, dest_dir) 
    except Exception as e:
        messagebox.showerror("Error", "File Copy Failed: \n\n"+str(e))
    messagebox.showinfo("Update", "Done!")

copy_button = Button(updates_lf, text="Copy Latest USB4VC Updates to Flash Drive", command=update_copy_button_click, state=DISABLED)
copy_button.place(x=10, y=5, width=300)

mappings_lf = LabelFrame(root, text="Custom Gamepad Mappings", width=MAIN_WINDOW_WIDTH - PADDING*2, height=425)
mappings_lf.place(x=PADDING, y=165)

select_root_folder('C:/Users/allen/Desktop/flashdrive_test')

root.update()
root.mainloop()
