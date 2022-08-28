import gi
import qinfo
import os
import sys
from defines import Defines
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

silent = False
config_file = os.path.join(os.environ.get("HOME"), ".config/.qinfo.conf")
config = qinfo.parse_config(config_file, silent)

if config is None:
    sys.exit(1)

if config["display_cpu"]:
    cpuline = f"CPU: {qinfo.cpu_model()}\n"
else:
    cpuline = ""

if config["display_mem"]:
    available_memory = qinfo.avalible_memory()
    total_memory = qinfo.total_memory()
    used_memory = total_memory - available_memory
    
    if config["display_gb"]:
        used_memory = (total_memory - available_memory) / Defines.KILOBYTE_GIGABYTE_CONVERSION
        total_memory = qinfo.total_memory() / Defines.KILOBYTE_GIGABYTE_CONVERSION
        unit = "GB"
        ramline = f"RAM: {used_memory:.2f}/{total_memory:.2f} {unit}\n"

    else:
        unit = "kB"
        ramline = f"RAM: {used_memory}/{total_memory} {unit}\n"
else:
    ramline = ""


class LabelWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="qinfo")

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_right.set_homogeneous(False)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        label = Gtk.Label(label=f"{cpuline}{ramline}")
        vbox_left.pack_start(label, True, True, 0)

        label = Gtk.Label(
            label="logoplaceholder"
        )
        label.set_line_wrap(True)
        label.set_justify(Gtk.Justification.LEFT)
        label.set_max_width_chars(32)
        vbox_right.pack_start(label, True, True, 0)

        self.add(hbox)


window = LabelWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
