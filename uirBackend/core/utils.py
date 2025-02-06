import json
from django.conf import settings
import os
from collections import defaultdict
from .models import Question, AnswerWeight, CombinedTest, CombinedTestQuestion, Characteristic, Answer, Test

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

    :return: список характеристик с объединенными характеристиками для каждого теста
    """
    # Получаем все тесты и их характеристики
    tests = Test.objects.all()
    test_characteristics = defaultdict(list)

    # Группируем характеристики по тестам
    for test in tests:
        for question in test.question_set.all():
            for answer_weight in question.answerweight_set.all():
                # Добавляем характеристику для каждого теста
                characteristic = answer_weight.trait
                if characteristic.name not in test_characteristics[test.id]:
                    test_characteristics[test.id].append(characteristic.name)

    # Формируем результат
    result = []
    for test_id, characteristics in test_characteristics.items():
        # Объединяем характеристики в одну строку с разделителем '/'
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


def get_tests_by_characteristics(characteristics_list):
    """
    Получает список тестов, которые выявляют переданные характеристики, 
    выбирает уникальные вопросы для каждой характеристики и возвращает результат в виде JSON-структуры.
    """
    # Словарь, который будет хранить результаты по каждой характеристике
    characteristics_questions = {}
    original_tests = set()

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
            original_tests.add(question.test)
        # Для каждой характеристики выбираем только один вопрос (например, первый)
        if unique_questions:
            characteristics_questions[characteristic_name] = [{
                "id": question.id,
                "text": question.question_text
            } for question in unique_questions]

    return characteristics_questions, original_tests

def get_unique_questions_with_answers(characteristics_list):
    """
    Получает список вопросов из get_tests_by_characteristics(),
    убирает дубликаты и добавляет ответы к каждому вопросу.
    """
    # Получаем вопросы по характеристикам
    characteristics_questions, original_tests = get_tests_by_characteristics(characteristics_list)

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

    return questions_list, original_tests

def save_combined_test_to_db(generated_test_name, characteristics_list, questions_list, original_tests):
    """
    Сохраняет комбинированный тест в базу данных, добавляет вопросы с привязкой к исходным тестам.
    """
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
        original_test = next(test for test in original_tests if test.test_name == question.test.test_name)

        # Создаем запись в CombinedTestQuestion
        CombinedTestQuestion.objects.create(
            combined_test=combined_test,
            original_test=original_test,
            question=question
        )

    return combined_test


def generate_test_by_characteristic(characteristics_list,test_name = "Новый тест"):
    test, original_tests = get_unique_questions_with_answers(characteristics_list)
    save_combined_test_to_db(test_name,characteristics_list,test,original_tests)

    return test

