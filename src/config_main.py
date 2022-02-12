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

invalid_filename_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
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
    mapping_save_button.config(state=NORMAL)
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

generic_usb_gamepad_buttons = ["BTN_GAMEPAD", "BTN_SOUTH", "BTN_A", "BTN_EAST", "BTN_B", "BTN_C", "BTN_NORTH", "BTN_X", "BTN_WEST", "BTN_Y", "BTN_Z", "BTN_TL", "BTN_TR", "BTN_TL2", "BTN_TR2", "BTN_SELECT", "BTN_START", "BTN_MODE", "BTN_THUMBL", "BTN_THUMBR"]
generic_usb_gamepad_axes = ["ABS_X", "ABS_Y", "ABS_Z", "ABS_RX", "ABS_RY", "ABS_RZ", "ABS_THROTTLE", "ABS_RUDDER", "ABS_WHEEL", "ABS_GAS", "ABS_BRAKE", "ABS_HAT0X", "ABS_HAT0Y", "ABS_HAT1X", "ABS_HAT1Y", "ABS_HAT2X", "ABS_HAT2Y", "ABS_HAT3X", "ABS_HAT3Y"]

xbox1_button_code_dict = {
    "XB1_A":"A Button",
    "XB1_B":"B Button",
    "XB1_X":"X Button",
    "XB1_Y":"Y Button",
    "XB1_LSB":"Left Stick Button",
    "XB1_RSB":"Right Stick Button",
    "XB1_LB":"LB Button",
    "XB1_RB":"RB Button",
    "XB1_VIEW":"View Button",
    "XB1_MENU":"Menu Button",
    "XB1_LOGO":"Xbox Button",
}

xbox1_axes_code_dict = {
    "XB1_LSX":"Left Stick X",
    "XB1_LSY":"Left Stick Y",
    "XB1_RSX":"Right Stick X",
    "XB1_RSY":"Right Stick Y",
    "XB1_LT":"Left Trigger",
    "XB1_RT":"Right Trigger",
    "XB1_DPX":"D-pad X",
    "XB1_DPY":"D-pad Y",
}

kb_code_list = [ "KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5", "KEY_6", "KEY_7", "KEY_8", "KEY_9", "KEY_0", "KEY_A", "KEY_B", "KEY_C", "KEY_D", "KEY_E", "KEY_F", "KEY_G", "KEY_H", "KEY_I", "KEY_J", "KEY_K", "KEY_L", "KEY_M", "KEY_N", "KEY_O", "KEY_P", "KEY_Q", "KEY_R", "KEY_S", "KEY_T", "KEY_U", "KEY_V", "KEY_W", "KEY_X", "KEY_Y", "KEY_Z", "KEY_SPACE", "KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", "KEY_ESC", "KEY_TAB", "KEY_ENTER", "KEY_END", "KEY_HOME", "KEY_LEFTALT", "KEY_LEFTCTRL", "KEY_LEFTSHIFT", "KEY_RIGHTALT", "KEY_RIGHTCTRL", "KEY_RIGHTSHIFT", "KEY_SCROLLLOCK", "KEY_SYSRQ", "KEY_PAGEUP", "KEY_PAGEDOWN", "KEY_INSERT", "KEY_DELETE", "KEY_102ND", "KEY_CAPSLOCK", "KEY_NUMLOCK", "KEY_MINUS", "KEY_EQUAL", "KEY_BACKSPACE", "KEY_LEFTBRACE", "KEY_RIGHTBRACE", "KEY_SEMICOLON", "KEY_APOSTROPHE", "KEY_GRAVE", "KEY_BACKSLASH", "KEY_COMMA", "KEY_DOT", "KEY_SLASH", "KEY_F1", "KEY_F2", "KEY_F3", "KEY_F4", "KEY_F5", "KEY_F6", "KEY_F7", "KEY_F8", "KEY_F9", "KEY_F10", "KEY_F11", "KEY_F12", "KEY_F13", "KEY_F14", "KEY_F15", "KEY_F16", "KEY_F17", "KEY_F18", "KEY_F19", "KEY_F20", "KEY_F21", "KEY_F22", "KEY_F23", "KEY_F24", "KEY_KP0", "KEY_KP1", "KEY_KP2", "KEY_KP3", "KEY_KP4", "KEY_KP5", "KEY_KP6", "KEY_KP7", "KEY_KP8", "KEY_KP9", "KEY_KPASTERISK", "KEY_KPDOT", "KEY_KPENTER", "KEY_KPMINUS", "KEY_KPPLUS", "KEY_KPSLASH"]
kb_code_unused = ["KEY_ZENKAKUHANKAKU", "KEY_RO", "KEY_KATAKANA", "KEY_HIRAGANA", "KEY_HENKAN", "KEY_KATAKANAHIRAGANA", "KEY_MUHENKAN", "KEY_MACRO", "KEY_MUTE", "KEY_VOLUMEDOWN", "KEY_VOLUMEUP", "KEY_POWER", "KEY_LINEFEED", "KEY_KPCOMMA", "KEY_KPEQUAL", "KEY_KPJPCOMMA", "KEY_KPLEFTPAREN", "KEY_KPRIGHTPAREN", "KEY_KPPLUSMINUS", "KEY_PAUSE", "KEY_SCALE", "KEY_HANGEUL", "KEY_HANGUEL", "KEY_HANJA", "KEY_YEN", "KEY_LEFTMETA", "KEY_RIGHTMETA", "KEY_COMPOSE", "KEY_STOP", "KEY_AGAIN", "KEY_PROPS", "KEY_UNDO", "KEY_FRONT", "KEY_COPY", "KEY_OPEN", "KEY_PASTE", "KEY_FIND", "KEY_CUT", "KEY_HELP", "KEY_MENU", "KEY_CALC", "KEY_SETUP", "KEY_SLEEP", "KEY_WAKEUP", "KEY_FILE", "KEY_SENDFILE", "KEY_DELETEFILE", "KEY_XFER", "KEY_PROG1", "KEY_PROG2", "KEY_WWW", "KEY_MSDOS", "KEY_COFFEE", "KEY_SCREENLOCK", "KEY_ROTATE_DISPLAY", "KEY_DIRECTION", "KEY_CYCLEWINDOWS", "KEY_MAIL", "KEY_BOOKMARKS", "KEY_COMPUTER", "KEY_BACK", "KEY_FORWARD", "KEY_CLOSECD", "KEY_EJECTCD", "KEY_EJECTCLOSECD", "KEY_NEXTSONG", "KEY_PLAYPAUSE", "KEY_PREVIOUSSONG", "KEY_STOPCD", "KEY_RECORD", "KEY_REWIND", "KEY_PHONE", "KEY_ISO", "KEY_CONFIG", "KEY_HOMEPAGE", "KEY_REFRESH", "KEY_EXIT", "KEY_MOVE", "KEY_EDIT", "KEY_SCROLLUP", "KEY_SCROLLDOWN", "KEY_NEW", "KEY_REDO"]

mouse_button_code_dict = {
    "BTN_LEFT":"Left Button",
    "BTN_RIGHT":"Right Button",
    "BTN_MIDDLE":"Middle Button",
    "BTN_SIDE":"Side Button",
    "BTN_EXTRA":"Extra Button",
}

mouse_axes_code_dict = {
    "REL_X":"Mouse X",
    "REL_Y":"Mouse Y",
    "REL_Z":"Vertical Scroll",
}

ibm_15pin_button_code_dict = {
    'IBM_GGP_BTN_1':'Button 1',
    'IBM_GGP_BTN_2':'Button 2',
    'IBM_GGP_BTN_3':'Button 3',
    'IBM_GGP_BTN_4':'Button 4',
}

ibm_15pin_half_axes_code_dict = {
    'IBM_GGP_JS1_X':'Joystick 1 X Axis',
    'IBM_GGP_JS1_Y':'Joystick 1 Y Axis',
    'IBM_GGP_JS2_X':'Joystick 2 X Axis',
    'IBM_GGP_JS2_Y':'Joystick 2 Y Axis',
}

ibm_15pin_half_axes_code_dict = {
    'IBM_GGP_JS1_XP':'Joystick 1 Positive X',
    'IBM_GGP_JS1_XN':'Joystick 1 Negative X',
    'IBM_GGP_JS1_YP':'Joystick 1 Positive Y',
    'IBM_GGP_JS1_YN':'Joystick 1 Negative Y',
    'IBM_GGP_JS2_XP':'Joystick 2 Positive X',
    'IBM_GGP_JS2_XN':'Joystick 2 Negative X',
    'IBM_GGP_JS2_YP':'Joystick 2 Positive Y',
    'IBM_GGP_JS2_YN':'Joystick 2 Negative Y',
}

def dict_reverse_lookup(my_dict, value_to_find):
    for key, value in my_dict.items():
        if value == value_to_find:
            return key
    return None

def creat_mapping_window(existing_rule=None):
    def validate_dropdown_menus(event):
        map_from_selected_option = map_from_option_var.get()
        map_category_selected_option = map_to_category_option_var.get()

        lookup_result = dict_reverse_lookup({**xbox1_button_code_dict, **xbox1_axes_code_dict}, map_from_selected_option)
        if lookup_result is not None:
            map_from_selected_option = lookup_result
        if map_from_selected_option in list(xbox1_button_code_dict.keys()) + generic_usb_gamepad_buttons:
            print("THIS IS A BUTTON")
            """
            usb gamepad buttons can be mapped to:
            15-pin gamepad buttons
            15-pin gamepad half axes
            keyboard key
            mouse button
            """
            if map_category_selected_option == "Keyboard":
                map_to_code_dropdown['values'] = kb_code_list
            if map_category_selected_option == "Mouse":
                map_to_code_dropdown['values'] = mouse_button_code_dict

        if map_from_selected_option in list(xbox1_axes_code_dict.keys()) + generic_usb_gamepad_axes:
            """
            usb gamepad axes can be mapped to:
            15-pin gamepad axes
            15-pin gamepad half axes (for xbox controller trigger only)
            keyboard key
            mouse axes
            """
            print("THIS IS AN AXIS")

    profile_selection = profile_lstbox.curselection()
    if len(profile_selection) <= 0:
        return
    pboard_type = gamepad_mapping_dict_list[profile_selection[0]].get('protocol_board', "Unknown")
    usb_gamepad_type = gamepad_mapping_dict_list[profile_selection[0]].get('usb_gamepad_type', "Generic")

    rule_window = Toplevel(root)
    rule_window.title("Edit rules")
    rule_window.geometry("400x210")
    rule_window.resizable(width=FALSE, height=FALSE)
    rule_window.grab_set()

    map_from_label = Label(master=rule_window, text="Map From:")
    map_from_label.place(x=10, y=10)

    map_to_label = Label(master=rule_window, text="Map To:")
    map_to_label.place(x=10, y=50)

    current_gamepad_code_list = generic_usb_gamepad_buttons + generic_usb_gamepad_axes
    if 'xbox one' in usb_gamepad_type.lower():
        current_gamepad_code_list = list(xbox1_button_code_dict.values()) + list(xbox1_axes_code_dict.values())

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

    map_to_code_list = kb_code_list
    map_to_code_dropdown = ttk.Combobox(rule_window)
    map_to_code_dropdown.place(x=100, y=80, width=250)

    secondary_map_to_code_dropdown = ttk.Combobox(rule_window, state=DISABLED)
    secondary_map_to_code_dropdown.place(x=100, y=110, width=250)

    map_save_button = Button(rule_window, text="Save This Mapping", command=None, fg='red')
    map_save_button.place(x=10, y=140, width=380, height=25)
    validate_dropdown_menus()

    def close_map_window():
        rule_window.destroy()

    map_cancel_button = Button(rule_window, text="Cancel", command=close_map_window)
    map_cancel_button.place(x=10, y=175, width=380, height=25)

def profile_add_click():
    answer = simpledialog.askstring("Input", "New profile name?", parent=profiles_lf)
    if answer is None:
        return
    answer = clean_input(answer, len_limit=20)
    if len(answer) == 0:
        return
    this_mapping = {'display_name': answer, 'device_type': 'protocol_list_gamepad', 'gamepad_type':'Generic', 'protocol_board': 'Unknown', 'protocol_name': 'OFF', 'mapping': {}}
    gamepad_mapping_dict_list.append(this_mapping)
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
        mapping_edit_button.config(state=DISABLED)
        mapping_dupe_button.config(state=DISABLED)
        mapping_remove_button.config(state=DISABLED)
        mapping_save_button.config(state=DISABLED)
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

mapping_add_button = Button(mappings_lf, text="New", command=creat_mapping_window, state=DISABLED)
mapping_add_button.place(x=20, y=350, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_edit_button = Button(mappings_lf, text="Edit", command=None, state=DISABLED)
mapping_edit_button.place(x=200, y=350, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_dupe_button = Button(mappings_lf, text="Duplicate", command=None, state=DISABLED)
mapping_dupe_button.place(x=20, y=380, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_remove_button = Button(mappings_lf, text="Remove", command=None, state=DISABLED)
mapping_remove_button.place(x=200, y=380, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

mapping_save_button = Button(gamepad_config_lf, text="Write Current Mappings to Flash Drive", command=None, state=DISABLED, fg='red')
mapping_save_button.place(x=10, y=447, width=755, height=BUTTON_HEIGHT)

def enable_profile_buttons():
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

usb_gamepad_type_dropdown_label = Label(master=options_lf, text="USB Gamepad:")
usb_gamepad_type_dropdown_label.place(x=10, y=80)
usb_gamepad_list = ['Generic', 'Xbox One Wired', "Xbox One Bluetooth"]
usb_gamepad_option_var = StringVar()
usb_gamepad_option_var.set(usb_gamepad_list[0])
usb_gamepad_dropdown = OptionMenu(options_lf, usb_gamepad_option_var, command=usb_gamepad_dropdown_change, *usb_gamepad_list)
usb_gamepad_dropdown.place(x=10, y=100, width=150)
usb_gamepad_dropdown.config(state=DISABLED)

select_root_folder('C:/Users/allen/Desktop/flashdrive_test')

root.update()
root.mainloop()
