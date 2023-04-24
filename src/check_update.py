import os
import time
import json
import socket
import urllib.request
import requests
import zipfile
import shutil

usb4vc_release_url = "https://api.github.com/repos/dekuNukem/usb4vc/releases/latest"
usb4vc_configurator_release_url = "https://api.github.com/repos/dekuNukem/usb4vc-configurator/releases/latest"

def is_internet_available():
    try:
        socket.create_connection(("www.google.com", 80), timeout=1)
        return True
    except OSError:
        pass
    return False

def versiontuple(v):
    return tuple(map(int, (v.strip('v').split("."))))

"""
0 no update
1 has update
2+ unknown
"""
def get_pc_app_update_status(this_version):
    if is_internet_available() is False:
        return 2
    try:
        result_dict = json.loads(urllib.request.urlopen(usb4vc_configurator_release_url).read())
        this_version = versiontuple(this_version)
        remote_version = versiontuple(result_dict['tag_name'])
        return int(remote_version > this_version)
    except Exception as e:
        print('get_pc_app_update_status:', e)
        return 3
    return 4

# """
# 0 success
# >0 fail
# """
# def download_latest_usb4vc_release(save_path):
#     try:
#         if is_internet_available() is False:
#             return 1, 'Internet Unavailable'
#         result_dict = json.loads(urllib.request.urlopen(usb4vc_release_url).read())
#         header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',}
#         for item in result_dict['assets']:
#             if item['name'].lower().startswith('usb4vc_flashdrive_') and item['name'].lower().endswith('.zip'):
#                 zip_path = os.path.join(save_path, item['name'])
#                 with open(zip_path, 'wb') as out_file:
#                     content = requests.get(item['browser_download_url'], headers=header, timeout=5).content
#                     out_file.write(content)
#                 return 0, zip_path
#         return 2, 'No Update Found'
#     except Exception as e:
#         return 3, f'exception: {e}'
#     return 4, ''

# def unzip_file(zip_path, extract_path):
#     to_copy_path = os.path.join(extract_path, 'usb4vc')
#     try:
#         shutil.rmtree(to_copy_path)
#         time.sleep(0.1)
#     except Exception as e:
#         pass
#     try:
#         with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#             zip_ref.extractall(extract_path)
#     except Exception as e:
#         return 5, str(e) 
#     return 0, to_copy_path

# def get_usb4vc_update(temp_path):
#     rcode, msg = download_latest_usb4vc_release(temp_path)
#     if rcode != 0:
#         return rcode, msg
#     rcode, msg = unzip_file(msg, temp_path)
#     return rcode, msg
