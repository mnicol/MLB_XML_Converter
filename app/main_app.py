import re
import time
import traceback
from pathlib import Path
from tkinter.filedialog import askopenfile
import tkinter as tk
from tkinter import ttk, HORIZONTAL, messagebox
from typing import List

from config import Config
from parse_engine import ParseEngine
import xml.etree.ElementTree as ET
import logging


class MainApp(tk.Tk):
    def __init__(self, config: Config):
        super().__init__()
        try:
            # Catch Exceptions
            self.report_callback_exception = _handle_exception

            self.protocol("WM_DELETE_WINDOW", self._on_close)

            self.config = config

            self.key_file_path = "key_file.txt"

            logging.info("Starting Parser")
            poll_rate = 1
            if self.config.contains("PARSE SETTINGS", "pollrate"):
                poll_rate = int(self.config.get("PARSE SETTINGS", "pollrate"))
            self.parser: ParseEngine = ParseEngine(poll_rate, self, self._get_xml_keys())

            self.title("MLB Data Converter")

            self.input_xml_file_path = "None selected"
            self.input_file = None
            self.output_xml_file_path = "None Selected"
            self.output_file = None

            self.parser_running = False

            if self.config.contains("FILE PATHS", "inputXml"):
                self.input_xml_file_path = self.config.get('FILE PATHS', 'inputXml')
                logging.info(f'input_xml_file_path ({self.input_xml_file_path})')
            if self.config.contains("FILE PATHS", "outputXml"):
                self.output_xml_file_path = self.config.get('FILE PATHS', 'outputXml')
                logging.info(f'output_xml_file_path ({self.output_xml_file_path})')

            # Input XML Frame
            self.xml_input_frame = tk.Frame(self, width=150, height=150)

            self.input_xml_label = ttk.Label(self.xml_input_frame, text='Input Xml:', font=('calibre', 10, 'bold'))
            self.input_xml_value_label = ttk.Label(self.xml_input_frame, text=self.input_xml_file_path,
                                                   font=('calibre', 10))
            self.open_input_xml_btn = ttk.Button(self.xml_input_frame, text='Select Input Xml',
                                                 command=lambda: self._set_input_xml())

            self.open_input_xml_btn.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)
            self.input_xml_label.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)
            self.input_xml_value_label.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)

            self.xml_input_frame.grid(row=0, column=0, sticky="nsew")

            # Output XML Frame
            self.xml_output_frame = tk.Frame(self, width=150, height=150)

            self.output_xml_label = ttk.Label(self.xml_output_frame, text='Input Xml:', font=('calibre', 10, 'bold'))
            self.output_xml_value_label = ttk.Label(self.xml_output_frame, text=self.output_xml_file_path,
                                                    font=('calibre', 10))
            self.open_output_xml_btn = ttk.Button(self.xml_output_frame, text='Select Output Xml',
                                                  command=lambda: self._set_output_xml())

            self.open_output_xml_btn.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)
            self.output_xml_label.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)
            self.output_xml_value_label.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)

            self.xml_output_frame.grid(row=1, column=0, sticky="nsew")

            # Key Input Frame
            self.key_input_frame = tk.Frame(self)

            # Scroll Bar
            scroll = tk.Scrollbar(self.key_input_frame)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)

            # TextBox Creation
            self.input_txt = tk.Text(self.key_input_frame, height=20, width=85, yscrollcommand=scroll.set)
            self.input_txt_label = ttk.Label(self.key_input_frame, text="Tricaster Keys",
                                             font=('calibre', 10, 'bold', 'underline'))
            self.save_label = ttk.Label(self.key_input_frame, text="", font=('calibre', 10, 'bold'))
            self.save_btn = ttk.Button(self.key_input_frame, text='Save Keys', command=self._save)

            # Configure the scrollbars
            scroll.config(command=self.input_txt.yview)

            self.input_txt_label.pack(side=tk.TOP, anchor=tk.SW, padx=5, pady=10)
            self.save_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)
            self.save_btn.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)
            self.input_txt.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)

            self.key_input_frame.grid(row=2, column=0, sticky="nsew")

            # Run Options Frame
            self.run_options_frame = tk.Frame(self, width=150, height=150)

            # Start/Stop
            self.start_btn = ttk.Button(self.run_options_frame, text='Start', command=self._start)
            self.stop_btn = ttk.Button(self.run_options_frame, text='Stop', command=self._stop)

            # Progress
            self.progress_label = ttk.Label(self.run_options_frame, text="Time Until Data Conversion:",
                                            font=('calibre', 10, 'bold'))
            self.progress = ttk.Progressbar(self.run_options_frame, orient=HORIZONTAL, length=100, mode='determinate')

            self.status_label = ttk.Label(self.run_options_frame, text="Status:", font=('calibre', 10, 'bold'))
            self.status_state_label = ttk.Label(self.run_options_frame, text="Stopped", font=('calibre', 10))

            self.progress_label.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)
            self.progress.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)

            self.status_label.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)
            self.status_state_label.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=10)

            self.stop_btn.pack(side=tk.RIGHT, anchor=tk.N, padx=5, pady=10)
            self.start_btn.pack(side=tk.RIGHT, anchor=tk.N, padx=5, pady=10)

            self.run_options_frame.grid(row=3, column=0, sticky="nsew")

            self._initialize_key_text()
            self._handle_button_state()
        except Exception as e:
            logging.error(e.args)
            traceback.print_exc()

            # Display message on startup failure
            self.failed_to_start_label = ttk.Label(self, text='App Failed to start. Check Logs for more info.',
                                                   font=('calibre', 10, 'bold'))
            self.failed_to_start_label.pack()

    def update_progress(self, value):
        self.progress['value'] = value
        self.update_idletasks()

    def get_input_xml(self) -> ET.ElementTree:
        if self.input_xml_file_path:
            try:
                return ET.parse(self.input_xml_file_path)
            except FileNotFoundError as e:
                logging.error(e)
                tk.messagebox.showerror("ERROR", e)
        return None

    def set_output_xml(self, xml_root_node: ET.Element):
        if not xml_root_node:
            return
        b_xml = ET.tostring(xml_root_node)
        try:
            with open(self.output_xml_file_path, "wb") as f:
                f.write(b_xml)
        except FileNotFoundError as e:
            logging.error(e)
            tk.messagebox.showerror("ERROR", e)

    def _start(self):
        self.status_state_label.configure(text="Running")
        self.parser.start()
        self.parser_running = True
        self._handle_button_state()

    def _stop(self):
        self.status_state_label.configure(text="Stopped")
        self.parser.stop()
        self.parser_running = False
        self._handle_button_state()

    def _save(self):
        input_text: List[str] = self._get_text_input()
        updated_input_text = ""
        with open(self.key_file_path, "w") as key_file:
            line_number = 1
            for input_key in input_text:
                if not input_key:
                    continue
                input_key = input_key.replace('[INVALID KEY]', '')
                match = re.search("^%[a-zA-Z0-9_]+(?:\\s[a-zA-Z0-9_]+)*%$", input_key)
                if match:
                    key_file.write(f'{input_key}\n')
                    updated_input_text = f"{updated_input_text}{input_key}\n"
                else:
                    new_key = input_key.replace('\n', '')
                    updated_input_text = f"{updated_input_text}[INVALID KEY]{new_key}\n"
                    logging.warning(f"Invalid key format on line {line_number} for key ({input_key}). "
                                    f"Proper key format '%value value...%'")
                line_number = line_number + 1
        self.parser.update_keys(self._get_xml_keys())
        self._update_text_input(updated_input_text)
        self.save_label.configure(text=f'Saved: {time.strftime("%x - %X")}')

    def _set_input_xml(self):
        file = askopenfile(mode='r', filetypes=[('Xml File', '*.xml')])
        if file is not None:
            self.input_xml_file_path = file.name
            self.config.update("FILE PATHS", "inputXml", file.name)
            self.input_xml_value_label.configure(text=self.input_xml_file_path)
            self.input_file = file
            self._handle_button_state()

    def _set_output_xml(self):
        file = askopenfile(mode='r', filetypes=[('Xml File', '*.xml')])
        if file is not None:
            self.output_xml_file_path = file.name
            self.config.update("FILE PATHS", "outputXml", file.name)
            self.output_xml_value_label.configure(text=self.output_xml_file_path)
            self.output_file = file
            self._handle_button_state()

    def _get_xml_keys(self) -> List[List[str]]:
        xml_keys = []
        if Path(self.key_file_path).is_file():
            try:
                with open(self.key_file_path, "r") as key_file:
                    for tricaster_key in key_file:
                        tricaster_key_parts: List[str] = tricaster_key.replace('%', '').rstrip().split(' ')
                        xml_keys.append(tricaster_key_parts)
            except FileNotFoundError as e:
                logging.error(e)
                tk.messagebox.showerror("ERROR", e)
        else:
            with open(self.key_file_path, "w"):
                logging.debug(f"Created key file ({self.key_file_path})")
        return xml_keys

    def _initialize_key_text(self):
        if Path(self.key_file_path).is_file():
            key_file_string = ""
            try:
                with open(self.key_file_path, "r") as key_file:
                    for key in key_file:
                        key_file_string = f"{key_file_string}{key}"
                    self._update_text_input(f'{key_file_string}\n')
            except FileNotFoundError as e:
                logging.error(e)
                tk.messagebox.showerror("ERROR", e)

        else:
            with open(self.key_file_path, "w"):
                logging.debug(f"Created key file ({self.key_file_path})")

    def _handle_button_state(self):
        # Save Button
        if self.parser_running:
            self.save_btn.configure(state=tk.DISABLED)
        else:
            self.save_btn.configure(state=tk.NORMAL)

        # Start/Stop Buttons
        if ".xml" in self.input_xml_file_path and ".xml" in self.output_xml_file_path:
            if self.parser_running:
                self.stop_btn.configure(state=tk.NORMAL)
                self.start_btn.configure(state=tk.DISABLED)
            else:
                self.stop_btn.configure(state=tk.DISABLED)
                self.start_btn.configure(state=tk.NORMAL)
        else:
            self.stop_btn.configure(state=tk.DISABLED)
            self.start_btn.configure(state=tk.DISABLED)

    def _get_text_input(self) -> List[str]:
        input_text = self.input_txt.get("1.0", 'end-1c')
        return input_text.split("\n")

    def _update_text_input(self, value: str):
        if self.input_txt.get("1.0", 'end-1c'):
            self.input_txt.delete("1.0", tk.END)
        self.input_txt.insert("1.0", value)

    def _on_close(self):
        if self.parser_running:
            if messagebox.askokcancel("Quit", "Parser Running. Are you sure you want to quit?"):
                self.parser.stop()
                self.destroy()
        else:
            self.destroy()

    def start(self):
        self.mainloop()


def _handle_exception(*args):
    logging.error(traceback.format_exception(*args))
