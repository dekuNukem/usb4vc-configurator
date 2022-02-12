try:
    with open(save_filename) as json_file:
        temp = json.load(json_file)
        if isinstance(temp, dict):
            config_dict = temp
        else:
            raise ValueError("not a valid config file")
except Exception as e:
    pass

            # print(usb_gamepad_source, list(map_dict.values()))
            # print(f'{usb_gamepad_source}\t\tREL_X\t\tREL_Y')
usb_gamepad_source + ' '*gap1 + dest_name + '\n'


    map_to_code_list = list(ibm_15pin_code_dict.values())
    # map_to_code_option_var = StringVar()
    # map_to_code_option_var.set(map_to_code_list[0])
    # map_to_code_dropdown = OptionMenu(rule_window, map_to_code_option_var, *map_to_code_list)
    # map_to_code_dropdown.place(x=370, y=45, width=250)

profile_selection = profile_lstbox.curselection()
    if len(profile_selection) <= 0:
        return
    mapping_selection = mappings_lstbox.curselection()
    if len(mapping_selection) <= 0:
        return
    # print(profile_selection, mapping_selection)
    pboard_type = gamepad_mapping_dict_list[profile_selection[0]].get('protocol_board', "Unknown")
    usb_gamepad_type = gamepad_mapping_dict_list[profile_selection[0]].get('usb_gamepad_type', "Generic")
    # print(list(gamepad_mapping_dict_list[profile_selection[0]]['mapping'].values))

kb_code_unused = ["KEY_ZENKAKUHANKAKU", "KEY_RO", "KEY_KATAKANA", "KEY_HIRAGANA", "KEY_HENKAN", "KEY_KATAKANAHIRAGANA", "KEY_MUHENKAN", "KEY_MACRO", "KEY_MUTE", "KEY_VOLUMEDOWN", "KEY_VOLUMEUP", "KEY_POWER", "KEY_LINEFEED", "KEY_KPCOMMA", "KEY_KPEQUAL", "KEY_KPJPCOMMA", "KEY_KPLEFTPAREN", "KEY_KPRIGHTPAREN", "KEY_KPPLUSMINUS", "KEY_PAUSE", "KEY_SCALE", "KEY_HANGEUL", "KEY_HANGUEL", "KEY_HANJA", "KEY_YEN", "KEY_LEFTMETA", "KEY_RIGHTMETA", "KEY_COMPOSE", "KEY_STOP", "KEY_AGAIN", "KEY_PROPS", "KEY_UNDO", "KEY_FRONT", "KEY_COPY", "KEY_OPEN", "KEY_PASTE", "KEY_FIND", "KEY_CUT", "KEY_HELP", "KEY_MENU", "KEY_CALC", "KEY_SETUP", "KEY_SLEEP", "KEY_WAKEUP", "KEY_FILE", "KEY_SENDFILE", "KEY_DELETEFILE", "KEY_XFER", "KEY_PROG1", "KEY_PROG2", "KEY_WWW", "KEY_MSDOS", "KEY_COFFEE", "KEY_SCREENLOCK", "KEY_ROTATE_DISPLAY", "KEY_DIRECTION", "KEY_CYCLEWINDOWS", "KEY_MAIL", "KEY_BOOKMARKS", "KEY_COMPUTER", "KEY_BACK", "KEY_FORWARD", "KEY_CLOSECD", "KEY_EJECTCD", "KEY_EJECTCLOSECD", "KEY_NEXTSONG", "KEY_PLAYPAUSE", "KEY_PREVIOUSSONG", "KEY_STOPCD", "KEY_RECORD", "KEY_REWIND", "KEY_PHONE", "KEY_ISO", "KEY_CONFIG", "KEY_HOMEPAGE", "KEY_REFRESH", "KEY_EXIT", "KEY_MOVE", "KEY_EDIT", "KEY_SCROLLUP", "KEY_SCROLLDOWN", "KEY_NEW", "KEY_REDO"]
        # print(this_code, this_display_name, this_type)
            # print("THIS IS A BUTTON")
            # print("THIS IS AN AXIS")

def dict_reverse_lookup(my_dict, value_to_find):
    for key, value in my_dict.items():
        if value == value_to_find:
            return key
    return None

def map_to_category_dropdown_change(event):
        selected_option = map_to_category_option_var.get()
        if selected_option == "Keyboard"

    def map_from_dropdown_change(event):
        selected_option = map_from_option_var.get()
        lookup_result = dict_reverse_lookup({**xbox1_button_code_dict, **xbox1_axes_code_dict}, selected_option)
        if lookup_result is not None:
            selected_option = lookup_result
        if selected_option in list(xbox1_button_code_dict.keys()) + generic_usb_gamepad_buttons:
            print("THIS IS A BUTTON")
            """
            usb gamepad buttons can be mapped to:
            15-pin gamepad buttons
            15-pin gamepad half axes
            keyboard key
            mouse button
            """
        if selected_option in list(xbox1_axes_code_dict.keys()) + generic_usb_gamepad_axes:
            """
            usb gamepad axes can be mapped to:
            15-pin gamepad axes
            15-pin gamepad half axes (for xbox controller trigger only)
            keyboard key
            mouse axes
            """
            print("THIS IS AN AXIS")


def save_mapping_to_file():
    # check if target is same as temp
    print('----------')

    filename_set = set()
    for item in gamepad_mapping_dict_list:
        filename = clean_input(item['display_name'], len_limit=20, clean_filename=True).lower()
        
    for item in gamepad_mapping_dict_list:
        print(filename)
        print(json.dumps(item, sort_keys=True))


# temp_path = "C:\\Users\\allen\\AppData\\Roaming\\dekuNukem\\usb4vc_config\\temp"
# print(get_usb4vc_update(temp_path))