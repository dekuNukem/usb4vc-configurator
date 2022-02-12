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