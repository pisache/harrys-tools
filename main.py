import tkinter as tk

from tkinter import ttk
from tkinter import font as tkfont

from lib.scanPDF import ScanPDF
from lib.excelAutomation import ExcelAutomation
from lib.toPDF import ToPDF

class HarrysToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Harrys Tools")
        self.root.geometry("400x400")

        # Style Configuration
        self.style = ttk.Style()
        self.style.configure('Welcome.TLabel', font=('Helvetica', 24, 'bold'))
        self.style.configure('Nav.TButton', font=('Helvetica', 12))

        # Main Container
        self.frame_main = ttk.Frame(self.root, padding="20")
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        # Welcome Message
        TEXT_WELCOME = "해리스 교육 행정 툴"
        label_welcome = ttk.Label(
            self.frame_main,
            text=TEXT_WELCOME,
            style='Welcome.TLabel'
        )
        label_welcome.pack(pady=40)

        # Button Container
        frame_button = ttk.Frame(self.frame_main)
        frame_button.pack(fill=tk.BOTH, expand=True)

        # Navigation Buttons
        buttons = [
            ("Tool 1", self.open_tool1),
            ("Tool 2", self.open_tool2),
            ("Tool 3", self.open_tool3),
            ("Tool 4", self.open_tool4)
        ]

        for text, command in buttons:
            btn = ttk.Button(
                frame_button,
                text=text,
                command=command,
                style="Nav.TButton",
                width=10
            )
            btn.pack(pady=10)

    def open_tool1(self):
        pass

    def open_tool2(self):
        pass

    def open_tool3(self):
        pass

    def open_tool4(self):
        pass

if __name__=="__main__":
    root=tk.Tk()
    app = HarrysToolsGUI(root)
    root.mainloop()