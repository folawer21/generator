import json
from django.conf import settings
import os

from .models import Question, AnswerWeight, CombinedTest, CombinedTestQuestion, Characteristic, Answer

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
    Получает список всех уникальных характеристик из базы данных.

    :return: список характеристик (например, ["Тип мышления", "Общительность", "Доброжелательность"])
    """
    characteristics = Characteristic.objects.all()
    return [{"id": characteristic.id, "name": characteristic.name} for characteristic in characteristics]



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


def get_tests_by_characteristics(characteristics_list):
    """
    Получает список тестов, которые выявляют переданные характеристики, 
    выбирает уникальные вопросы для каждой характеристики и возвращает результат в виде JSON-структуры.
    """
    # Словарь, который будет хранить результаты по каждой характеристике
    characteristics_questions = {}

    # Перебираем все характеристики, которые переданы на backend
    for characteristic_name in characteristics_list:
        # Получаем все веса ответов, связанные с данной характеристикой
        answer_weights = AnswerWeight.objects.filter(trait__name=characteristic_name)
        
        # Для данной характеристики собираем уникальные вопросы
        unique_questions = set()

        for answer_weight in answer_weights:
            question = answer_weight.question
            # Добавляем вопросы в множество, чтобы исключить дубли
            unique_questions.add(question)

        # Для каждой характеристики выбираем только один вопрос (например, первый)
        if unique_questions:
            characteristics_questions[characteristic_name] = [{
                "id": question.id,
                "text": question.question_text
            } for question in unique_questions]

    return characteristics_questions

def get_unique_questions_with_answers(characteristics_list):
    """
    Получает список вопросов из get_tests_by_characteristics(),
    убирает дубликаты и добавляет ответы к каждому вопросу.
    """
    # Получаем вопросы по характеристикам
    characteristics_questions = get_tests_by_characteristics(characteristics_list)

    # Используем словарь, чтобы избежать дублирования вопросов
    unique_questions = {}

    for characteristic, questions in characteristics_questions.items():
        for question_data in questions:  # Теперь это список, а не словарь
            question_id = question_data["id"]

            # Если вопрос уже добавлен, пропускаем его
            if question_id not in unique_questions:
                unique_questions[question_id] = {
                    "id": question_id,
                    "text": question_data["text"],
                    "answers": []
                }

    # Добавляем ответы к каждому уникальному вопросу
    for question_id in unique_questions:
        answers = Answer.objects.filter(question_id=question_id)
        unique_questions[question_id]["answers"] = [
            {"id": answer.id, "text": answer.answer_text} for answer in answers
        ]

    # Преобразуем словарь в список уникальных вопросов
    questions_list = list(unique_questions.values())

    print(f"Данные успешно получены. Количество уникальных вопросов: {questions_list}")

    return questions_list

def generate_test_by_characteristic(characteristics_list):
    test = get_unique_questions_with_answers(characteristics_list)
    generated_test = test
    return test

