import os
import django
import json

# Настроим Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uirBackend.settings')
django.setup()

from core.models import Test, Characteristic, Question, Answer, AnswerWeight, CombinedTest, CombinedTestQuestion, Scale

# Путь к JSON файлу с тестами
file_paths = [
    'output/new_input.json'  # Путь к файлу с тестами
]

# from django.apps import apps

# # Получаем все модели твоего приложения (например, 'core')
# app_models = apps.get_app_config('core').get_models()

# # Удаляем все данные из каждой модели
# for model in app_models:
#     model.objects.all().delete()

# Процесс загрузки данных
for file_path in file_paths:
    try:
        print(f'Обрабатывается файл: {file_path}')
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        if file_path == 'output/new_input.json':
            print('Загружаем обычные тесты')
            for test_data in json_data:
                test_name = test_data.get("test_name")
                characteristics = test_data.get("characteristics")
                question_count = len(test_data['questions'])
                if Test.objects.filter(test_name=test_name).exists():
                    print(f"Тест с названием '{test_name}' уже существует. Пропускаем.")
                    continue
                
                # Создание теста
                test = Test.objects.create(
                    test_name=test_name,
                    characteristics=characteristics,
                    question_count=question_count
                )

                # Загрузка шкал
                scales_data = test_data.get("scales", {})
                for trait_name, bounds in scales_data.items():
                    min_score = bounds.get("min_score", 0)
                    max_score = bounds.get("max_score", 0)
                    Scale.objects.create(
                        test=test,
                        trait=trait_name,
                        min_score=min_score,
                        max_score=max_score
                    )

                # Загрузка вопросов
                print("Загрузка вопросов")
                for question_data in test_data['questions']:
                    question_text = question_data.get("text")
                    question = Question.objects.create(test=test, question_text=question_text)

                    for answer_data in question_data.get('answers', []):
                        answer_text = answer_data.get("answer")
                        weight_dict = answer_data.get("weight", {})

                        # Создание ответа
                        answer = Answer.objects.create(question=question, answer_text=answer_text)

                        # Обработка всех характеристик и их весов в weight
                        for trait_name, weight in weight_dict.items():
                            characteristic, _ = Characteristic.objects.get_or_create(name=trait_name)
                            
                            # Создание записи в AnswerWeight с новой связью
                            AnswerWeight.objects.create(
                                question=question,
                                trait=characteristic,
                                weight=weight,
                                answer=answer  # Теперь связываем AnswerWeight с ответом
                            )

    except Exception as e:
        print(f'Ошибка при обработке файла {file_path}: {e}')
