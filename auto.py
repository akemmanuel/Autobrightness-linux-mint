#!/usr/bin/python3
from gi.repository import Gio
import os
import cv2
import numpy as np

proxy = Gio.DBusProxy.new_sync(
            Gio.bus_get_sync(Gio.BusType.SESSION, None),
            Gio.DBusProxyFlags.NONE,
            None,
            "org.cinnamon.SettingsDaemon.Power",
            "/org/cinnamon/SettingsDaemon/Power",
            "org.cinnamon.SettingsDaemon.Power.Screen",
            None)

camera = cv2.VideoCapture(0)

while True:
    _, image = camera.read()
    cv2.imwrite(os.path.expanduser("~/.face.png"), image)
    os.system("mv ~/.face.png ~/.face")
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    brightness = np.mean(hsv[:, :, 2])

    brightness_percent = (brightness / 255) * 100

    brightness_percent = 100 - round(brightness_percent, 2)

    proxy.SetPercentage("(u)", brightness_percent)

