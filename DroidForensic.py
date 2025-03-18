#!/usr/bin/python3
import os
import re
import time
from subprocess import check_output, run, CalledProcessError
from colorama import Fore, Style, init
import art

# Initialize colorama for Windows compatibility
init(autoreset=True)

# Check if running on Linux/macOS
if os.name != "posix":
    print(Fore.RED + "\n[!] OS not supported... Exiting!" + Fore.RESET)
    exit()

# Clear screen
os.system('clear')

# Ensure 'Datas' directory exists
DATA_DIR = "Datas"
os.makedirs(DATA_DIR, exist_ok=True)

# Display banner
print(Fore.CYAN + art.text2art("DroidForensic"))
print(Fore.MAGENTA + "[+] DroidForensic: Advanced Mobile Forensic Framework" + Fore.RESET)
print(Fore.MAGENTA + "[+] Creator: @0xgh057r3c0n ( X )\n" + Fore.RESET)

# Features List
features = [
    "Dump Call Logs", "Dump SMS", "Dump Photos", "Dump Videos",
    "Dump Installed APKs", "Upload Files", "Dump Documents",
    "Extract information (passwords, emails) from documents"
]

print(Fore.YELLOW + "[x] Features:" + Fore.RESET)
for feature in features:
    print(Fore.BLUE + f"[*] {feature}" + Fore.RESET)

print(Fore.GREEN + "\n[x] Type 'help' or '?' to see available commands\n" + Fore.RESET)

# Device detection
print(Fore.YELLOW + "[-] Checking for connected device..." + Fore.RESET)
adb_output = check_output("adb devices -l", shell=True).decode()

if "model" in adb_output:
    device_name = re.search(r"device:\S+", adb_output)
    if device_name:
        print(Fore.GREEN + f"[✔] Device Detected: {device_name.group().split(':')[1]}" + Fore.RESET)
    else:
        print(Fore.GREEN + "[✔] Device Detected" + Fore.RESET)
    print()
else:
    print(Fore.RED + "\n[!] No mobile phone detected. Please connect a device and enable ADB debugging.\n" + Fore.RESET)
    exit()

# Function to display help menu
def show_help():
    print(Fore.YELLOW + "\n[!] Available Commands\n" + Fore.RESET)
    commands = {
        "clear": "Clear the screen",
        "dump_call_logs": "Extract call logs from the device",
        "dump_sms": "Extract SMS messages from the device",
        "dump_photos": "Download all images from the device",
        "dump_videos": "Download all videos from the device",
        "dump_downloads": "Download all files from the Downloads folder",
        "dump_in_apks": "Extract all installed APKs",
        "dump_documents": "Download all documents from the device",
        "exfil": "Extract information (passwords, emails) from documents",
        "exit / quit": "Exit DroidForensic"
    }
    
    for cmd, desc in commands.items():
        print(Fore.BLUE + f"[*] {cmd:<20}" + Fore.RESET + f" {desc}")

    print()

# Function to execute ADB commands
def run_adb_command(command, output_path, success_msg, error_msg):
    try:
        os.makedirs(output_path, exist_ok=True)
        check_output(command, shell=True)
        print(Fore.GREEN + f"[✔] {success_msg}" + Fore.RESET)
    except CalledProcessError:
        print(Fore.RED + f"[✘] {error_msg}" + Fore.RESET)

# Main command loop
try:
    while True:
        shell = input(Fore.CYAN + "[📂] DroidForensic >> " + Fore.RESET).strip().lower()

        if shell in ["help", "?"]:
            show_help()
        
        elif shell == "clear":
            os.system('clear')
        
        elif shell in ["exit", "quit"]:
            print(Fore.RED + "\n[!] Exiting... Goodbye!\n" + Fore.RESET)
            exit(0)

        elif shell == "dump_call_logs":
            run_adb_command("adb pull /data/data/com.android.providers.contacts/databases/calllog.db Datas/Call_Logs/",
                            "Datas/Call_Logs", "Call logs extracted!", "Failed to extract call logs.")

        elif shell == "dump_sms":
            run_adb_command("adb backup -noapk -f Datas/DroidForensic_sms.ab -nocompress com.android.providers.telephony",
                            "Datas/", "SMS backup completed! Extracting...", "Failed to extract SMS.")
            run_adb_command("mvt-android check-backup Datas/DroidForensic_sms.ab -o Datas/ && rm Datas/DroidForensic_sms.ab",
                            "Datas/", "SMS extracted successfully!", "Failed to extract SMS database.")

        elif shell == "dump_photos":
            run_adb_command("adb pull /sdcard/Pictures Datas/Pictures/",
                            "Datas/Pictures", "Photos downloaded!", "Failed to download photos.")

        elif shell == "dump_videos":
            run_adb_command("adb pull /sdcard/DCIM Datas/Videos/",
                            "Datas/Videos", "Videos downloaded!", "Failed to download videos.")

        elif shell == "dump_downloads":
            run_adb_command("adb pull /sdcard/Download Datas/Downloads/",
                            "Datas/Downloads", "Downloads extracted!", "Failed to extract downloads.")

        elif shell == "dump_in_apks":
            run_adb_command("adb shell pm list packages -f | cut -d ':' -f2 | cut -d '=' -f1 | xargs -I {} adb pull {} Datas/APKs/",
                            "Datas/APKs", "Installed APKs extracted!", "Failed to extract APKs.")

        elif shell == "dump_documents":
            run_adb_command("adb pull /sdcard/Documents Datas/Documents/",
                            "Datas/Documents", "Documents extracted!", "Failed to extract documents.")

        elif shell == "exfil":
            run_adb_command("python3 exfiltrate.py Datas/Documents/ -o Datas/Extracted_Info/",
                            "Datas/Extracted_Info", "Sensitive info extracted!", "Failed to extract sensitive info.")

        else:
            print(Fore.RED + "[✘] Unknown command. Type 'help' to see available commands." + Fore.RESET)

except KeyboardInterrupt:
    print(Fore.RED + "\n\n[!] User interrupted. Exiting...\n" + Fore.RESET)
    exit()
