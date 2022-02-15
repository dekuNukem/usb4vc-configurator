import os
import sys

if 'win32' not in sys.platform:
    print("this script is for windows only!")
    exit()

os.system('rm -rfv ./__pycache__')
os.system('rm -rfv ./build')
os.system('rm -rfv ./dist')
os.system('rm -rfv ./*.spec')

THIS_VERSION = None
try:
	mainfile = open('usb4vc_config.py')
	for line in mainfile:
		if "THIS_VERSION_NUMBER =" in line:
			THIS_VERSION = line.replace('\n', '').replace('\r', '').split("'")[-2]
	mainfile.close()
except Exception as e:
	print('build_windows exception:', e)
	exit()

if THIS_VERSION is None:
	print('could not find version number!')
	exit()

os.system("pyinstaller.exe --noconsole --icon=icon.ico usb4vc_config.py")

output_folder_path = os.path.join('.', "dist")
original_name = os.path.join(output_folder_path, "usb4vc_config")
new_name = os.path.join(output_folder_path, "usb4vc_config_" + THIS_VERSION + "_win10_x64")

print(original_name)
print(new_name)

os.rename(original_name, new_name)
zip_file_name = "usb4vc_config_" + THIS_VERSION + "_win10_x64.zip"
os.system('7z.exe a ' + zip_file_name + ' -r ' + new_name)

os.system('rm -rfv ./__pycache__')
os.system('rm -rfv ./build')
os.system('rm -rfv ./dist')
os.system('rm -rfv ./*.spec')