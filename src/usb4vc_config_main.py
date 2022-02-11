import os
import time
from datetime import datetime
import webbrowser
# import check_update
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import urllib.request

THIS_VERSION_NUMBER = '0.0.1'
MAIN_WINDOW_WIDTH = 800
MAIN_WINDOW_HEIGHT = 600
PADDING = 10
HEIGHT_CONNECT_LF = 60

default_button_color = 'SystemButtonFace'
if 'linux' in sys.platform:
    default_button_color = 'grey'

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

INVALID_ROOT_FOLDER_STRING = "<-- Press & Select Your Flash Drive"
dp_root_folder_display = StringVar()
dp_root_folder_display.set(INVALID_ROOT_FOLDER_STRING)

root_folder_path_label = Label(master=connection_lf, textvariable=dp_root_folder_display, foreground='navy')
root_folder_path_label.place(x=100, y=6)

user_manual_button = Button(connection_lf, text="User Manual", command=open_user_manual_url)
user_manual_button.place(x=570, y=5, width=100)

discord_button = Button(connection_lf, text="Discord", command=open_discord_link)
discord_button.place(x=680, y=5, width=80)

dp_root_folder_path = ''
def select_root_folder(root_path=None):
    global dp_root_folder_path
    if root_path is None:
        root_path = filedialog.askdirectory()
    if len(root_path) <= 0:
        return
    dp_root_folder_path = root_path
    dp_root_folder_display.set("Selected: " + root_path)

open_button = Button(connection_lf, text="Open...", command=select_root_folder)
open_button.place(x=10, y=5, width=80)

updates_lf = LabelFrame(root, text="Updates", width=MAIN_WINDOW_WIDTH - PADDING*2, height=90)
updates_lf.place(x=PADDING, y=70)

pc_app_update_label = Label(master=updates_lf)
pc_app_update_label.place(x=10, y=40)
pc_app_update_label.config(text='This app (' + str(THIS_VERSION_NUMBER) + '): Unknown', fg='black', bg=default_button_color)
pc_app_update_label.unbind("<Button-1>")

copy_button = Button(updates_lf, text="Copy latest updates to flash drive", command=None)
copy_button.place(x=10, y=10, width=200)

mappings_lf = LabelFrame(root, text="Custom Mappings", width=MAIN_WINDOW_WIDTH - PADDING*2, height=420)
mappings_lf.place(x=PADDING, y=170)

root.update()

root.mainloop()
