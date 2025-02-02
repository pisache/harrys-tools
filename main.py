import tkinter as tk
import tkinter.ttk as ttk

from tkinter import font as tkfont
from tkinter import filedialog, messagebox
from pathlib import Path

from lib.scanPDF import ScanPDF
from lib.excelAutomation import ExcelAutomation
from lib.toPDF import ToPDF
from lib.scoring import Scoring
from lib.compile import Compile

class HarrysToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Harrys Tools")
        self.root.geometry("400x300")
        self.scorer=Scoring(output_dir="./out")
        self.compiler=Compile(results_dir="./out")

        self.test_numbers = self._get_test_numbers()

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
            ("모의고사 채점", self.open_tool1)
            #("X", self.open_tool2)
        ]

        for text, command in buttons:
            btn = ttk.Button(
                frame_button,
                text=text,
                command=command,
                style="Nav.TButton",
                width=15
            )
            btn.pack(pady=10)

    def _get_test_numbers(self):
        path_resources = Path("./resources/answers")
        test_numbers = []
        if path_resources.exists():
            test_numbers = [f.stem for f in path_resources.glob("*.txt")]
        
        return sorted(test_numbers)

    def open_tool1(self):
        window_tool = tk.Toplevel(self.root)
        window_tool.title("개별오답 채점 자동화")
        window_tool.geometry("400x350")
        
        frame_main = ttk.Frame(window_tool, padding="20")
        frame_main.pack(fill=tk.BOTH, expand=True)

        # Title
        label_title = ttk.Label(
            frame_main,
            text="모의고사 자동 채점 툴",
            style='Title.Label'
        )
        label_title.pack(pady=20)

        # Control Frame
        frame_controls = ttk.Frame(frame_main)
        frame_controls.pack(fill=tk.X, pady=20)

        # Test number Selection
        label_test = ttk.Label(frame_controls, text="시험지를 선택해 주세요:")
        label_test.pack(side=tk.LEFT)

        test_var = tk.StringVar()
        if self.test_numbers:
            test_var.set(self.test_numbers[0])

        test_dropdown = ttk.Combobox(
            frame_controls,
            textvariable=test_var,
            values=self.test_numbers,
            state='readonly',
            width=15
        )
        test_dropdown.pack(side=tk.LEFT)

        def select_and_score():
            files = filedialog.askopenfilenames(
                title="답안지 선택",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )

            if files:
                try:
                    selected_test = test_var.get()
                    total_process = 0

                    for path_file in files:
                        wrong_questions = self.scorer.score(selected_test, path_file, output_dir="./out")
                        total_process += 1
                    
                    if total_process > 0:
                        compilation = self.compiler.compile_wrong_answers(selected_test)
                        messagebox.showinfo(
                            "해리스 툴즈",
                            f"{total_process}개의 답안지 채점 및 개별오답 정리 완료!"
                        )
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_score = ttk.Button(
            frame_controls,
            text="답안지 채점",
            command=select_and_score
        )
        button_score.pack(side=tk.LEFT)

        # Instruction
        instructions = (
            "사용 방법\n\n"
            "프로그램 폴더/resources/answers/ 안에 답안지 저장되있는지 확인\n\n"
            "1. 시험지 선택 드랍다운 메뉴에서 시험지 선택\n"
            "2. 답안지 채점 버튼 클릭후 답안지 전체 선택\n"
            "3. 개별오답 정리 파일을 저장할 위치 선택\n\n"
            "결과는 개별오답과 통계 두개의 파일로 저장됨"
        )

        label_instructions = ttk.Label(
            frame_main,
            text=instructions,
            wraplength=500,
            justify=tk.LEFT
        )
        label_instructions.pack(pady=20, fill=tk.X)
        

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