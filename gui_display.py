from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.ttk import *

from parse_engine import ParseEngine
import xml.etree.ElementTree as ET


class GuiDisplay:
    def __init__(self):
        self.parser: ParseEngine = ParseEngine(5, self)
        self.root = Tk()
        self.root.geometry("600x400")
        self.root.title("MLB Data Converter")

        self.input_xml_file_path = ""
        self.input_file = None
        self.output_xml_file_path = ""
        self.output_file = None

        # Input XML
        self.input_xml_label = Label(self.root, text='Input Xml:', font=('calibre', 10, 'bold'))
        self.input_xml_value_label = Label(self.root, font=('calibre', 10))
        self.open_input_xml_btn = Button(self.root, text='Select Input Xml', command=lambda: self._set_input_xml())

        # Output XML
        self.output_xml_label = Label(self.root, text='Input Xml:', font=('calibre', 10, 'bold'))
        self.output_xml_value_label = Label(self.root, font=('calibre', 10))
        self.open_output_xml_btn = Button(self.root, text='Select Output Xml', command=lambda: self._set_output_xml())

        # Start/Stop
        self.start_btn = Button(self.root, text='Start', command=self._start)
        self.stop_btn = Button(self.root, text='Stop', command=self._stop)

        # Progress
        self.progress = Progressbar(self.root, orient=HORIZONTAL, length=100, mode='determinate')

        # Grid
        # Input XML
        self.open_input_xml_btn.grid(row=0, column=0)
        self.input_xml_label.grid(row=0, column=1)
        self.input_xml_value_label.grid(row=0, column=2)

        # Output XML
        self.open_output_xml_btn.grid(row=1, column=0)
        self.output_xml_label.grid(row=1, column=1)
        self.output_xml_value_label.grid(row=1, column=2)

        # Start/Stop
        self.start_btn.grid(row=3, column=0)
        self.stop_btn.grid(row=3, column=1)

        # Progress
        self.progress.grid(row=4, column=0)

    def update_progress(self, value):
        self.progress['value'] = value
        self.root.update_idletasks()

    def get_input_xml(self) -> ET.ElementTree:
        return ET.parse(self.input_xml_file_path)

    def set_output_xml(self, xml: ET.ElementTree):
        b_xml = ET.tostring(xml.getroot())
        with open(self.output_xml_file_path, "wb") as f:
            f.write(b_xml)

    def _start(self):
        self.parser.start()

    def _stop(self):
        self.parser.stop()

    def _set_input_xml(self):
        file = askopenfile(mode='r', filetypes=[('Xml File', '*.xml')])
        if file is not None:
            self.input_xml_file_path = file.name
            self.input_xml_value_label.configure(text=self.input_xml_file_path)
            self.input_file = file

    def _set_output_xml(self):
        file = askopenfile(mode='r', filetypes=[('Xml File', '*.xml')])
        if file is not None:
            self.output_xml_file_path = file.name
            self.output_xml_value_label.configure(text=self.output_xml_file_path)
            self.output_file = file

    def start(self):
        self.root.mainloop()
