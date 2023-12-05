import os
import psutil
import time
from win10toast import ToastNotifier
from tkinter import Tk, Label, Button, Entry, messagebox, Text, Toplevel, END
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import sys

# Global variables for settings
notification_interval = 10  # Default value in seconds
turn_off_delay = 60  # Default value in seconds

# Global variable to track the state of the charger connection
charger_connected_prev = psutil.sensors_battery().power_plugged

def show_notification(message):
    toaster = ToastNotifier()
    icon_path = 'icons8-connect-48.ico'
    toaster.show_toast("Uzi Battery Monitor 🩺🍂", message, duration=10, icon_path=icon_path)

def check_battery_and_update_gui():
    global charger_connected_prev

    while True:
        percent, power_plugged = check_battery_status()

        if percent is not None and power_plugged is not None:
            if not power_plugged:
                handle_unplugged_scenario(percent, power_plugged)
            else:
                if not charger_connected_prev:
                    show_notification("Charger Connected!")

            charger_connected_prev = power_plugged

        time.sleep(2)

def handle_unplugged_scenario(percent, power_plugged):
    show_notification(f"Charger Unplugged! Battery: {percent}%")
    elapsed_time = 0

    while not power_plugged and elapsed_time < turn_off_delay:
        time.sleep(10)
        elapsed_time += 10

        percent, power_plugged = check_battery_status()
        if power_plugged:
            show_notification("Charger reconnected. Resetting shutdown timer.")
            elapsed_time = 0

    if not power_plugged and elapsed_time >= turn_off_delay:
        shutdown_with_confirmation()
        print("Laptop would be turned off now.")
        show_notification("Shutdown canceled.")
        elapsed_time = 0

def check_battery_status():
    try:
        battery = psutil.sensors_battery()
        percent = battery.percent
        power_plugged = battery.power_plugged
        return percent, power_plugged
    except Exception as e:
        print(f"Error getting battery status: {e}")
        return None, None

def shutdown_with_confirmation():
    show_notification("Laptop will shut down in 1 minute. Click here to Cancel.")
    cancel_shutdown = messagebox.askyesno("Cancel Shutdown", "Do you want to cancel the shutdown?")

    if not cancel_shutdown:
        os.system("shutdown /s /t 60")

def create_info_notification():
    message = "This Program helps check when laptop charger disconnected🙄,if the user doesn't connect, it shuts down the laptop to save the user's battery."
    show_notification(message)

def minimize_to_tray(root, menu_icon):
    root.iconify()
    menu_icon.visible = True

def maximize_from_tray(root, menu_icon):
    root.deiconify()
    menu_icon.visible = False

def on_exit(root, icon, item):
    root.iconify()
    icon.stop()

def exit_program(icon, item):
    icon.stop()
    os._exit(0)



def create_system_tray_icon(root):
    icon_path = 'C:\\icons8-connect-48.ico' 

    menu = [
        item('Program Info', lambda icon, item: create_info_notification()),
        item('Exit Program', lambda icon, item: exit_program(menu_icon, item))
    ]
    image = Image.open(icon_path)

    menu_icon = pystray.Icon("Uzi Battery Monitor", image, "Uzi Battery Monitor", menu)
    menu_icon.visible = False

    root.protocol("WM_DELETE_WINDOW", lambda: minimize_to_tray(root, menu_icon))

    menu_icon.run()



if __name__ == "__main__":
    charger_connected_prev = psutil.sensors_battery().power_plugged
    battery_thread = threading.Thread(target=check_battery_and_update_gui, daemon=True)
    battery_thread.start()

    root = Tk()
    root.withdraw()  # Hide the main window initially

    create_system_tray_icon(root)
    root.mainloop()
