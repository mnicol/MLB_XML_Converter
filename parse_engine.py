import time
import threading
import xml.etree.ElementTree as ET


class ParseEngine:
    def __init__(self, parse_interval: int, gui_display):
        self.parse_interval = parse_interval
        self.is_running = False
        self.gui_display = gui_display
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        else:
            self.thread: ParseThread = ParseThread(self.gui_display, self.parse_interval)
            self.thread.start()

    def stop(self):
        self.thread.stop()
        self.thread.join()

    def update_interval(self, parse_interval: int):
        return


class ParseThread (threading.Thread):
    def __init__(self, gui_display, parse_interval: int):
        threading.Thread.__init__(self)
        self.parse_interval = parse_interval
        self.gui_display = gui_display
        self._stop_event = threading.Event()

    def run(self):
        if self.parse_interval < 1:
            return
        progress_interval = 100 / (self.parse_interval*2)  # Adjust for half second tic
        progress = 0
        while not self.stopped():
            print(f"Progress: {progress}")
            self.gui_display.update_progress(progress)
            progress = progress + progress_interval
            if progress > 100:
                self.gui_display.update_progress(progress)
                progress = progress_interval
                self._process()
            time.sleep(0.5)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def _process(self):
        print(f"Process")
        xml_tree: ET.ElementTree = self.gui_display.get_input_xml()
        current_batter_full_name = xml_tree.find("./clsGame/CurrentBatter/fullName")
        output_xml_tree = ET.Element('CurrentBatter')
        ET.SubElement(output_xml_tree, 'fullName')
        return

