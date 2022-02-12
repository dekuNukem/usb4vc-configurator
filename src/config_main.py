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
MAIN_WINDOW_HEIGHT = 650
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

root_folder_path = ''
flash_drive_base_path = ''
flash_drive_config_path = ''

updates_lf = LabelFrame(root, text="Updates", width=MAIN_WINDOW_WIDTH - PADDING*2, height=60)
updates_lf.place(x=PADDING, y=70)

pc_app_update_label = Label(master=updates_lf)
pc_app_update_label.place(x=400, y=10)
pc_app_update_label.config(text='This app (' + str(THIS_VERSION_NUMBER) + '): Unknown', fg='black', bg=default_button_color)
pc_app_update_label.unbind("<Button-1>")

def update_copy_button_click():
    rcode, src_base_path = check_update.get_usb4vc_update(temp_path)
    if rcode != 0:
        messagebox.showerror("Error", "Error Fetching Update: \n\n"+str(msg))
        return
    if len(root_folder_path) < 2:
        return
    try:
        dest_base_path = os.path.join(root_folder_path, 'usb4vc')
        dest_firmware_path = os.path.join(dest_base_path, 'firmware')
        dest_rpi_app_path = os.path.join(dest_base_path, 'rpi_app')
        ensure_dir(dest_base_path)
        time.sleep(0.1)
        shutil.rmtree(dest_rpi_app_path)
        time.sleep(0.1)
        shutil.rmtree(dest_firmware_path)
        time.sleep(0.1)
    except Exception as e:
        pass
    try:
        src_firmware_path = os.path.join(src_base_path, 'firmware')
        src_rpi_app_path = os.path.join(src_base_path, 'rpi_app')
        shutil.copytree(src_firmware_path, dest_firmware_path)
        shutil.copytree(src_rpi_app_path, dest_rpi_app_path)
    except Exception as e:
        messagebox.showerror("Error", "File Copy Failed: \n\n"+str(e))
    messagebox.showinfo("Update", "Done!")

copy_button = Button(updates_lf, text="Copy Latest USB4VC Updates to Flash Drive", command=update_copy_button_click, state=DISABLED)
copy_button.place(x=10, y=5, width=300)

gamepad_config_lf = LabelFrame(root, text="Custom Gamepad Mappings", width=MAIN_WINDOW_WIDTH - PADDING*2, height=500)
gamepad_config_lf.place(x=PADDING, y=140)

profiles_lf = LabelFrame(gamepad_config_lf, text="Profiles", width=180, height=435)
profiles_lf.place(x=10, y=5)

options_lf = LabelFrame(gamepad_config_lf, text="Options", width=180, height=435)
options_lf.place(x=200, y=5)

mappings_lf = LabelFrame(gamepad_config_lf, text="Mappings", width=375, height=435)
mappings_lf.place(x=390, y=5)

gamepad_mapping_dict_list = []
profile_var = StringVar()

def on_profile_lstbox_select(event):
    update_profile_display()

def update_profile_display():
    profile_var.set([x['display_name'] for x in gamepad_mapping_dict_list])
    if len(profile_lstbox.curselection()) <= 0:
        return
    index = profile_lstbox.curselection()[0]
    pboard_dropdown.config(state=NORMAL)
    usb_gamepad_dropdown.config(state=NORMAL)
    mapping_add_button.config(state=NORMAL)
    mapping_remove_button.config(state=NORMAL)
    mapping_edit_button.config(state=NORMAL)
    mapping_dupe_button.config(state=NORMAL)
    print(gamepad_mapping_dict_list[index])
    pboard_option_var.set(str(gamepad_mapping_dict_list[index].get('protocol_board', "Unknown")))
    usb_gamepad_option_var.set(str(gamepad_mapping_dict_list[index].get('usb_gamepad_type', "Generic")))
    mapping_str_list = []
    try:
        for item in gamepad_mapping_dict_list[index]['mapping']:
            this_str = ''
            usb_gamepad_source = item
            map_dict = gamepad_mapping_dict_list[index]['mapping'][item]
            gap1 = 15 - len(usb_gamepad_source)
            this_str += usb_gamepad_source + ' '*gap1
            for value in list(map_dict.values()):
                this_gap = 15 - len(value)
                this_str += value + ' '*this_gap
            this_str += '\n'
            mapping_str_list.append(this_str)
        mappings_var.set(mapping_str_list)
    except Exception as e:
        print('update_profile_display', e)

profile_lstbox = Listbox(profiles_lf, listvariable=profile_var, height=16, exportselection=0)
profile_lstbox.place(x=10, y=5, width=150, height=270)
profile_lstbox.bind('<<ListboxSelect>>', on_profile_lstbox_select)

mappings_var = StringVar()
mappings_lstbox = Listbox(mappings_lf, listvariable=mappings_var, height=16, exportselection=0, font='TkFixedFont')
mappings_lstbox.place(x=10, y=5, width=350, height=340)
mappings_lstbox.config()

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 25

profile_add_button = Button(profiles_lf, text="New", command=None, state=DISABLED)
profile_add_button.place(x=10, y=290, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

profile_dupe_button = Button(profiles_lf, text="Duplicate", command=None, state=DISABLED)
profile_dupe_button.place(x=10, y=320, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

profile_rename_button = Button(profiles_lf, text="Rename", command=None, state=DISABLED)
profile_rename_button.place(x=10, y=350, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

profile_remove_button = Button(profiles_lf, text="Remove", command=None, state=DISABLED)
profile_remove_button.place(x=10, y=380, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_add_button = Button(mappings_lf, text="New", command=None, state=DISABLED)
mapping_add_button.place(x=20, y=350, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_edit_button = Button(mappings_lf, text="Edit", command=None, state=DISABLED)
mapping_edit_button.place(x=200, y=350, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_dupe_button = Button(mappings_lf, text="Duplicate", command=None, state=DISABLED)
mapping_dupe_button.place(x=20, y=380, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_remove_button = Button(mappings_lf, text="Remove", command=None, state=DISABLED)
mapping_remove_button.place(x=200, y=380, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_save_button = Button(gamepad_config_lf, text="Save Current Mappings to Flash Drive", command=None, state=NORMAL, fg='red')
mapping_save_button.place(x=10, y=447, width=755, height=BUTTON_HEIGHT)

def enable_buttons():
    copy_button.config(state=NORMAL)
    profile_add_button.config(state=NORMAL)
    profile_remove_button.config(state=NORMAL)
    profile_rename_button.config(state=NORMAL)
    profile_dupe_button.config(state=NORMAL)

def select_root_folder(root_path=None):
    global root_folder_path
    global flash_drive_base_path
    global flash_drive_config_path
    if root_path is None:
        root_path = filedialog.askdirectory()
    if len(root_path) <= 0:
        return
    root_folder_path = root_path
    dp_root_folder_display.set("Selected: " + root_path)
    flash_drive_base_path = os.path.join(root_folder_path, 'usb4vc')
    flash_drive_config_path = os.path.join(flash_drive_base_path, 'config')
    load_gamepad_mapping(flash_drive_config_path)
    update_profile_display()
    enable_buttons()

open_button = Button(connection_lf, text="Open...", command=select_root_folder)
open_button.place(x=10, y=5, width=80)

def load_gamepad_mapping(search_path):
    try:
        gamepad_mapping_dict_list.clear()
        file_list = [d for d in os.listdir(search_path) if d.startswith("usb4vc_map") and d.lower().endswith(".json")]
        for item in file_list:
            full_file_name = os.path.join(search_path, item)
            with open(full_file_name) as json_file:
                temp = json.load(json_file)
                if isinstance(temp, dict) and 'display_name' in temp:
                    gamepad_mapping_dict_list.append(temp)
                else:
                    raise ValueError("not a valid config file")
    except Exception as e:
        print('load_gamepad_mapping:', e)

protocol_board_dropdown_label = Label(master=options_lf, text="Protocol Card:")
protocol_board_dropdown_label.place(x=5, y=5)
protocol_board_list = ['Unknown', 'IBMPC', "ADB"]
pboard_option_var = StringVar()
pboard_option_var.set(protocol_board_list[0])
pboard_dropdown = OptionMenu(options_lf, pboard_option_var, *protocol_board_list)
pboard_dropdown.place(x=5, y=30, width=150)
pboard_dropdown.config(state=DISABLED)

usb_gamepad_type_dropdown_label = Label(master=options_lf, text="USB Gamepad:")
usb_gamepad_type_dropdown_label.place(x=5, y=80)
usb_gamepad_list = ['Generic', 'Xbox One Wired', "Xbox One Bluetooth"]
usb_gamepad_option_var = StringVar()
usb_gamepad_option_var.set(usb_gamepad_list[0])
usb_gamepad_dropdown = OptionMenu(options_lf, usb_gamepad_option_var, *usb_gamepad_list)
usb_gamepad_dropdown.place(x=5, y=100, width=150)
usb_gamepad_dropdown.config(state=DISABLED)

select_root_folder('C:/Users/allen/Desktop/flashdrive_test')

root.update()
root.mainloop()
