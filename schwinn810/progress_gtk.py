""" Simple GTK progress indicator """

import os.path
from gi.repository import Gtk

class GtkProgress:

    def __init__(self):
        dir = os.path.dirname(__file__)
        builder = Gtk.Builder()
        builder.add_from_file("{:s}/progress.glade".format(dir))
        self.window = builder.get_object("progressWindow")
        self.trackCountLabel = builder.get_object("trackCountLabel")
        self.trackBar = builder.get_object("trackBar")
        self.pointCountLabel = builder.get_object("pointCountLabel")
        self.pointBar = builder.get_object("pointBar")
        self.window.show_all()
        self._update()

    def _update(self):
        while Gtk.events_pending(): Gtk.main_iteration()

    def track(self, name, at, end, points):
        self.trackBar.set_fraction(float(at-1)/end)
        self.trackCountLabel.set_text("{:d}/{:d}".format(at, end))
        self._update()

    def point(self, at, end):
        if at % 100 == 0:
            self.pointBar.set_fraction(float(at)/end)
            self.pointCountLabel.set_text("{:d}/{:d}".format(at, end))
            self._update()
