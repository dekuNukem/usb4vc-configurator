def unzip_file(zip_path, extract_path):
    to_copy_path = os.path.join(extract_path, 'usb4vc')
    try:
        shutil.rmtree(to_copy_path)
        time.sleep(0.05)
    except Exception as e:
        pass
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except Exception as e:
        return 5, str(e) 
    return 0, to_copy_path


def unzip_file(zip_path, extract_path):
    base_path = os.path.join(extract_path, 'usb4vc')
    firmware_path = os.path.join(base_path, 'firmware')
    rpi_app_path = os.path.join(base_path, 'rpi_app')

    ensure_dir(base_path)
    try:
        shutil.rmtree(firmware_path)
        time.sleep(0.05)
        shutil.rmtree(rpi_app_path)
        time.sleep(0.05)
    except Exception as e:
        pass

    return 0, base_path