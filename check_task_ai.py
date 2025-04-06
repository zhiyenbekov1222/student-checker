'''
AI automation of student tasks 
'''

import openai
import os
import json
import pandas as pd
import csv

openai.api_key = "your api_key"

class check_by_chat:
    '''
    Класс для автоматизированной проверки кода студентов на соответствие заданию.
    Сравнивает код и описание задачи с помощью OpenAI и сохраняет результат в CSV файл.
    '''
    def __init__(self):
        # можно расширить при необходимости
        pass

    def read_python_file(self, file_path):
        '''
        Считывает Python-файл и возвращает его содержимое как строку.
        :param file_path: путь до файла
        :return: строка с содержимым файла
        '''
        with open(file_path, 'r') as file:
            code = file.read()
        return code

    def create_csv(self):
        '''
        Создает новый CSV файл (или очищает старый), куда будут записаны результаты проверки.
        '''
        f = open('student_records.csv', 'w')
        print('New csv for records has been created.')
 
    def csv_records(self, row_list):
        '''
        Добавляет одну строку записи о студенте в CSV файл.
        Если файл еще не создан или пуст, добавляет заголовки столбцов.
        :param row_list: список значений для одной строки записи
        '''
        file_exists = os.path.isfile('student_records.csv')
        write_header = not file_exists or os.stat('student_records.csv').st_size == 0
    
        with open('student_records.csv', 'a', newline='') as file:
            csv_writer = csv.writer(file)
            
            if write_header:
                header = ['Student Name', 'Task Name', 'Workable', 'Relevance %', 'Assessment %', 'Unnecessary code %', 'Comments']
                csv_writer.writerow(header)
            
            csv_writer.writerow(row_list)
            print('1 record successfully inserted.')

        
    def check_task(self, student_name, code, name_task, task_description):
        """ Проверяет соответствие кода студента описанию задания с помощью OpenAI.

            Алгоритм работы:
            1. Формирует prompt, в котором указано, как следует проанализировать код:
                - Совпадает ли логика кода с требованиями задания?
                - Работает ли код без ошибок?
                - Используются ли все переменные и подключены ли библиотеки?
                - Есть ли избыточные участки кода?
        
            2. Пример результата: 
                student_name, name_task, Yes/No, % релевантности, % общего качества, % избыточного кода, комментарий
            
            Пояснения к полям:
            0. Имя студента
            1. Название задания
            2. Работоспособность: Yes/No (есть ли ошибки, всё ли используется, подключены ли библиотеки)
            3. Релевантность к заданию (0-100%)
            4. Общая оценка кода (логика, структура, оптимизация, читаемость)
            5. % избыточного кода (рассчитывается как: ненужные строки / общее количество строк * 100)
            6. Краткий комментарий с предложениями по улучшению (не более 50 слов)
        
            Возвращает:
                Строку с результатом, готовую для записи в CSV.
        """
        
        prompt = f"""
        There is a task to be completed. You should check the student code for the task description how much does it coinside with expected output. 
        You should pay attention also the code workabilty, does the code works correctly or will raise an error. 
        If the task description is differ from the code logic what it does then it should put 0% and comment it.
        If the code corresponds for all criteria in task description and inlcude necessary function then it should put 100% and comment it
        At the end you should provide the result consisting 6 answers with comma seperated values. nothing else!
        0.Student_name
        1.Task name
        2.Yes/No if the code workable and all varibales are used, necessary libraries imported.Provide no more 20 words.
        3.The percentage 0 - 100,   if the code relevant to the task. 
        4.Overall assessment of code. In percentage 0 - 100. How much code optimized, logically correct, maybe unnecessary variables and
        5.Some operands used to extend. Only in percentage 0 -100% (formula: unnecessary number of code / all number of code * 100). If all good then 0% and do not miss it.
        6.Comment for improvements. Words no more that 50.
        
        task description: 
        {task_description}
        Name task: {name_task}
        The student {student_name}'s code:
        Code:
        {code}
        Example of output:
        student_name, name_task, Yes, 70, 0, 20 "The code completed well. Some drawback, specification and generally good"
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.5
        )
        
        return response.choices[0].message["content"].strip()

    def compare_code_similarity(code, name_task):
        '''Сравнивает данный код с ранее загруженными кодами по структуре, логике и именам переменных с помощью OpenAI.

            Алгоритм работы:
            1. Формирует специальный prompt, в котором GPT должно:
                - Определить, насколько данный код похож на предыдущие (например, по структуре, названиям переменных, логике).
                - Если код анализируется впервые, то результат должен быть 0, как "новый".
                - Если найдены похожие ранее отправленные коды, нужно вернуть имя наиболее похожего и оценку сходства (0–100%).
        
            2. Формат возвращаемого результата:
                - `name_code(current), SIMILARITY Score (0-100), name code (наиболее похожий из предыдущих)`
                - Никаких дополнительных пояснений, только одна строка.
        
            Аргументы:
            - `code` (str): текст Python-кода, который нужно проанализировать.
            - `name_code` (str): имя текущего кода (например, имя файла или задание студента).
        
            Возвращает:
            - Строку с оценкой сходства, формат: `name_code, similarity_score, similar_to_name_code`
        '''
        
        prompt = f"""
        Below is a code snippets. Please compare it and tell me how similar they are in terms of structure, variable names, and logic to
        the previous codes. If the first then similarity score 0, because it is new. Apply the fule for all following codes.
    
        name task: {name_task}
        Code:
        {code}
        
        Provide a similarity score (0 to 100) and a brief explanation similarity to which name code ?
        Result should be:
        name_code(existing), SIMILARITY Score(0 - 100), name code(name of previous code, if it this code similar)
        No more text. Only one line result with comma seperated. 
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.5
        )
        
        return response.choices[0].message["content"].strip()

    
    def main_run(self):
        
        dir_path = os.getcwd()
        folders = [path for path in os.listdir(dir_path) if (os.path.isdir(dir_path+'/'+path)) and not path.startswith('.')]
        dir_tasks = {}
        for task in folders:
            files = [file for file in os.listdir(dir_path + '/' + task) if not file.startswith('.')]
            #print(f'The file 2b read: {files}')
            dir_inner = {}
            for file in files:
                file_path = dir_path + '/' + task + '/' + file
                python_code = self.read_python_file(file_path)
                
                #print(f'The file_path 2b read: {file_path}')
                
                if file.endswith('.ipynb'):
                    parsed_data = json.loads(python_code)
                    n = 1
                    if len(parsed_data['cells']) == 1:
                        n = 0
                    python_code = " ".join(parsed_data['cells'][n]['source'])
                
                file_name = file.split('.')[0]
                file_desc = [description for description in os.listdir() if description.endswith('.txt') & (description[:len(task)] == task)][0]
                code_desc = self.read_python_file(file_desc)
                print(file_name)
                
                task_result = self.check_task(file_name, python_code, task, code_desc)
                print(task_result)
                row_list = [item.strip() for item in task_result.split(',')]
                if not os.path.exists('student_records.csv'):
                    self.create_csv()
                self.csv_records(row_list)
                dir_inner[file_name] = task_result
            dir_tasks[task] = dir_inner

if __name__ == "__main__":
    chat = check_by_chat()
    chat.main_run()
