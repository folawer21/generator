# from django.core.management.base import BaseCommand
# from uirBackend.core.models import Test, Characteristic, Question, Answer, AnswerWeight, CombinedTest, CombinedTestQuestion
# import json

# class Command(BaseCommand):
#     help = 'Загружает данные тестов из JSON файлов в базу данных'

#     def handle(self, *args, **kwargs):
#         # Путь к JSON файлу с тестами
#         file_paths = [
#             'input_data.json',      # Тесты с вопросами
#             'combined_test.json',   # Комбинированный тест
#         ]

#         # Процесс загрузки данных
#         for file_path in file_paths:
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     json_data = json.load(file)

#                 if file_path == 'input_data.json':
#                     self.load_tests(json_data)
#                 elif file_path == 'combined_test.json':
#                     self.load_combined_test(json_data)

#                 self.stdout.write(self.style.SUCCESS(f'Успешно загружены данные из файла {file_path}'))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных из файла {file_path}: {e}'))

#     def load_tests(self, json_data):
#         # Обработка тестов
#         for test_data in json_data:
#             test_name = test_data.get("test_name")
#             characteristics = test_data.get("characteristics")
            
#             # Создание теста
#             test = Test.objects.create(test_name=test_name, characteristics=characteristics, question_count=len(test_data['questions']))
            
#             for question_data in test_data['questions']:
#                 question_text = question_data.get("question_text")
                
#                 # Создание вопроса
#                 question = Question.objects.create(test=test, question_text=question_text)
                
#                 for answer_data in question_data.get('answers', []):
#                     answer_text = answer_data.get("answer_text")
#                     weight = answer_data.get("weight")
#                     trait_name = answer_data.get("trait")
                    
#                     # Создание или получение характеристики
#                     characteristic, created = Characteristic.objects.get_or_create(name=trait_name)
                    
#                     # Создание ответа и веса
#                     answer = Answer.objects.create(question=question, answer_text=answer_text)
#                     AnswerWeight.objects.create(question=question, trait=characteristic, weight=weight)

#     def load_combined_test(self, json_data):
#         # Обработка комбинированного теста
#         combined_test_name = json_data.get("combined_test_name")
#         characteristics = json_data.get("characteristics")

#         combined_test = CombinedTest.objects.create(combined_test_name=combined_test_name, characteristics=characteristics)

#         # Проходим по каждому тесту из комбинированного теста
#         for test_data in json_data.get("tests", []):
#             test_name = test_data.get("test_name")
#             questions_count = test_data.get("questions_count")
            
#             # Получаем тест по имени
#             try:
#                 test = Test.objects.get(test_name=test_name)
#             except Test.DoesNotExist:
#                 self.stdout.write(self.style.ERROR(f'Тест с именем {test_name} не найден'))
#                 continue
            
#             # Выбираем первые несколько вопросов (например, 3-4) из данного теста
#             questions = test.question_set.all()[:questions_count]
            
#             # Добавляем вопросы в комбинированный тест
#             for question in questions:
#                 # Создаём запись о вопросе в комбинированном тесте
#                 CombinedTestQuestion.objects.create(combined_test=combined_test, original_test=test, question=question)
import random
from core.models import (
    Group, Student,
    Temperament, RepresentationalSystem,
    PsychProfileTrait, LearningRecommendation,
    PsychologicalPortrait
)

# Группы и студенты
group_names = ["K09-221", "K09-222", "K09-223", "K07-681"]
students_data = {
    "K07-681": [
        "Автомонов Андрей", "Вареников Александр", "Железняков Евгений",
        "Каширин Станислав", "Кибанов Андрей", "Колесников Павел"
    ],
    "K09-222": ["Шибаев Максим", "Шупейко Никита"],
    "K09-223": ["Иванов Иван", "Петров Петр", "Сидоров Сергей"],
    "K09-221": ["Лебедев Алексей", "Новиков Дмитрий"]
}

# Справочники
temperament_names = ["Сангвиник", "Флегматик", "Холерик", "Меланхолик"]
system_names = ["Визуал", "Аудиал", "Кинестетик", "Дигитал"]

traits_list = [
    ("Интроверсия/Экстраверсия", ["Интроверт", "Экстраверт"]),
    ("Возбудимость/Устойчивость", ["Возбудимый", "Устойчивый"]),
    ("Активность/Пассивность", ["Активный", "Пассивный"]),
    ("Ригидность/Гибкость", ["Гибкий", "Ригидный"]),
    ("Реакция", ["Быстрая", "Медленная"]),
]

# Группы и студенты
def create_group(name):
    return Group.objects.create(name=name)

def create_student(name, group):
    return Student.objects.create(full_name=name, group=group)

# Справочники темпераментов и систем
def prepare_temperaments():
    return [Temperament.objects.create(temperament_type=t) for t in temperament_names]

def prepare_systems():
    return [RepresentationalSystem.objects.create(system_type=s) for s in system_names]

# Справочник черт
def prepare_traits():
    traits = []
    for description, (left, right) in traits_list:
        # Чертой без привязки к психологическому портрету нельзя создать
        traits.append((description, left, right))
    return traits


# Рекомендации по обучению
def create_learning_recommendation(student):
    recommendation_text = "Рекомендуется использовать визуальные материалы и групповые обсуждения."
    return LearningRecommendation.objects.create(student=student, recommendation_text=recommendation_text)

# Психологический портрет
def create_psychological_portrait(student, temperament_objs, system_objs, trait_objs):
    temperament = random.choice(temperament_objs)
    representational_system = random.choice(system_objs)
    recommendation = LearningRecommendation.objects.get(student=student)

    # Создаем психологический портрет
    portrait = PsychologicalPortrait.objects.create(
        student=student,
        temperament=temperament,
        representational_system=representational_system,
        recommendations=recommendation.recommendation_text
    )

    # Теперь создаем PsychProfileTrait после того, как portrait создан
    for trait_description, left, right in trait_objs:
        PsychProfileTrait.objects.create(
            portrait=portrait,  # Ссылка на только что созданный психологический портрет
            trait_name=trait_description,
            trait_value=random.choice([left, right])  # Пример выбора значения для черты
        )

    return portrait

# Основной запуск
def fill_data():
    # Подготовка справочников
    temperament_objs = prepare_temperaments()
    system_objs = prepare_systems()
    trait_objs = prepare_traits()

    # Группы
    groups = {name: create_group(name) for name in group_names}

    for group_name, students in students_data.items():
        group = groups[group_name]
        for student_name in students:
            student = create_student(student_name, group)
            create_learning_recommendation(student)
            create_psychological_portrait(student, temperament_objs, system_objs, trait_objs)

    print("Данные успешно заполнены!")
