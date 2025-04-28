import json
from django.conf import settings
import os
import random
from collections import defaultdict
from .models import Question, AnswerWeight, CombinedTest, CombinedTestQuestion, Characteristic, Answer, Test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from PsyhPortret.build_portret import process_answers

import logging
# Инициализируем логгер
logger = logging.getLogger(__name__)

generated_test = []

def get_questions_by_characteristics(characteristics: list[str]) -> dict:
    """
    Получает вопросы, которые связаны с заданными характеристиками.

    :param characteristics: список характеристик (например, ["Тип мышления", "Общительность"])
    :return: словарь {характеристика: [вопросы]}
    """
    result = {char: [] for char in characteristics}

    # Получаем все вопросы, у которых есть указанные характеристики
    answer_weights = AnswerWeight.objects.filter(trait__in=characteristics).select_related("question")

    for aw in answer_weights:
        result[aw.trait].append(aw.question.question_text)

    return result

def get_all_characteristics():
    """
    Получает список всех уникальных характеристик из базы данных, объединяя характеристики для каждого теста в одну строку.
    """
    tests = Test.objects.all()
    test_characteristics = defaultdict(list)

    for test in tests:
        for question in test.questions.all():  # ✅ используем правильный related_name
            for answer_weight in question.answerweight_set.all():
                characteristic = answer_weight.trait
                if characteristic.name not in test_characteristics[test.id]:
                    test_characteristics[test.id].append(characteristic.name)

    result = []
    for test_id, characteristics in test_characteristics.items():
        combined_characteristics = ", ".join(characteristics)
        result.append({
            "id": test_id,
            "name": combined_characteristics
        })
    return result



import logging
logger = logging.getLogger(__name__)


def get_all_generated_tests() -> list[dict]:
    """
    Получает все сгенерированные тесты с их ID, характеристиками и количеством вопросов.
    """
    tests = CombinedTest.objects.all()

    logger.debug("Запрос к базе данных: %s", tests)

    result = []
    for test in tests:
        question_count = CombinedTestQuestion.objects.filter(combined_test=test).count()
        result.append({
            "id": test.id,
            "testName": test.combined_test_name,
            "charachteristicsList": test.characteristics,
            "questionCount": question_count
        })

    logger.debug("Результат: %s", result)
    return result



def get_all_questions_with_answers():
    # Получаем все вопросы и убираем повторяющиеся по тексту
    questions = Question.objects.all()
    
    # Множество для хранения уникальных вопросов по тексту
    seen_questions = set()
    
    formatted_questions = []
    
    for question in questions:
        # Если вопрос с таким текстом еще не добавлен
        if question.question_text not in seen_questions:
            seen_questions.add(question.question_text)
            
            # Получаем все ответы для конкретного вопроса
            answers = Answer.objects.filter(question=question)

            # Формируем структуру данных для фронта
            formatted_questions.append({
                "id": question.id,
                "text": question.question_text,
                "answers": [{"text": answer.answer_text} for answer in answers]
            })

    return formatted_questions


# def get_tests_by_characteristics(characteristics_list):
#     """
#     Получает список тестов, которые выявляют переданные характеристики, 
#     выбирает уникальные вопросы для каждой характеристики и возвращает результат в виде JSON-структуры.
#     """
#     # Разворачиваем вложенные строки с запятыми в отдельные элементы
#     expanded_characteristics = []
#     for characteristic in characteristics_list:
#         expanded_characteristics.extend([char.strip() for char in characteristic.split(",")])

#     characteristics_list = expanded_characteristics

#     # Словарь, который будет хранить результаты по каждой характеристике
#     characteristics_questions = {}
#     original_tests = set()

#     # Перебираем все характеристики, которые переданы на backend
#     for characteristic_name in characteristics_list:
#         # Получаем все веса ответов, связанные с данной характеристикой
#         answer_weights = AnswerWeight.objects.filter(trait__name=characteristic_name)
        
#         # Для данной характеристики собираем уникальные вопросы
#         unique_questions = set()

#         for answer_weight in answer_weights:
#             question = answer_weight.question
#             # Добавляем вопросы в множество, чтобы исключить дубли
#             unique_questions.add(question)
#             original_tests.add(question.test)
#         # Для каждой характеристики выбираем только один вопрос (например, первый)
#         if unique_questions:
#             characteristics_questions[characteristic_name] = [{
#                 "id": question.id,
#                 "text": question.question_text
#             } for question in unique_questions]

#     return characteristics_questions, original_tests


# def get_unique_questions_with_answers(characteristics_list):
#     """
#     Получает список вопросов из get_tests_by_characteristics(),
#     убирает дубликаты и добавляет ответы к каждому вопросу.
#     """
#     # Получаем вопросы по характеристикам
#     characteristics_questions, original_tests = get_tests_by_characteristics(characteristics_list)

#     # Используем словарь, чтобы избежать дублирования вопросов
#     unique_questions = {}

#     for characteristic, questions in characteristics_questions.items():
#         for question_data in questions:  # Теперь это список, а не словарь
#             question_id = question_data["id"]

#             # Если вопрос уже добавлен, пропускаем его
#             if question_id not in unique_questions:
#                 unique_questions[question_id] = {
#                     "id": question_id,
#                     "text": question_data["text"],
#                     "answers": []
#                 }

#     # Добавляем ответы к каждому уникальному вопросу
#     for question_id in unique_questions:
#         answers = Answer.objects.filter(question_id=question_id)
#         unique_questions[question_id]["answers"] = [
#             {"id": answer.id, "text": answer.answer_text} for answer in answers
#         ]

#     # Преобразуем словарь в список уникальных вопросов
#     questions_list = list(unique_questions.values())
#     random.shuffle(questions_list)
#     return questions_list[:-5], original_tests

def save_combined_test_to_db(generated_test_name, characteristics_list, questions_list, original_tests):
    """
    Сохраняет комбинированный тест в базу данных, добавляет вопросы с привязкой к исходным тестам.
    """
    logger.info("📥 Сохраняем комбинированный тест в БД...")

    try:
        # Создаем комбинированный тест
        combined_test = CombinedTest.objects.create(
            combined_test_name=generated_test_name,
            characteristics=" / ".join(characteristics_list)  # Соединяем характеристики в строку
        )

        # Добавляем вопросы в комбинированный тест
        for question_data in questions_list:
            # Ищем вопрос в базе данных
            question = Question.objects.get(id=question_data["id"])

            # Сохраняем связь с оригинальными тестами
            # original_test = next(test for test in original_tests if test.test_name == question.test.test_name)
            original_test = next((test for test in original_tests if test.test_name == question.test.test_name), None)
            if original_test is None:
                logger.warning(f"Оригинальный тест для вопроса '{question}' не найден")
                continue

            # Создаем запись в CombinedTestQuestion
            CombinedTestQuestion.objects.create(
                combined_test=combined_test,
                original_test=original_test,
                question=question
            )

        return combined_test
    except Exception as e:
        logger.error(f"Ошибка при сохранении теста: {e}")


# def generate_test_by_characteristic(characteristics_list,test_name = "Новый тест"):
#     test, original_tests = get_unique_questions_with_answers(characteristics_list)
#     save_combined_test_to_db(test_name,characteristics_list,test,original_tests)
#     time.sleep(2.5)
#     return test

@csrf_exempt
def delete_combined_test_by_id(test_id):
    """
    Удаляет комбинированный тест по его ID.

    :param test_id: ID комбинированного теста
    :return: JsonResponse с результатом удаления
    """
    combined_test = get_object_or_404(CombinedTest, id=test_id)
    combined_test.delete()
    return JsonResponse({"message": "Тест успешно удалён"}, status=200)


def get_combined_test_questions(combined_test_id):
    """
    Получает список всех вопросов и ответов для указанного комбинированного теста.

    :param combined_test_id: ID комбинированного теста
    :return: JsonResponse с вопросами и ответами
    """
    questions = CombinedTestQuestion.objects.filter(combined_test_id=combined_test_id)

    result = []
    for entry in questions:
        question = entry.question
        answers = Answer.objects.filter(question=question)

        result.append({
            "id": question.id,
            "text": question.question_text,
            "answers": [{"id": answer.id, "text": answer.answer_text} for answer in answers]
        })

    return result[:-5]

from .models import Student
from collections import defaultdict


def get_all_groups_with_students() -> dict[str, list[dict]]:
    """
    Возвращает словарь, где ключ — название группы, 
    а значение — список студентов в формате { id, fullName }.
    """
    students = Student.objects.all()
    groups = defaultdict(list)

    for student in students:
        groups[student.group.name].append({  # Используем student.group.name для ключа
            "id": student.id,
            "full_name": student.full_name
        })

    return dict(groups)


from .models import PsychologicalPortrait


def get_student_psychological_portrait(student_id: int) -> dict:
    """
    Возвращает психологический портрет студента с указанным ID.
    Включает темперамент, репрезентативную систему, рекомендации и черты личности.
    """
    try:
        portrait = PsychologicalPortrait.objects.select_related(
            "student", "temperament", "representational_system"
        ).prefetch_related("traits").get(student__id=student_id)

        return {
            "studentId": student_id,
            "fullName": portrait.student.full_name,
            "group": portrait.student.group.name,
            "temperament": portrait.temperament.temperament_type if portrait.temperament else None,
            "representationalSystem": portrait.representational_system.system_type if portrait.representational_system else None,
            "recommendations": portrait.recommendations,
            "traits": [
                {
                    "trait": t.trait_name,
                    "value": t.trait_value
                }
                for t in portrait.traits.all()
            ]
        }

    except PsychologicalPortrait.DoesNotExist:
        return {"error": "Психологический портрет не найден"}
@csrf_exempt
def submit_test_results(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            full_name = data.get("fullName")
            group_name = data.get("group")
            answers = data.get("answers")

            print(f"ФИО: {full_name}")
            print(f"Группа: {group_name}")
            print("Ответы:")
            for question_id, answer_id in answers.items():
                print(f"Вопрос {question_id}: Ответ {answer_id}")

            process_answers(full_name=full_name, group_name= group_name, answers= answers)

            return JsonResponse({"status": "ok"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Только POST-запросы разрешены"}, status=405)



from genetics.genetic_algorythm import GeneticTestGenerator
from genetics.question_wrapper import QuestionWrapper
from .models import Question


def generate_test_by_characteristics(characteristics, name="Безымянный"):
    try:
        # Получаем список всех доступных вопросов
        questions = Question.objects.all()

        # Преобразуем вопросы в объекты QuestionWrapper
        question_wrappers = [QuestionWrapper(question) for question in questions]

        # Инициализируем генетический алгоритм с характеристиками
        genetic_algorithm = GeneticTestGenerator(
            question_wrappers, num_generations=25, population_size=int(len(question_wrappers)*0.85), mutation_rate=0.1, lambda1=0.5, lambda2=0.3
        )
        
        # Генерируем тест
        logger.info("🚀 Запуск генетического алгоритма для генерации теста")
        best_chromosome = genetic_algorithm.generate()

        # Получаем выбранные вопросы на основе хромосомы
        selected_questions = [question_wrappers[i] for i in range(len(best_chromosome)) if best_chromosome[i] == 1]

        # Возвращаем результат пользователю (можно отобразить их в JSON)
        selected_questions_text = [q.text for q in selected_questions]
        original_tests = list({q.original.test for q in selected_questions})

        logger.info(f"✅ Генерация завершена. {len(selected_questions_text)} вопросов были выбраны.")
        save_combined_test_to_db(
            generated_test_name=name,
            characteristics_list=characteristics,
            questions_list=[{"id": q.original.id} for q in selected_questions],
            original_tests=original_tests
        )
    
        return {
            'test_name': name if name else "Без названия",
            'selected_questions': selected_questions_text
        }
    except Exception as e:
        logger.error(f"Ошибка при генерации теста: {e}")
        return {"error": "Ошибка при генерации теста"}
    