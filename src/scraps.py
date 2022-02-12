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