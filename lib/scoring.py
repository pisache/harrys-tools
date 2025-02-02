import os 
import csv

from pathlib import Path

class Scoring:
    def __init__(self, output_dir="./"):
        self.path_resource = Path("./resources/answers")
        self.output_dir = Path(output_dir)

    def _read_answer_key(self, test_number):
        path_answer_key = self.path_resource/f"{test_number}.txt"

        if not path_answer_key.exists():
            raise FileNotFoundError(f"Anser key not found for {test_number}")
        
        with open(path_answer_key, 'r') as f:
            return [int(x) for x in f.read().strip().split()]
        
    def _parse_student_answers(self, file_content, target_test):
        lines = file_content.strip().split('\n')
        current_test = None
        current_answers = []
        final_answers = []

    
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # is the current a test number
            if not any(c.isspace() for c in line):
                if current_test == target_test and current_answers:
                    final_answers = current_answers
                    break

                current_test = line
                current_answers = []
                continue

            # is the test number target test?
            if current_test == target_test:
                current_answers.extend([int(x) for x in line.split()])
        
        if current_test == target_test and current_answers and not final_answers:
            final_answers = current_answers

        if not final_answers:
            raise ValueError(f"Test {target_test} not found in answer file")
        
        return final_answers
    
    def score(self, test, file_answer, output_dir=None):
        path_output = Path(output_dir) if output_dir else self.output_dir
        answer_key = self._read_answer_key(test)

        with open(file_answer, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        student_answer = self._parse_student_answers(content, test)

        # is the number of answers correct
        if len(student_answer) != len(answer_key):
            raise ValueError(f"Number of ansers ({len(student_answer)}) does not match")
        
        results = []
        wrong_answers = []

        for q_num, (student_ans, correct_ans) in enumerate(zip(student_answer, answer_key), start=18):
            is_correct = student_ans == correct_ans
            results.append({
                'Question': q_num,
                'Student Answer':student_ans,
                'Correct': is_correct
            })
            
            if not is_correct:
                wrong_answers.append(q_num)

        output_filename = path_output / f"{Path(file_answer).stem}-{test}.csv"

        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Question', 'Student Answer', 'Correct'])
            writer.writeheader()
            writer.writerows(results)

        return wrong_answers



