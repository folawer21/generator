import json
from django.conf import settings
import os

from .models import Question, AnswerWeight, CombinedTest, CombinedTestQuestion

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


def get_all_characteristics() -> list[str]:
    """
    Получает список всех уникальных характеристик из базы данных.

    :return: список характеристик (например, ["Тип мышления", "Общительность", "Доброжелательность"])
    """
    return list(AnswerWeight.objects.values_list("trait", flat=True).distinct())

import logging
logger = logging.getLogger(__name__)


def get_all_generated_tests() -> list[dict]:
    """
    Получает все сгенерированные тесты с их ID, характеристиками и количеством вопросов.
    """
    print("Запрос поступил!")
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