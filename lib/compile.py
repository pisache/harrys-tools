import csv
import tkinter as tk

from pathlib import Path
from tkinter import filedialog

class Compile:
    def __init__(self, results_dir="./out"):
        self.results_dir = Path(results_dir)

    def _get_output_directory(self):
        root = tk.Tk()
        root.withdraw()

        dir_path = filedialog.askdirectory(
            title="결과를 저장할 위치 선택",
            initialdir="."
        )

        root.destroy()
        return dir_path if dir_path else None
    
    def compile_wrong_answers(self, test_number):
        output_dir = self._get_output_directory()

        if not output_dir:
            raise ValueError("올바른 경로가 아닙니다.")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        pattern = f"*-{test_number}.csv"
        result_files = list(self.results_dir.glob(pattern))

        if not result_files:
            raise FileNotFoundError(f"No result files found for test {test_number}")

        compiled_results = []

        for result_file in result_files:
            student_name = result_file.stem.split('-')[0]

            wrong_questions = []
            with open(result_file, 'r', newline='', encoding='utf-8-sig') as f:
                csv_reader = csv.DictReader(f)

                for row in csv_reader:
                    if row['Correct'].lower() == 'false':
                        wrong_questions.append(int(row['Question']))

            wrong_questions.sort()
            wrong_questions_str = ', '.join(map(str, wrong_questions))

            compiled_results.append({
                '이름': student_name,
                '개별오답': wrong_questions_str
            })

        output_file = output_path / f"{test_number}-개별오답.csv"
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['이름', '개별오답'])
            writer.writeheader()
            writer.writerows(compiled_results)

        return output_file