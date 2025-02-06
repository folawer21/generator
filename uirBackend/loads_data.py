import os
import django
import json

# Настроим Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uirBackend.settings')
django.setup()

from core.models import Test, Characteristic, Question, Answer, AnswerWeight, CombinedTest, CombinedTestQuestion

# Путь к JSON файлу с тестами
file_paths = [
    'output/input_data.json',      # Тесты с вопросами
    'output/combined_test.json',   # Комбинированный тест
]

# Процесс загрузки данных
for file_path in file_paths:
    try:
        print(f'Обрабатывается файл: {file_path}')
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        if file_path == 'output/input_data.json':
            print('Загружаем обычные тесты')
            # Загрузка обычных тестов
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

        elif file_path == 'output/combined_test.json':
            print('Загружаем комбинированный тест')
            # Загрузка комбинированного теста
            combined_test_name = json_data.get("combined_test_name")
            characteristics = json_data.get("characteristics")

            combined_test = CombinedTest.objects.create(combined_test_name=combined_test_name, characteristics=characteristics)

            for test_data in json_data.get("tests", []):
                test_name = test_data.get("test_name")
                questions_count = test_data.get("questions_count")

                # Получаем тест по имени
                try:
                    test = Test.objects.get(test_name=test_name)
                except Test.DoesNotExist:
                    print(f'Тест с именем {test_name} не найден')
                    continue

                questions = test.question_set.all()[:questions_count]

                for question in questions:
                    CombinedTestQuestion.objects.create(combined_test=combined_test, original_test=test, question=question)

        print(f'Успешно загружены данные из {file_path}')
    except Exception as e:
        print(f'Ошибка при загрузке данных из {file_path}: {e}')
