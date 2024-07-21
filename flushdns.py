import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import time
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab

def flush_dns():
    update_log("flush_dns function called")  # Log message to confirm function call
    # Add new commands
    update_log("EXECUTING netsh int ip reset")
    subprocess.run(["netsh", "int", "ip", "reset"], capture_output=True, text=True)
    update_log("EXECUTING ipconfig /release")
    subprocess.run(["ipconfig", "/release"], capture_output=True, text=True)
    update_log("EXECUTING ipconfig /renew")
    subprocess.run(["ipconfig", "/renew"], capture_output=True, text=True)
    
    update_log("EXECUTING ipconfig /flushdns")
    result = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True)
    update_log(result.stdout)
    update_status("Flushing DNS, please wait...")
    update_log("Flushing DNS. FLUSHED " + str(flushed_count[0]) + " times")
    flushed_count[0] += 1
    update_log("FLUSHED DNS COOLDOWN IN PROGRESS.")

def detect_error_and_retry():
    template = cv2.imread(r'C:\Users\phamt\OneDrive - caugiay.edu.vn\DnsJumper\error_template.png', 0) #CHANGE TO LOCATION
    retry_button_template = cv2.imread(r'C:\Users\phamt\OneDrive - caugiay.edu.vn\DnsJumper\retry.png', 0)  # Load the image of the "Retry" button

    while is_running:
        update_log("Checking for HTTP error")  # Log message to indicate script is checking for HTTP error
        update_status("Checking HTTP error")
        screen = np.array(ImageGrab.grab())
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        if np.any(loc[0]):
            update_log("HTTP error detected, DNS FLUSHING COOLDOWN in progress")
            flush_dns()  # Call flush_dns function when HTTP error window is found

            # After flushing DNS, find the "Retry" button and click it
            res = cv2.matchTemplate(screen_gray, retry_button_template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            if np.any(loc[0]):
                # Get the position of the top-left corner of the "Retry" button
                top_left = (loc[1][0], loc[0][0])
                # Calculate the position of the center of the "Retry" button
                retry_button_position = (top_left[0] + retry_button_template.shape[1] // 2, top_left[1] + retry_button_template.shape[0] // 2)
                # Move the mouse to the "Retry" button and click it
                pyautogui.moveTo(retry_button_position)
                pyautogui.click()

        # Cooldown for 60 seconds
        for i in range(60, 0, -1):
            update_status(f"Cooldown in {i} seconds")
            time.sleep(1)


def start_flush():
    global is_running
    if not is_running:
        is_running = True
        update_log("Starting script")
        update_status("Starting script")
        threading.Thread(target=detect_error_and_retry, daemon=True).start()

def stop_flush():
    global is_running
    if is_running:
        is_running = False
        update_log("Stopping script")
        update_status("Stopping script")

def update_log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)  # Auto scroll to the bottom

def update_status(message):
    status_label.config(text=message)  # Assuming status_label is the name of your status label

root = tk.Tk()

log_box = scrolledtext.ScrolledText(root)
log_box.pack()

status_label = tk.Label(root, text="Status: Idle")
status_label.pack()

start_button = tk.Button(root, text="Start", command=start_flush)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_flush)
stop_button.pack()

is_running = False
flushed_count = [1]
cooldown = [60]

root.mainloop()
