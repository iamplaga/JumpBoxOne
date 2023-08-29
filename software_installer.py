# install_software.py

import subprocess

def install_package(package_name):
    try:
        print(f"Installing {package_name}...")
        subprocess.run(['sudo', 'apt-get', 'install', package_name, '-y'])
        print(f"{package_name} installed successfully.")
    except Exception as e:
        print(f"Error installing {package_name}: {e}")

# You can add more functions to install other features here
