import json
from django.conf import settings
import os

from .models import Question, AnswerWeight, CombinedTest, CombinedTestQuestion, Characteristic, Answer

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

