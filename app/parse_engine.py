import time
import threading
import xml.etree.ElementTree as ET
from typing import List
import logging


class ParseEngine:
    def __init__(self, parse_interval: int, main_app, xml_keys: List[List[str]]):
        self.parse_interval = parse_interval
        self.is_running = False
        self.main_app = main_app
        self.thread = None
        self.xml_keys = xml_keys

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        else:
            self.thread: ParseThread = ParseThread(self.main_app, self.parse_interval, self.xml_keys)
            self.thread.start()

    def stop(self):
        if self.thread and self.thread.is_alive():
            self.thread.stop()
            self.thread.join()

    def update_keys(self, xml_keys: List[List[str]]):
        self.stop()
        self.xml_keys = xml_keys


class ParseThread (threading.Thread):
    def __init__(self, gui_display, parse_interval: int, xml_keys: List[List[str]]):
        threading.Thread.__init__(self)
        self.parse_interval = parse_interval
        self.main_app = gui_display
        self._stop_event = threading.Event()
        self.xml_keys = xml_keys

    def run(self):
        logging.debug("Starting Parse Thread")
        if self.parse_interval < 1:
            return
        progress_interval = 100 / (self.parse_interval*2)  # Adjust for half second tic
        logging.debug(f"Parse Interval ({progress_interval})")
        progress = 0
        while not self.stopped():
            self.main_app.update_progress(progress)
            progress = progress + progress_interval
            logging.debug(f"Progress ({progress})")
            if progress > 100:
                self.main_app.update_progress(progress)
                progress = progress_interval
                self._process()
            time.sleep(0.5)
        logging.debug("Ending Parse Thread")

    def stop(self):
        logging.debug("Stop event fired")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def _process(self):
        logging.debug("Processing XML")
        xml_tree: ET.ElementTree = self.main_app.get_input_xml()
        if not xml_tree:
            logging.warning("Could not get xml. Skipping processing.")
            self.stop()
            return
        logging.debug(f"XML: {xml_tree}")
        root = None
        for key_list in self.xml_keys:
            xpath_key = f'.//{"/".join(key_list)}'
            logging.debug(f"Handle XPATH ({xpath_key})")
            xml_element = xml_tree.find(xpath_key)
            if not root or key_list[0] not in root.tag:
                root = _add_key_to_xml_tree(key_list[0])
                logging.debug(f"Created Root ({root.tag})")
            temp_element = root
            for key in key_list[1:]:
                logging.debug(f"Adding Key ({key}) to element ({temp_element.tag})")
                temp_element = _add_key_to_xml_tree(key, temp_element)
            temp_element.text = xml_element.text
        logging.debug("Done Processing XML")
        self.main_app.set_output_xml(root)


def _add_key_to_xml_tree(key: str, parent_element: ET.Element = None) -> ET.Element:
    if parent_element is None:
        return ET.Element(key)
    else:
        sub_element = ET.SubElement(parent_element, key)
        return sub_element
