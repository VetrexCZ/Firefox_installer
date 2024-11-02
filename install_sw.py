from pathlib import Path
import urllib.request
import subprocess
import sys

def install_software(package):
    try:
        downloads_folder = Path.home() / "Downloads" # Saves file to the Downloads folder
        downloads_folder.mkdir(exist_ok=True) # If the folder does not exist, create it

        if package == "firefox":
            if sys.platform == "win32": # Script detect type of os
                print("Detected Windows OS.")
                url = "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US"
                installer_path = downloads_folder / "firefox_installer.exe"
            elif sys.platform == "darwin":
                print("Detected macOS.")
                url = "https://download.mozilla.org/?product=firefox-latest&os=osx&lang=en-US"
                installer_path = downloads_folder / "firefox_installer.dmg"
            elif sys.platform.startswith("linux"):
                print("Detected Linux OS.")
                print("Installing Firefox using package manager...")
                subprocess.check_call(["sudo", "apt", "install", "-y", "firefox"]) # Commands, Debia/Ubuntu
                return
            else:
                raise OSError("Unsupported OS For Firefox installation")

            # Download Firefox installer file
            print("Downloading Firefox from website...")
            urllib.request.urlretrieve(url, installer_path)
            print("Download completed")

            # Install Firefox
            if sys.platform == "win32":
                print("Starting silent install for Firefox on Windows...")
                subprocess.check_call([str(installer_path), "-ms"])  # Silent install on Windows
            elif sys.platform == "darwin":
                print("Mounting DMG for macOS installation...")
                subprocess.check_call(["hdiutil", "attach", str(installer_path)]) # Silent install on macOS
                print("Copying Firefox to Applications folder...")
                subprocess.check_call(["cp", "-r", "/Volumes/Firefox/Firefox.app", "/Applications"])
                subprocess.check_call(["hdiutil", "detach", "/Volumes/Firefox"]) # Silent install on Linux

        else:
            # Ensure pip is up to date
            print("Updating pip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            print(f"Installing Python package: {package}...")
            # Install Python package
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully.")

        print(f"Successfully installed {package}")
        print(f"Installation package is located in {downloads_folder}")

# Displays errors
    except subprocess.CalledProcessError as error:
        print(f"Subprocess failed with error: {error}")
    except Exception as error:
        print(f"An error occurred during installation of {package}: {error}")

# Test the subprocess functionality with a simple echo command
try:
    subprocess.check_call(["cmd", "/c", "echo", "Subprocess is working!"])
except Exception as ex:
    print(f"Error testing subprocess: {ex}")


# Calling a user function
install_software("firefox")
