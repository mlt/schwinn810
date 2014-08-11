#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import dbus
from time import sleep
from subprocess import Popen

class DeviceAddedListener:
    def __init__(self, tray):
        self.tray = tray
        self.bus = dbus.SystemBus()
        self.hal_manager_obj = self.bus.get_object(
            "org.freedesktop.Hal", 
            "/org/freedesktop/Hal/Manager")
        self.hal_manager = dbus.Interface(self.hal_manager_obj,
            "org.freedesktop.Hal.Manager")
        self.hal_manager.connect_to_signal("DeviceAdded", self._added)
        self.hal_manager.connect_to_signal("DeviceRemoved", self._removed)

        for udi in self.hal_manager.FindDeviceByCapability("serial"):
            if "usb" not in udi:
                next
            device_obj = self.bus.get_object('org.freedesktop.Hal', udi)
            usb = dbus.Interface(device_obj, 'org.freedesktop.Hal.Device')
            if self.check_parent(usb):
                self.udi = udi
                self.fire()
                break

    def check_parent(self, device):
        parent = device.GetProperty('info.parent')
        parent_obj = self.bus.get_object ( 'org.freedesktop.Hal', parent)
        usb = dbus.Interface(parent_obj, 'org.freedesktop.Hal.Device')
        if usb.GetProperty("linux.subsystem") == "usb" and \
           usb.GetProperty("usb.vendor_id") == 0x10c4 and \
           usb.GetProperty("usb.product_id") == 0xea61:
            return True

    def _added(self, udi):
        device_obj = self.bus.get_object ("org.freedesktop.Hal", udi)
        device = dbus.Interface(device_obj, "org.freedesktop.Hal.Device")

        if device.QueryCapability("serial") and self.check_parent(device):
            self.udi = udi
            sleep(2)
            return self.fire()

    def _removed(self, udi):
        if self.udi and self.udi == udi:
            self.tray.statusIcon.set_from_stock(gtk.STOCK_DISCONNECT)

    def fire(self):
        self.tray.statusIcon.set_from_stock(gtk.STOCK_CONNECT)
        Popen("schwinn810")

class Schwinn810Tray:

    def __init__(self):
        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_stock(gtk.STOCK_DISCONNECT)
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("Schwinn810 monitor")

        self.menu = gtk.Menu()
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        self.menu.show_all()

        self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_visible(1)

        from dbus.mainloop.glib import DBusGMainLoop
        DBusGMainLoop(set_as_default=True)
        DeviceAddedListener(self)
        gtk.main()

    def quit_cb(self, widget, data = None):
        gtk.main_quit()


    def popup_menu_cb(self, widget, button, time, data = None):
        data.popup(None, None, gtk.status_icon_position_menu,
                   button, time, self.statusIcon)

if __name__ == "__main__":
    Schwinn810Tray()
