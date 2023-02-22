import wmi
import time
import psutil
import os
import win32gui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont
import threading


def is_screen_off():
    """
    Check if the monitor screen is off or not using WMI.
    Returns:
        True if the screen is off, False otherwise.
    """
    c = wmi.WMI(namespace="root\WMI")
    try:
        power_state = c.WmiMonitorBasicDisplayParams()[0].Active
        bl_screen_is_off = False
    except IndexError:
        bl_screen_is_off = True
    return bl_screen_is_off


def check_network_speed():
    """
    Measure received bytes for 60 seconds and use the average to display network speed in KB/s.
    Returns:
        The network speed in KB/s.
    """
    interval = 10
    previous_bytes_recv = psutil.net_io_counters().bytes_recv
    previous_bytes_sent = psutil.net_io_counters().bytes_sent
    time.sleep(interval)
    # Check Download Speed and Upload Speed
    current_bytes_recv = psutil.net_io_counters().bytes_recv
    bytes_received = current_bytes_recv - previous_bytes_recv
    kbps_received = bytes_received / interval / 1024
    previous_bytes_recv = current_bytes_recv
    # Check Upload Speed
    current_bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_sent = current_bytes_sent - previous_bytes_sent
    kbps_sent = bytes_sent / interval / 1024
    previous_bytes_sent = current_bytes_sent
    return kbps_received, kbps_sent


def check_cpu_load(cpu_threshold):
    """
    Check the CPU load.
    Args:
        cpu_threshold (float): The CPU usage threshold in percent.
    Returns:
        The CPU usage percentage.
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    # if cpu_percent <= cpu_threshold:
    #     duration_below_threshold += 1
    # else:
    #     duration_below_threshold = 0
    return cpu_percent


if __name__ == '__main__':
    duration_below_threshold = 0
    while True:
        laptop_screen_status = is_screen_off()
        if laptop_screen_status:
            print(f"Laptop lid is closed.")
        else:
            print(f"Laptop lid is open.")
        print(f"Download Speed {check_network_speed()[0]:.2f}KB/s | Upload Speed {check_network_speed()[1]:.2f}KB/s")
        print(f"Current CPU Load is {check_cpu_load(20):.0f}%")

