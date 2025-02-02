import csv
import tkinter as tk

from pathlib import Path
from tkinter import filedialog
from collections import defaultdict

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
    
    def _collect_statistics(self, result_files):
        correct_counts = defaultdict(int)
        total_students = len(result_files)
        wrong_counts = defaultdict(int)

        for result_file in result_files:
            with open(result_file, 'r', newline='', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)

                for row in csv_reader:
                    question = int(row['Question'])
                    print(f"question number: {question}")
                    is_correct = row['Correct'].lower() == 'true'

                    if is_correct:
                        correct_counts[question] += 1
                    else:
                        wrong_counts[question] += 1

        most_wrong = max(wrong_counts.items(), key=lambda x: x[1])[0]

        return total_students, correct_counts, most_wrong
            
    def create_statistics(self, test_number, output_dir):
        pattern = f"*-{test_number}.csv"
        result_files = list(self.results_dir.glob(pattern))

        if not result_files:
            raise FileNotFoundError(f"No result files found for test {test_number}")
        
        total_students, correct_counts, most_wrong = self._collect_statistics(result_files)

        path_output = Path(output_dir) / f"{test_number}-통계.txt"

        with open(path_output, 'w', encoding='utf-8-sig') as f:
            f.write(f"{test_number} 통계\n\n")
            f.write(f"제출한 학생 수: {total_students}명\n")
            f.write(f"가장 많이 틀린 문항: {most_wrong}번\n\n")

            f.write("문항별 정답률:\n")
            for question in range(18, 46):
                correct = correct_counts[question]
                percentage = (correct / total_students) * 100
                #print(f"question number: {question}\n")
                #print(f"correct_counts: {correct_counts[question]}\n")
                f.write(f"{question} : {correct}/{total_students} ({percentage:.0f}%)\n")
        
        return path_output


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

        compiled_results.sort(key=lambda x: x['이름'])

        output_file = output_path / f"{test_number}-개별오답.csv"
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['이름', '개별오답'])
            writer.writeheader()
            writer.writerows(compiled_results)

        self.create_statistics(test_number, output_path)

        return output_file