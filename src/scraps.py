    if usb_gamepad_type == "Xbox One Bluetooth":
        for key in mapping_dict:
            lookup_result = xbox_one_bluetooth_to_linux_ev_code_dict.get(key)
            if lookup_result is not None:
                translated_map_dict[lookup_result] = mapping_dict[key]
        mapping_dict = translated_map_dict
    elif usb_gamepad_type == "Xbox One Wired":
        for key in mapping_dict:
            lookup_result = xbox_one_wired_to_linux_ev_code_dict.get(key)
            if lookup_result is not None:
                translated_map_dict[lookup_result] = mapping_dict[key]
        mapping_dict = translated_map_dict

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



        if source_type == 'usb_abs_axis' and target_type == 'kb_key':
            if source_code in analog_trigger_codes:
                pass
            else:
                if target_code not in curr_kb_output:
                    curr_kb_output[target_code] = set()
                is_activated = 0
                deadzone_amount = 50
                try:
                    deadzone_amount = int(127 * target_info['deadzone_percent'] / 100)
                except Exception:
                    pass
                if convert_to_8bit_midpoint127(this_gp_dict[source_code], axes_info, source_code) > 127 + deadzone_amount:
                    is_activated = 1
                curr_kb_output[target_code].add(is_activated)

                if target_info['code_neg'] not in curr_kb_output:
                    curr_kb_output[target_info['code_neg']] = set()
                is_activated = 0
                if convert_to_8bit_midpoint127(this_gp_dict[source_code], axes_info, source_code) < 127 - deadzone_amount:
                    is_activated = 1
                curr_kb_output[target_info['code_neg']].add(is_activated)


        # usb gamepad analog axes to mouse axes
        if source_type == 'usb_abs_axis' and target_type == 'usb_rel_axis' and target_code in curr_mouse_output:
            movement = convert_to_8bit_midpoint127(this_gp_dict[source_code], axes_info, source_code) - 127
            deadzone_amount = 20
            try:
                deadzone_amount = int(127 * target_info['deadzone_percent'] / 100)
            except Exception:
                pass
            if abs(movement) <= deadzone_amount:
                movement = 0
            joystick_to_mouse_slowdown = 20
            curr_mouse_output[target_code] = int(movement / joystick_to_mouse_slowdown)
            curr_mouse_output['is_modified'] = True
['axes_info']

    usb_gamepad_type = mapping_info.get('usb_gamepad_type', 'Generic USB')
