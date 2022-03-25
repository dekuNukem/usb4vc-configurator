import os
import time
from datetime import datetime
import webbrowser
import check_update
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import ttk
import urllib.request
from appdirs import *
import json
import shutil
import copy

THIS_VERSION_NUMBER = '0.0.4'
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
        time.sleep(0.05)

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

invalid_filename_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ' ']
def clean_input(str_input, len_limit=None, clean_filename=False):
    result = ''.join([x for x in str_input if 32 <= ord(x) <= 126 and x not in invalid_filename_characters])
    if clean_filename is False:
        result = ''.join([x for x in str_input if 32 <= ord(x) <= 126])
    while('  ' in result):
        result = result.replace('  ', ' ')
    if len_limit is not None:
        result = result[:len_limit]
    return result.strip()

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

def app_update_click(event):
    webbrowser.open('https://github.com/dekuNukem/usb4vc-configurator/releases/latest')

updates_lf = LabelFrame(root, text="Updates", width=MAIN_WINDOW_WIDTH - PADDING*2, height=60)
updates_lf.place(x=PADDING, y=70)

pc_app_update_label = Label(master=updates_lf)
pc_app_update_label.place(x=400, y=10)

update_stats = check_update.get_pc_app_update_status(THIS_VERSION_NUMBER)

if update_stats == 0:
    pc_app_update_label.config(text=f'This app ({THIS_VERSION_NUMBER}): Up to date', fg='black', bg=default_button_color)
    pc_app_update_label.unbind("<Button-1>")
elif update_stats == 1:
    pc_app_update_label.config(text=f'This app ({THIS_VERSION_NUMBER}): Update available! Click me!', fg='black', bg='orange', cursor="hand2")
    pc_app_update_label.bind("<Button-1>", app_update_click)
else:
    pc_app_update_label.config(text=f'This app ({THIS_VERSION_NUMBER}): Unknown', fg='black', bg=default_button_color)
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
        shutil.copytree(src_rpi_app_path, dest_rpi_app_path)
        shutil.copytree(src_firmware_path, dest_firmware_path)
    except Exception as e:
        messagebox.showerror("Error", "File Copy Failed: \n\n"+str(e))
    messagebox.showinfo("Update", "Success!")

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
    print(gamepad_mapping_dict_list[index])
    pboard_option_var.set(str(gamepad_mapping_dict_list[index].get('protocol_board', "IBMPC")))
    usb_gamepad_option_var.set(str(gamepad_mapping_dict_list[index].get('usb_gamepad_type', "Xbox")))
    mapping_str_list = []
    try:
        for item in gamepad_mapping_dict_list[index]['mapping']:
            this_str = ''
            usb_gamepad_source_code, usb_gamepad_source_display_name, usb_gamepad_source_type = tuple_list_search_by_codename(all_codes_list, item)
            map_dict = gamepad_mapping_dict_list[index]['mapping'][item]
            gap1 = 15 - len(usb_gamepad_source_display_name)
            this_str += usb_gamepad_source_display_name + ' '*gap1
            for value in list(map_dict.values()):
                this_code, this_display_name, this_type = tuple_list_search_by_codename(all_codes_list, value)
                this_gap = 15 - len(this_display_name)
                this_str += this_display_name + ' '*this_gap
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

# code, display name, type
generic_usb_gamepad_code_list = [("BTN_GAMEPAD", "BTN_GAMEPAD", "usb_gp_btn"),
    ("BTN_SOUTH", "BTN_SOUTH", "usb_gp_btn"),
    ("BTN_A", "BTN_A", "usb_gp_btn"),
    ("BTN_EAST", "BTN_EAST", "usb_gp_btn"),
    ("BTN_B", "BTN_B", "usb_gp_btn"),
    ("BTN_C", "BTN_C", "usb_gp_btn"),
    ("BTN_NORTH", "BTN_NORTH", "usb_gp_btn"),
    ("BTN_X", "BTN_X", "usb_gp_btn"),
    ("BTN_WEST", "BTN_WEST", "usb_gp_btn"),
    ("BTN_Y", "BTN_Y", "usb_gp_btn"),
    ("BTN_Z", "BTN_Z", "usb_gp_btn"),
    ("BTN_TL", "BTN_TL", "usb_gp_btn"),
    ("BTN_TR", "BTN_TR", "usb_gp_btn"),
    ("BTN_TL2", "BTN_TL2", "usb_gp_btn"),
    ("BTN_TR2", "BTN_TR2", "usb_gp_btn"),
    ("BTN_SELECT", "BTN_SELECT", "usb_gp_btn"),
    ("BTN_START", "BTN_START", "usb_gp_btn"),
    ("BTN_MODE", "BTN_MODE", "usb_gp_btn"),
    ("BTN_THUMBL", "BTN_THUMBL", "usb_gp_btn"),
    ("BTN_THUMBR", "BTN_THUMBR", "usb_gp_btn"),
    ("ABS_X", "ABS_X", "usb_abs_axis"),
    ("ABS_Y", "ABS_Y", "usb_abs_axis"),
    ("ABS_Z", "ABS_Z", "usb_abs_axis"),
    ("ABS_RX", "ABS_RX", "usb_abs_axis"),
    ("ABS_RY", "ABS_RY", "usb_abs_axis"),
    ("ABS_RZ", "ABS_RZ", "usb_abs_axis"),
    ("ABS_THROTTLE", "ABS_THROTTLE", "usb_abs_axis"),
    ("ABS_RUDDER", "ABS_RUDDER", "usb_abs_axis"),
    ("ABS_WHEEL", "ABS_WHEEL", "usb_abs_axis"),
    ("ABS_GAS", "ABS_GAS", "usb_abs_axis"),
    ("ABS_BRAKE", "ABS_BRAKE", "usb_abs_axis"),
    ("ABS_HAT0X", "ABS_HAT0X", "usb_abs_axis"),
    ("ABS_HAT0Y", "ABS_HAT0Y", "usb_abs_axis"),
    ("ABS_HAT1X", "ABS_HAT1X", "usb_abs_axis"),
    ("ABS_HAT1Y", "ABS_HAT1Y", "usb_abs_axis"),
    ("ABS_HAT2X", "ABS_HAT2X", "usb_abs_axis"),
    ("ABS_HAT2Y", "ABS_HAT2Y", "usb_abs_axis"),
    ("ABS_HAT3X", "ABS_HAT3X", "usb_abs_axis"),
    ("ABS_HAT3Y", "ABS_HAT3Y", "usb_abs_axis"),

    ("BTN_MISC", "BTN_MISC", "usb_gp_btn"),
    ("BTN_0", "BTN_0", "usb_gp_btn"),
    ("BTN_1", "BTN_1", "usb_gp_btn"),
    ("BTN_2", "BTN_2", "usb_gp_btn"),
    ("BTN_3", "BTN_3", "usb_gp_btn"),
    ("BTN_4", "BTN_4", "usb_gp_btn"),
    ("BTN_5", "BTN_5", "usb_gp_btn"),
    ("BTN_6", "BTN_6", "usb_gp_btn"),
    ("BTN_7", "BTN_7", "usb_gp_btn"),
    ("BTN_8", "BTN_8", "usb_gp_btn"),
    ("BTN_9", "BTN_9", "usb_gp_btn"),

    ("BTN_JOYSTICK", "BTN_JOYSTICK", "usb_gp_btn"),
    ("BTN_TRIGGER", "BTN_TRIGGER", "usb_gp_btn"),
    ("BTN_THUMB", "BTN_THUMB", "usb_gp_btn"),
    ("BTN_THUMB2", "BTN_THUMB2", "usb_gp_btn"),
    ("BTN_TOP", "BTN_TOP", "usb_gp_btn"),
    ("BTN_TOP2", "BTN_TOP2", "usb_gp_btn"),
    ("BTN_PINKIE", "BTN_PINKIE", "usb_gp_btn"),
    ("BTN_BASE", "BTN_BASE", "usb_gp_btn"),
    ("BTN_BASE2", "BTN_BASE2", "usb_gp_btn"),
    ("BTN_BASE3", "BTN_BASE3", "usb_gp_btn"),
    ("BTN_BASE4", "BTN_BASE4", "usb_gp_btn"),
    ("BTN_BASE5", "BTN_BASE5", "usb_gp_btn"),
    ("BTN_BASE6", "BTN_BASE6", "usb_gp_btn"),
    ("BTN_DEAD", "BTN_DEAD", "usb_gp_btn"),

    ("BTN_TRIGGER_HAPPY", "BTN_TRIGGER_HAPPY", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY1", "BTN_TRIGGER_HAPPY1", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY2", "BTN_TRIGGER_HAPPY2", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY3", "BTN_TRIGGER_HAPPY3", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY4", "BTN_TRIGGER_HAPPY4", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY5", "BTN_TRIGGER_HAPPY5", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY6", "BTN_TRIGGER_HAPPY6", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY7", "BTN_TRIGGER_HAPPY7", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY8", "BTN_TRIGGER_HAPPY8", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY9", "BTN_TRIGGER_HAPPY9", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY10", "BTN_TRIGGER_HAPPY10", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY11", "BTN_TRIGGER_HAPPY11", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY12", "BTN_TRIGGER_HAPPY12", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY13", "BTN_TRIGGER_HAPPY13", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY14", "BTN_TRIGGER_HAPPY14", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY15", "BTN_TRIGGER_HAPPY15", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY16", "BTN_TRIGGER_HAPPY16", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY17", "BTN_TRIGGER_HAPPY17", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY18", "BTN_TRIGGER_HAPPY18", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY19", "BTN_TRIGGER_HAPPY19", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY20", "BTN_TRIGGER_HAPPY20", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY21", "BTN_TRIGGER_HAPPY21", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY22", "BTN_TRIGGER_HAPPY22", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY23", "BTN_TRIGGER_HAPPY23", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY24", "BTN_TRIGGER_HAPPY24", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY25", "BTN_TRIGGER_HAPPY25", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY26", "BTN_TRIGGER_HAPPY26", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY27", "BTN_TRIGGER_HAPPY27", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY28", "BTN_TRIGGER_HAPPY28", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY29", "BTN_TRIGGER_HAPPY29", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY30", "BTN_TRIGGER_HAPPY30", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY31", "BTN_TRIGGER_HAPPY31", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY32", "BTN_TRIGGER_HAPPY32", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY33", "BTN_TRIGGER_HAPPY33", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY34", "BTN_TRIGGER_HAPPY34", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY35", "BTN_TRIGGER_HAPPY35", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY36", "BTN_TRIGGER_HAPPY36", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY37", "BTN_TRIGGER_HAPPY37", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY38", "BTN_TRIGGER_HAPPY38", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY39", "BTN_TRIGGER_HAPPY39", "usb_gp_bbtn"),
    ("BTN_TRIGGER_HAPPY40", "BTN_TRIGGER_HAPPY40", "usb_gp_bbtn"),]

# code, display name, type
xbox_code_list = [("XB_A", "XB A Button", "usb_gp_btn"),
    ("XB_B", "XB B Button", "usb_gp_btn"),
    ("XB_X", "XB X Button", "usb_gp_btn"),
    ("XB_Y", "XB Y Button", "usb_gp_btn"),
    ("XB_LB", "XB LB Button", "usb_gp_btn"),
    ("XB_RB", "XB RB Button", "usb_gp_btn"),
    ("XB_LSB", "XB L-Stick Button", "usb_gp_btn"),
    ("XB_RSB", "XB R-Stick Button", "usb_gp_btn"),
    ("XB_VIEW", "XB View Button", "usb_gp_btn"),
    ("XB_MENU", "XB Menu Button", "usb_gp_btn"),
    ("XB_SHARE", "XB Share Button", "usb_gp_btn"),
    ("XB_LOGO", "XB Xbox Button", "usb_gp_btn"),
    ("XB_LSX", "XB L-Stick X", "usb_abs_axis"),
    ("XB_LSY", "XB L-Stick Y", "usb_abs_axis"),
    ("XB_RSX", "XB R-Stick X", "usb_abs_axis"),
    ("XB_RSY", "XB R-Stick Y", "usb_abs_axis"),
    ("XB_LT", "XB LT Analog Trigger", "usb_abs_axis"),
    ("XB_RT", "XB RT Analog Trigger", "usb_abs_axis"),
    ("XB_DPX", "XB D-pad X", "usb_abs_axis"),
    ("XB_DPY", "XB D-pad Y", "usb_abs_axis")]

ps_code_list = [("PS_CROSS","PS Cross Button","usb_gp_btn"),
    ("PS_CIRCLE","PS Circle Button","usb_gp_btn"),
    ("PS_SQUARE","PS Square Button","usb_gp_btn"),
    ("PS_TRIANGLE","PS Triangle Button","usb_gp_btn"),
    ("PS_L1","PS L1 Button","usb_gp_btn"),
    ("PS_R1","PS R1 Button","usb_gp_btn"),
    ("PS_L2_BUTTON","PS L2 Button","usb_gp_btn"),
    ("PS_R2_BUTTON","PS R2 Button","usb_gp_btn"),
    ("PS_CREATE","PS Create Button","usb_gp_btn"),
    ("PS_OPTION","PS Option Button","usb_gp_btn"),
    ("PS_LOGO","PS Playstation Button","usb_gp_btn"),
    ("PS_MUTE","PS Mute Button","usb_gp_btn"),
    ("PS_TOUCHPAD_BUTTON","PS Touchpad Button","usb_gp_btn"),
    ("PS_LSB","PS L-Stick Button","usb_gp_btn"),
    ("PS_RSB","PS R-Stick Button","usb_gp_btn"),
    ("PS_LSX","PS L-Stick X","usb_abs_axis"),
    ("PS_LSY","PS L-Stick Y","usb_abs_axis"),
    ("PS_RSX","PS R-Stick X","usb_abs_axis"),
    ("PS_RSY","PS R-Stick Y","usb_abs_axis"),
    ("PS_L2_ANALOG","PS L2 Analog Trigger","usb_abs_axis"),
    ("PS_R2_ANALOG","PS R2 Analog Trigger","usb_abs_axis"),
    ("PS_DPX","PS D-pad X","usb_abs_axis"),
    ("PS_DPY","PS D-pad Y","usb_abs_axis")]

# code, display name, type
kb_code_list = [("KEY_1", "KEY_1", "kb_key"), ("KEY_2", "KEY_2", "kb_key"), ("KEY_3", "KEY_3", "kb_key"), ("KEY_4", "KEY_4", "kb_key"), ("KEY_5", "KEY_5", "kb_key"), ("KEY_6", "KEY_6", "kb_key"), ("KEY_7", "KEY_7", "kb_key"), ("KEY_8", "KEY_8", "kb_key"), ("KEY_9", "KEY_9", "kb_key"), ("KEY_0", "KEY_0", "kb_key"), ("KEY_A", "KEY_A", "kb_key"), ("KEY_B", "KEY_B", "kb_key"), ("KEY_C", "KEY_C", "kb_key"), ("KEY_D", "KEY_D", "kb_key"), ("KEY_E", "KEY_E", "kb_key"), ("KEY_F", "KEY_F", "kb_key"), ("KEY_G", "KEY_G", "kb_key"), ("KEY_H", "KEY_H", "kb_key"), ("KEY_I", "KEY_I", "kb_key"), ("KEY_J", "KEY_J", "kb_key"), ("KEY_K", "KEY_K", "kb_key"), ("KEY_L", "KEY_L", "kb_key"), ("KEY_M", "KEY_M", "kb_key"), ("KEY_N", "KEY_N", "kb_key"), ("KEY_O", "KEY_O", "kb_key"), ("KEY_P", "KEY_P", "kb_key"), ("KEY_Q", "KEY_Q", "kb_key"), ("KEY_R", "KEY_R", "kb_key"), ("KEY_S", "KEY_S", "kb_key"), ("KEY_T", "KEY_T", "kb_key"), ("KEY_U", "KEY_U", "kb_key"), ("KEY_V", "KEY_V", "kb_key"), ("KEY_W", "KEY_W", "kb_key"), ("KEY_X", "KEY_X", "kb_key"), ("KEY_Y", "KEY_Y", "kb_key"), ("KEY_Z", "KEY_Z", "kb_key"), ("KEY_SPACE", "KEY_SPACE", "kb_key"), ("KEY_UP", "KEY_UP", "kb_key"), ("KEY_DOWN", "KEY_DOWN", "kb_key"), ("KEY_LEFT", "KEY_LEFT", "kb_key"), ("KEY_RIGHT", "KEY_RIGHT", "kb_key"), ("KEY_ESC", "KEY_ESC", "kb_key"), ("KEY_TAB", "KEY_TAB", "kb_key"), ("KEY_ENTER", "KEY_ENTER", "kb_key"), ("KEY_END", "KEY_END", "kb_key"), ("KEY_HOME", "KEY_HOME", "kb_key"), ("KEY_LEFTALT", "KEY_LEFTALT", "kb_key"), ("KEY_LEFTCTRL", "KEY_LEFTCTRL", "kb_key"), ("KEY_LEFTSHIFT", "KEY_LEFTSHIFT", "kb_key"), ("KEY_RIGHTALT", "KEY_RIGHTALT", "kb_key"), ("KEY_RIGHTCTRL", "KEY_RIGHTCTRL", "kb_key"), ("KEY_RIGHTSHIFT", "KEY_RIGHTSHIFT", "kb_key"), ("KEY_SCROLLLOCK", "KEY_SCROLLLOCK", "kb_key"), ("KEY_SYSRQ", "KEY_SYSRQ", "kb_key"), ("KEY_PAGEUP", "KEY_PAGEUP", "kb_key"), ("KEY_PAGEDOWN", "KEY_PAGEDOWN", "kb_key"), ("KEY_INSERT", "KEY_INSERT", "kb_key"), ("KEY_DELETE", "KEY_DELETE", "kb_key"), ("KEY_102ND", "KEY_102ND", "kb_key"), ("KEY_CAPSLOCK", "KEY_CAPSLOCK", "kb_key"), ("KEY_NUMLOCK", "KEY_NUMLOCK", "kb_key"), ("KEY_MINUS", "KEY_MINUS", "kb_key"), ("KEY_EQUAL", "KEY_EQUAL", "kb_key"), ("KEY_BACKSPACE", "KEY_BACKSPACE", "kb_key"), ("KEY_LEFTBRACE", "KEY_LEFTBRACE", "kb_key"), ("KEY_RIGHTBRACE", "KEY_RIGHTBRACE", "kb_key"), ("KEY_SEMICOLON", "KEY_SEMICOLON", "kb_key"), ("KEY_APOSTROPHE", "KEY_APOSTROPHE", "kb_key"), ("KEY_GRAVE", "KEY_GRAVE", "kb_key"), ("KEY_BACKSLASH", "KEY_BACKSLASH", "kb_key"), ("KEY_COMMA", "KEY_COMMA", "kb_key"), ("KEY_DOT", "KEY_DOT", "kb_key"), ("KEY_SLASH", "KEY_SLASH", "kb_key"), ("KEY_F1", "KEY_F1", "kb_key"), ("KEY_F2", "KEY_F2", "kb_key"), ("KEY_F3", "KEY_F3", "kb_key"), ("KEY_F4", "KEY_F4", "kb_key"), ("KEY_F5", "KEY_F5", "kb_key"), ("KEY_F6", "KEY_F6", "kb_key"), ("KEY_F7", "KEY_F7", "kb_key"), ("KEY_F8", "KEY_F8", "kb_key"), ("KEY_F9", "KEY_F9", "kb_key"), ("KEY_F10", "KEY_F10", "kb_key"), ("KEY_F11", "KEY_F11", "kb_key"), ("KEY_F12", "KEY_F12", "kb_key"), ("KEY_F13", "KEY_F13", "kb_key"), ("KEY_F14", "KEY_F14", "kb_key"), ("KEY_F15", "KEY_F15", "kb_key"), ("KEY_F16", "KEY_F16", "kb_key"), ("KEY_F17", "KEY_F17", "kb_key"), ("KEY_F18", "KEY_F18", "kb_key"), ("KEY_F19", "KEY_F19", "kb_key"), ("KEY_F20", "KEY_F20", "kb_key"), ("KEY_F21", "KEY_F21", "kb_key"), ("KEY_F22", "KEY_F22", "kb_key"), ("KEY_F23", "KEY_F23", "kb_key"), ("KEY_F24", "KEY_F24", "kb_key"), ("KEY_KP0", "KEY_KP0", "kb_key"), ("KEY_KP1", "KEY_KP1", "kb_key"), ("KEY_KP2", "KEY_KP2", "kb_key"), ("KEY_KP3", "KEY_KP3", "kb_key"), ("KEY_KP4", "KEY_KP4", "kb_key"), ("KEY_KP5", "KEY_KP5", "kb_key"), ("KEY_KP6", "KEY_KP6", "kb_key"), ("KEY_KP7", "KEY_KP7", "kb_key"), ("KEY_KP8", "KEY_KP8", "kb_key"), ("KEY_KP9", "KEY_KP9", "kb_key"), ("KEY_KPASTERISK", "KEY_KPASTERISK", "kb_key"), ("KEY_KPDOT", "KEY_KPDOT", "kb_key"), ("KEY_KPENTER", "KEY_KPENTER", "kb_key"), ("KEY_KPMINUS", "KEY_KPMINUS", "kb_key"), ("KEY_KPPLUS", "KEY_KPPLUS", "kb_key"), ("KEY_KPSLASH", "KEY_KPSLASH", "kb_key")]

# code, display name, type
mouse_code_list = [("BTN_LEFT", "Mouse Left", "mouse_btn"),
    ("BTN_RIGHT", "Mouse Right", "mouse_btn"),
    ("BTN_MIDDLE", "Mouse Middle", "mouse_btn"),
    ("BTN_SIDE", "Mouse Side", "mouse_btn"),
    ("BTN_EXTRA", "Mouse Extra", "mouse_btn"),
    ("REL_X", "Mouse X", "usb_rel_axis"),
    ("REL_Y", "Mouse Y", "usb_rel_axis"),
    ("REL_Z", "Mouse Scroll", "usb_rel_axis")]

# code, display name, type
ibm_15pin_gamepad_code_list = [('IBM_GGP_BTN_1', '15P Button 1', 'ibm_ggp_btn'),
    ('IBM_GGP_BTN_2', '15P Button 2', 'ibm_ggp_btn'),
    ('IBM_GGP_BTN_3', '15P Button 3', 'ibm_ggp_btn'),
    ('IBM_GGP_BTN_4', '15P Button 4', 'ibm_ggp_btn'),
    ('IBM_GGP_JS1_X', '15P JS1 X-Axis', 'ibm_ggp_axis'),
    ('IBM_GGP_JS1_Y', '15P JS1 Y-Axis', 'ibm_ggp_axis'),
    ('IBM_GGP_JS2_X', '15P JS2 X-Axis', 'ibm_ggp_axis'),
    ('IBM_GGP_JS2_Y', '15P JS2 Y-Axis', 'ibm_ggp_axis'),
    ('IBM_GGP_JS1_XP', '15P JS1 Positive X', 'ibm_ggp_half_axis'),
    ('IBM_GGP_JS1_XN', '15P JS1 Negative X', 'ibm_ggp_half_axis'),
    ('IBM_GGP_JS1_YP', '15P JS1 Positive Y', 'ibm_ggp_half_axis'),
    ('IBM_GGP_JS1_YN', '15P JS1 Negative Y', 'ibm_ggp_half_axis'),
    ('IBM_GGP_JS2_XP', '15P JS2 Positive X', 'ibm_ggp_half_axis'),
    ('IBM_GGP_JS2_XN', '15P JS2 Negative X', 'ibm_ggp_half_axis'),
    ('IBM_GGP_JS2_YP', '15P JS2 Positive Y', 'ibm_ggp_half_axis'),
    ('IBM_GGP_JS2_YN', '15P JS2 Negative Y', 'ibm_ggp_half_axis')]

all_codes_list = generic_usb_gamepad_code_list + xbox_code_list + ps_code_list + kb_code_list + mouse_code_list + ibm_15pin_gamepad_code_list

def get_gamepad_type():
    profile_selection = profile_lstbox.curselection()
    if len(profile_selection) <= 0:
        return None
    return gamepad_mapping_dict_list[profile_selection[0]].get('usb_gamepad_type', "Xbox")

def get_lookup_prefix():
    this_gamepad_type = get_gamepad_type()
    display_name_prefix = ''
    if 'Xbox'.lower() in this_gamepad_type.lower():
        display_name_prefix = 'XB '
    elif 'PlayStation'.lower() in this_gamepad_type.lower():
        display_name_prefix = 'PS '
    return display_name_prefix

def tuple_list_search_by_displayname(tup_list, query, prefix=''):
    for item in tup_list:
        if prefix + str(query) == item[1]:
            return item
    return None, None, None

def tuple_list_search_by_codename(tup_list, query):
    for item in tup_list:
        if query == item[0]:
            return item
    return None, None, None

def create_mapping_window(existing_rule=None):
    def validate_dropdown_menus(event):
        map_from_selected_option = map_from_option_var.get()
        map_category_selected_option = map_to_category_option_var.get()
        this_code, this_display_name, this_type = tuple_list_search_by_displayname(xbox_code_list + ps_code_list + generic_usb_gamepad_code_list, map_from_selected_option, get_lookup_prefix())
        if this_code is None:
            return
        secondary_map_to_code_dropdown.set('')
        map_to_code_dropdown.set('')
        secondary_map_to_code_dropdown['values'] = []
        secondary_map_to_code_dropdown.config(state=DISABLED)
        if this_type == 'usb_gp_btn':
            """
            usb gamepad buttons can be mapped to:
            keyboard key
            mouse button
            15-pin gamepad buttons
            15-pin gamepad half axes
            """
            if map_category_selected_option == "Keyboard":
                map_to_code_dropdown['values'] = [x[1] for x in kb_code_list if x[2] == 'kb_key']
            elif map_category_selected_option == "Mouse":
                map_to_code_dropdown['values'] = [x[1] for x in mouse_code_list if x[2] == 'mouse_btn']
            elif map_category_selected_option == "15-Pin Gamepad":
                map_to_code_dropdown['values'] = [x[1] for x in ibm_15pin_gamepad_code_list if x[2] == 'ibm_ggp_btn' or x[2] == 'ibm_ggp_half_axis']

        if this_type == 'usb_abs_axis':
            """
            usb gamepad axes can be mapped to:
            keyboard key
            mouse axes
            15-pin gamepad axes
            15-pin gamepad half axes (for xbox controller analog trigger only)
            """
            if map_category_selected_option == "Keyboard":
                map_to_code_dropdown['values'] = [x[1] for x in kb_code_list if x[2] == 'kb_key']
                # ENABLE SECOND DROPDOWN HERE
                secondary_map_to_code_dropdown.config(state=NORMAL)
                secondary_map_to_code_dropdown['values'] = [x[1] for x in kb_code_list if x[2] == 'kb_key']
            elif map_category_selected_option == "Mouse":
                map_to_code_dropdown['values'] = [x[1] for x in mouse_code_list if x[2] == 'usb_rel_axis']
            elif map_category_selected_option == "15-Pin Gamepad":
                map_to_code_dropdown['values'] = [x[1] for x in ibm_15pin_gamepad_code_list if x[2] == 'ibm_ggp_axis' or x[2] == 'ibm_ggp_half_axis']

    profile_selection = profile_lstbox.curselection()
    if len(profile_selection) <= 0:
        return
    pboard_type = gamepad_mapping_dict_list[profile_selection[0]].get('protocol_board', "IBMPC")
    usb_gamepad_type = gamepad_mapping_dict_list[profile_selection[0]].get('usb_gamepad_type', "Xbox")

    rule_window = Toplevel(root)
    rule_window.title("Edit rules")
    rule_window.geometry("400x210")
    rule_window.resizable(width=FALSE, height=FALSE)
    rule_window.grab_set()

    map_from_label = Label(master=rule_window, text="Map From:")
    map_from_label.place(x=10, y=10)

    map_to_label = Label(master=rule_window, text="Map To:")
    map_to_label.place(x=10, y=50)

    # test
    current_gamepad_code_list = generic_usb_gamepad_code_list
    if 'xbox'.lower() in usb_gamepad_type.lower():
        current_gamepad_code_list = [str(x[1]).partition('XB ')[2] for x in xbox_code_list]
    elif 'PlayStation'.lower() in usb_gamepad_type.lower():
        current_gamepad_code_list = [str(x[1]).partition('PS ')[2] for x in ps_code_list]
    else:
        current_gamepad_code_list = [str(x[1]) for x in current_gamepad_code_list]

    map_from_option_var = StringVar()
    map_from_option_var.set(current_gamepad_code_list[0])
    map_from_dropdown = OptionMenu(rule_window, map_from_option_var, command=validate_dropdown_menus, *current_gamepad_code_list)
    map_from_dropdown.place(x=100, y=5, width=250)

    map_to_category_list = ["Keyboard", "Mouse"]
    if 'ibmpc' in pboard_type.lower():
        map_to_category_list.append("15-Pin Gamepad")

    map_to_category_option_var = StringVar()
    map_to_category_option_var.set(map_to_category_list[0])
    map_to_category_dropdown = OptionMenu(rule_window, map_to_category_option_var, command=validate_dropdown_menus, *map_to_category_list)
    map_to_category_dropdown.place(x=100, y=45, width=250)

    map_to_code_dropdown = ttk.Combobox(rule_window)
    map_to_code_dropdown.place(x=100, y=80, width=250)

    secondary_map_to_code_dropdown = ttk.Combobox(rule_window, state=DISABLED)
    secondary_map_to_code_dropdown.place(x=100, y=110, width=250)

    def close_map_window():
        update_profile_display()
        rule_window.destroy()

    def save_this_mapping():
        selection = profile_lstbox.curselection()
        if len(selection) <= 0:
            return
        map_from_code, map_from_display_name, map_from_type = tuple_list_search_by_displayname(all_codes_list, map_from_option_var.get(), get_lookup_prefix())
        map_to_code1, map_to_display_name1, map_to_type1 = tuple_list_search_by_displayname(all_codes_list, map_to_code_dropdown.get())
        map_to_code2, map_to_display_name2, map_to_type2 = tuple_list_search_by_displayname(all_codes_list, secondary_map_to_code_dropdown.get())
        
        print(map_from_option_var.get(), map_from_code, map_from_display_name, map_from_type)
        print(map_to_code_dropdown.get(), map_to_code1, map_to_display_name1, map_to_type1)

        if map_from_code is None:
            return
        this_map_dict = {'code':map_to_code1}
        if map_to_code2 is not None:
            this_map_dict['code'] = map_to_code2
            this_map_dict['code_neg'] = map_to_code1
        gamepad_mapping_dict_list[selection[0]]['mapping'][map_from_code] = this_map_dict
        update_profile_display()

    map_save_button = Button(rule_window, text="Add This Mapping", command=save_this_mapping)
    map_save_button.place(x=10, y=140, width=380, height=25)
    validate_dropdown_menus(None)

    map_cancel_button = Button(rule_window, text="Exit", command=close_map_window)
    map_cancel_button.place(x=10, y=175, width=380, height=25)

def profile_add_click():
    answer = simpledialog.askstring("Input", "New profile name?", parent=profiles_lf)
    if answer is None:
        return
    answer = clean_input(answer, len_limit=20)
    if len(answer) == 0:
        return
    this_mapping = {'display_name': answer, 'device_type': 'protocol_list_gamepad', 'usb_gamepad_type':'Xbox', 'protocol_board': 'IBMPC', 'protocol_name': 'GAMEPORT_15PIN_GAMEPAD', 'mapping': {}}
    gamepad_mapping_dict_list.append(this_mapping)
    update_profile_display()
    profile_lstbox.selection_clear(0, len(gamepad_mapping_dict_list))
    profile_lstbox.selection_set(len(gamepad_mapping_dict_list)-1)
    update_profile_display()

def profile_remove_click():
    selection = profile_lstbox.curselection()
    if len(selection) <= 0:
        return
    gamepad_mapping_dict_list.pop(selection[0])
    update_profile_display()
    profile_lstbox.selection_clear(0, len(gamepad_mapping_dict_list))
    profile_lstbox.selection_set(selection[0])
    if len(gamepad_mapping_dict_list) <= 0 or len(profile_lstbox.curselection()) <= 0:
        mapping_add_button.config(state=DISABLED)
        mapping_remove_button.config(state=DISABLED)
        pboard_dropdown.config(state=DISABLED)
        usb_gamepad_dropdown.config(state=DISABLED)
        mappings_var.set([])
    update_profile_display()

def profile_rename_click():
    selection = profile_lstbox.curselection()
    if len(selection) <= 0:
        return
    answer = simpledialog.askstring("Input", "New name?", parent=profiles_lf, initialvalue=gamepad_mapping_dict_list[selection[0]].get('display_name', 'None'))
    if answer is None:
        return
    answer = clean_input(answer, len_limit=20)
    if len(answer) == 0:
        return
    gamepad_mapping_dict_list[selection[0]]['display_name'] = answer
    update_profile_display()

def profile_dupe_click():
    selection = profile_lstbox.curselection()
    if len(selection) <= 0:
        return
    answer = simpledialog.askstring("Input", "New name?", parent=profiles_lf, initialvalue=gamepad_mapping_dict_list[selection[0]].get('display_name', 'None'))
    if answer is None:
        return
    answer = clean_input(answer, len_limit=20)
    if len(answer) == 0:
        return
    new_profile = copy.deepcopy(gamepad_mapping_dict_list[selection[0]])
    new_profile['display_name'] = answer
    gamepad_mapping_dict_list.insert(selection[0] + 1, new_profile)
    update_profile_display()

def mapping_remove_click():
    profile_index = profile_lstbox.curselection()
    if len(profile_index) <= 0:
        return
    profile_index = profile_index[0]

    mapping_index = mappings_lstbox.curselection()
    if len(mapping_index) <= 0:
        return
    mapping_index = mapping_index[0]

    key_to_delete = list(gamepad_mapping_dict_list[profile_index]['mapping'].keys())[mapping_index]
    gamepad_mapping_dict_list[profile_index]['mapping'].pop(key_to_delete, None)
    update_profile_display()

def make_default_backup_dir_name():
    return 'usb4vc_backup_' + datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

def save_mapping_to_file():
    # check if target is same as temp
    this_backup_dir = os.path.join(backup_path, make_default_backup_dir_name())
    ensure_dir(this_backup_dir)

    for item in gamepad_mapping_dict_list:
        filename = clean_input(f'usb4vc_map_{item["display_name"]}_{item["protocol_board"]}.json', clean_filename=True).lower()
        backup_dest = os.path.join(this_backup_dir, filename)
        try:
            with open(backup_dest, 'w', encoding='utf-8') as save_file:
                save_file.write(json.dumps(item, sort_keys=True))
        except Exception as e:
            messagebox.showerror("Error", "Saving Backup Failed!\n\n"+str(e))

    ensure_dir(flash_drive_config_path)
    file_list = [d for d in os.listdir(flash_drive_config_path) if d.startswith("usb4vc_map") and d.lower().endswith(".json")]
    for item in file_list:
        try:
            os.remove(os.path.join(flash_drive_config_path, item))
        except Exception:
            continue
        time.sleep(0.05)

    for item in gamepad_mapping_dict_list:
        filename = clean_input(f'usb4vc_map_{item["display_name"]}_{item["protocol_board"]}.json', clean_filename=True).lower()
        save_dest = os.path.join(flash_drive_config_path, filename)
        try:
            print('writing:', save_dest, item)
            with open(save_dest, 'w', encoding='utf-8') as save_file:
                save_file.write(json.dumps(item, sort_keys=True))
        except Exception as e:
            messagebox.showerror("Error", "Saving to Flash Drive Failed!\n\n"+str(e))
            return
    messagebox.showinfo("Save", "Success!")

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 25

profile_add_button = Button(profiles_lf, text="New", command=profile_add_click, state=DISABLED)
profile_add_button.place(x=10, y=290, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

profile_dupe_button = Button(profiles_lf, text="Duplicate", command=profile_dupe_click, state=DISABLED)
profile_dupe_button.place(x=10, y=320, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

profile_rename_button = Button(profiles_lf, text="Rename", command=profile_rename_click, state=DISABLED)
profile_rename_button.place(x=10, y=350, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

profile_remove_button = Button(profiles_lf, text="Remove", command=profile_remove_click, state=DISABLED)
profile_remove_button.place(x=10, y=380, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_add_button = Button(mappings_lf, text="New", command=create_mapping_window, state=DISABLED)
mapping_add_button.place(x=20, y=350, width=330, height=BUTTON_HEIGHT)

mapping_remove_button = Button(mappings_lf, text="Remove", command=mapping_remove_click, state=DISABLED)
mapping_remove_button.place(x=20, y=380, width=330, height=BUTTON_HEIGHT)

mapping_save_button = Button(gamepad_config_lf, text="Write Current Mappings to Flash Drive", command=save_mapping_to_file, state=DISABLED, fg='red')
mapping_save_button.place(x=10, y=447, width=755, height=BUTTON_HEIGHT)

def enable_profile_buttons():
    copy_button.config(state=NORMAL)
    profile_add_button.config(state=NORMAL)
    profile_remove_button.config(state=NORMAL)
    profile_rename_button.config(state=NORMAL)
    profile_dupe_button.config(state=NORMAL)
    mapping_save_button.config(state=NORMAL)

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
    enable_profile_buttons()

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

def pboard_dropdown_change(event):
    selection = profile_lstbox.curselection()
    if len(selection) <= 0:
        return
    gamepad_mapping_dict_list[selection[0]]['protocol_board'] = pboard_option_var.get()
    if gamepad_mapping_dict_list[selection[0]]['protocol_board'] == 'IBMPC':
        gamepad_mapping_dict_list[selection[0]]['protocol_name'] = 'GAMEPORT_15PIN_GAMEPAD'
    else:
        gamepad_mapping_dict_list[selection[0]]['protocol_name'] = 'OFF'
    update_profile_display()

def usb_gamepad_dropdown_change(event):
    selection = profile_lstbox.curselection()
    if len(selection) <= 0:
        return
    gamepad_mapping_dict_list[selection[0]]['usb_gamepad_type'] = usb_gamepad_option_var.get()
    update_profile_display()

protocol_board_dropdown_label = Label(master=options_lf, text="Protocol Card:")
protocol_board_dropdown_label.place(x=10, y=5)
protocol_board_list = ['Unknown', 'IBMPC', "ADB"]
pboard_option_var = StringVar()
pboard_option_var.set(protocol_board_list[0])
pboard_dropdown = OptionMenu(options_lf, pboard_option_var, command=pboard_dropdown_change, *protocol_board_list)
pboard_dropdown.place(x=10, y=30, width=150)
pboard_dropdown.config(state=DISABLED)

usb_gamepad_type_dropdown_label = Label(master=options_lf, text="Gamepad Type:")
usb_gamepad_type_dropdown_label.place(x=10, y=80)
usb_gamepad_list = ['Xbox', 'PlayStation', 'Generic USB']
usb_gamepad_option_var = StringVar()
usb_gamepad_option_var.set(usb_gamepad_list[1])
usb_gamepad_dropdown = OptionMenu(options_lf, usb_gamepad_option_var, command=usb_gamepad_dropdown_change, *usb_gamepad_list)
usb_gamepad_dropdown.place(x=10, y=100, width=150)
usb_gamepad_dropdown.config(state=DISABLED)

select_root_folder('C:/Users/allen/Desktop/flashdrive_test')

root.update()
root.mainloop()
