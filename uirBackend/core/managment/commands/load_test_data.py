from django.core.management.base import BaseCommand
from uirBackend.core.models import Test, Characteristic, Question, Answer, AnswerWeight, CombinedTest, CombinedTestQuestion
import json

class Command(BaseCommand):
    help = 'Загружает данные тестов из JSON файлов в базу данных'

    def handle(self, *args, **kwargs):
        # Путь к JSON файлу с тестами
        file_paths = [
            'input_data.json',      # Тесты с вопросами
            'combined_test.json',   # Комбинированный тест
        ]

        # Процесс загрузки данных
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)

                if file_path == 'input_data.json':
                    self.load_tests(json_data)
                elif file_path == 'combined_test.json':
                    self.load_combined_test(json_data)

                self.stdout.write(self.style.SUCCESS(f'Успешно загружены данные из файла {file_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных из файла {file_path}: {e}'))

    def load_tests(self, json_data):
        # Обработка тестов
        for test_data in json_data:
            test_name = test_data.get("test_name")
            characteristics = test_data.get("characteristics")
            
            # Создание теста
            test = Test.objects.create(test_name=test_name, characteristics=characteristics, question_count=len(test_data['questions']))
            
            for question_data in test_data['questions']:
                question_text = question_data.get("question_text")
                
                # Создание вопроса
                question = Question.objects.create(test=test, question_text=question_text)
                
                for answer_data in question_data.get('answers', []):
                    answer_text = answer_data.get("answer_text")
                    weight = answer_data.get("weight")
                    trait_name = answer_data.get("trait")
                    
                    # Создание или получение характеристики
                    characteristic, created = Characteristic.objects.get_or_create(name=trait_name)
                    
                    # Создание ответа и веса
                    answer = Answer.objects.create(question=question, answer_text=answer_text)
                    AnswerWeight.objects.create(question=question, trait=characteristic, weight=weight)

    def load_combined_test(self, json_data):
        # Обработка комбинированного теста
        combined_test_name = json_data.get("combined_test_name")
        characteristics = json_data.get("characteristics")

        combined_test = CombinedTest.objects.create(combined_test_name=combined_test_name, characteristics=characteristics)

        # Проходим по каждому тесту из комбинированного теста
        for test_data in json_data.get("tests", []):
            test_name = test_data.get("test_name")
            questions_count = test_data.get("questions_count")
            
            # Получаем тест по имени
            try:
                test = Test.objects.get(test_name=test_name)
            except Test.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Тест с именем {test_name} не найден'))
                continue
            
            # Выбираем первые несколько вопросов (например, 3-4) из данного теста
            questions = test.question_set.all()[:questions_count]
            
            # Добавляем вопросы в комбинированный тест
            for question in questions:
                # Создаём запись о вопросе в комбинированном тесте
                CombinedTestQuestion.objects.create(combined_test=combined_test, original_test=test, question=question)
