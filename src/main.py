import gi
# import logging
import qinfo
import os
from math import trunc
import sys
import time
import threading 
from defines import Defines
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Window(Gtk.Window):
    
    def get_values(self) -> str:
        silent = False
        config_file = os.path.join(os.environ.get("HOME"), ".config/.qinfo.conf")
        config = qinfo.parse_config(config_file, silent)

        if config is None:
            sys.exit(1)
    
        if config["display_hostname"]:
            hostnamestring = f"Hostname:\t\t{qinfo.hostname()}"
        if config["display_cpu"]:
            cpuline = f"CPU:\t\t\t\t{qinfo.cpu_model()} ({qinfo.core_count()} cores, {qinfo.thread_count()} threads)\n"
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
                ramline = f"Memory:\t\t\t{used_memory:.2f}/{total_memory:.2f} {unit}\n"

            else:
                unit = "kB"
                ramline = f"Memory:\t\t\t{used_memory}/{total_memory} {unit}\n"
        else:
            ramline = ""

        if config["display_board"]:
            boardline = f"Motherboard:\t\t{qinfo.motherboard_model()}\n"
        else:
            boardline = ""
        
        if config["display_os"]:
            osline = f"Operating System:\t{qinfo.os_name()}\n"
        else:
            osline = ""

        if config["display_kernel"]:
            kernelline = f"Kernel Release:\t\t{qinfo.kernel_release()}\n"
        else:
            kernelline = ""

        if config["display_rootfs_birth"]:
            rootfsbirthdate = qinfo.rootfs_age()
            birthyear = rootfsbirthdate["year"]
            birthmonth = rootfsbirthdate["month"]
            birthday = rootfsbirthdate["day"]
            if not config["date_order"]:
                birthstring = f"Root (/) Birth:\t\t{birthmonth}/{birthday}/{birthyear}\n"
            else:
                birthstring = f"Root (/) Birth:\t\t{birthyear}/{birthmonth}/{birthday}\n"
        else: 
            birthstring = ""

        if config["display_uptime"]:
            uptime = qinfo.uptime()
            uptime_days = trunc(uptime / Defines.SECOND_DAY_CONVERSION)
            uptime_hours = trunc(uptime / Defines.SECOND_HOUR_CONVERSION % Defines.HOUR_DAY_CONVERSION)
            uptime_minutes = trunc(uptime / Defines.SECOND_MINUTE_CONVERSION % Defines.MINUTE_HOUR_CONVERSION)
            uptime_seconds = trunc(uptime % Defines.SECOND_MINUTE_CONVERSION)
            uptimestring = "System Uptime:\t"
            
            if uptime_days > 0:
                uptimestring += f"{uptime_days:.0f} days "
            if uptime_hours > 0:
                uptimestring += f"{uptime_hours:.0f} hours "
            if uptime_minutes > 0:
                uptimestring += f"{uptime_minutes:.0f} minutes "
            if uptime_seconds > 0:
                uptimestring += f"{uptime_seconds:.0f} seconds"
            uptimestring += "\n"
        else:
            uptimestring = ""

        return f"{cpuline}{ramline}{boardline}{osline}{kernelline}{uptimestring}{birthstring}"
            
    
    def __init__(self):

        super().__init__(title="qinfo-gui")

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_right.set_homogeneous(False)
        
        
    
        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        self.label = Gtk.Label(label=self.get_values())
        self.label.set_margin_top(50)

        # Update info every 3 seconds
        x = threading.Thread(target=self.loop_sleep)
        x.daemon = True
        x.start()

        vbox_left.pack_start(self.label, False, True, 0)

        # label1 = Gtk.Label(
        #     label="logoplaceholder"
        # )
        # label1.set_line_wrap(True)
        # label1.set_justify(Gtk.Justification.LEFT)
        # label1.set_max_width_chars(32)
        # vbox_right.pack_start(label1, True, True, 0)


        self.add(hbox)
    
    def stop(self):
      Gtk.main_quit()

    def loop_sleep(self):
        
        while True:
            self.label.set_text(self.get_values())
            while Gtk.events_pending():
                    Gtk.main_iteration()
            time.sleep(3)


        

def main() -> int:
    window = Window()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())