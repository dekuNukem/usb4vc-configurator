import json
import socket
import urllib.request
import requests

usb4vc_release_url = "https://api.github.com/repos/dekuNukem/usb4vc/releases/latest"

def is_internet_available():
    try:
        socket.create_connection(("www.google.com", 80), timeout=1)
        return True
    except OSError:
        pass
    return False

"""
0 success
1 fail
"""
def download_latest_usb4vc_release():
    if is_internet_available() is False:
        return 1, 'Internet Unavailable'
    result_dict = json.loads(urllib.request.urlopen(usb4vc_release_url).read())
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',}
    for item in result_dict['assets']:
        if item['name'].lower().startswith('usb4vc_rpi_img_') and item['name'].lower().endswith('.zip'):
            print(item['name'], item['browser_download_url'])
            with open(item['name'], 'wb') as out_file:
                content = requests.get(item['browser_download_url'], headers=header).content
                out_file.write(content)
            return 0, ''
    return 2, 'No Update Found'

print(download_latest_usb4vc_release())