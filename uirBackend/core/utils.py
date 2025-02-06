# # Получаем все тесты
# tests = Test.objects.all()

# # Можно вывести их на экран (например, для отладки)
# for test in tests:
#     print(test.test_name, test.question_count, test.characteristics)

# # Получаем все комбинированные тесты
# combined_tests = CombinedTest.objects.all()

# # Выводим их на экран
# for combined_test in combined_tests:
#     print(combined_test.combined_test_name, combined_test.characteristics)

# # Получаем список тестов с их вопросами, ответами и весами
# for test in tests:
#     print(f"Тест: {test.test_name}")
    
#     # Получаем все вопросы для данного теста
#     questions = Question.objects.filter(test=test)
    
#     for question in questions:
#         print(f"  Вопрос: {question.question_text}")
        
#         # Получаем все ответы для данного вопроса
#         answers = Answer.objects.filter(question=question)
        
#         for answer in answers:
#             print(f"    Ответ: {answer.answer_text}")
        
#         # Получаем все веса для данного вопроса
#         answer_weights = AnswerWeight.objects.filter(question=question)
        
#         for aw in answer_weights:
#             print(f"    Вес для {aw.trait}: {aw.weight}")

# # Получаем список комбинированных тестов с их вопросами и ответами
# for combined_test in combined_tests:
#     print(f"Комбинированный тест: {combined_test.combined_test_name}")
#     по
#     # Получаем все вопросы для комбинированного теста
#     combined_test_questions = CombinedTestQuestion.objects.filter(combined_test=combined_test)
    
#     for ctq in combined_test_questions:
#         original_test = ctq.original_test  # Оригинальный тест для комбинированного вопроса
#         question = ctq.question  # Вопрос из оригинального теста
        
#         print(f"  Вопрос: {question.question_text} (Оригинальный тест: {original_test.test_name})")
        
#         # Получаем все ответы для данного вопроса
#         answers = Answer.objects.filter(question=question)
        
#         for answer in answers:
#             print(f"    Ответ: {answer.answer_text}")
        
#         # Получаем все веса для данного вопроса
#         answer_weights = AnswerWeight.objects.filter(question=question)
        
#         for aw in answer_weights:
#             print(f"    Вес для {aw.trait}: {aw.weight}")

import json
from django.conf import settings
import os

# Получите путь к файлу с моковыми данными
mock_data_path = os.path.join(settings.BASE_DIR, 'core', 'mock_data.json')

# Загрузите моковые данные из файла
with open(mock_data_path, 'r') as file:
    mock_data = json.load(file)
    
def get_generated_tests(request):
    return JsonResponse(mock_data['generated_tests'], safe=False)

def get_questions(request):
    return JsonResponse(mock_data['questions'], safe=False)

def get_characteristics(request):
    return JsonResponse(mock_data['characteristics'], safe=False)



# #тесты_для_характеристик
# def get_test_ids_by_characteristic(characteristic):
#     return {characteristic: [
#         test["id"]
#         for test in data["tests"]
#         if characteristic.lower() in test["charachteristicsList"].lower()
#     ]}

# def get_tests_for_characteristics(charachteristics: [str]):
#     ids = {}
#     for characteristic in charachteristics:
#         ids.update(get_test_ids_by_characteristic(characteristic))
#     return ids

# def get_guestions_for_test(test):
#     pass

# def get_question_for_tests(tests:[int]):
#     questions = {}
#     for test in tests:
#         questions_for_test = get_guestions_for_test(test)
#         questions[test] = questions_for_test
#     return questions



# # def get_questions_for_charachteristics_list(charachteristics: [str]):
# #     tests = get_tests_for_characteristics(charachteristics)
# #     questions = 


# #гпт 
# from models import Question, AnswerWeight, CombinedTest, CombinedTestQuestion

# def get_questions_by_characteristics(characteristics: list[str]) -> dict:
#     """
#     Получает вопросы, которые связаны с заданными характеристиками.

#     :param characteristics: список характеристик (например, ["Тип мышления", "Общительность"])
#     :return: словарь {характеристика: [вопросы]}
#     """
#     result = {char: [] for char in characteristics}

#     # Получаем все вопросы, у которых есть указанные характеристики
#     answer_weights = AnswerWeight.objects.filter(trait__in=characteristics).select_related("question")

#     for aw in answer_weights:
#         result[aw.trait].append(aw.question.question_text)

#     return result


# def get_all_characteristics() -> list[str]:
#     """
#     Получает список всех уникальных характеристик из базы данных.

#     :return: список характеристик (например, ["Тип мышления", "Общительность", "Доброжелательность"])
#     """
#     return list(AnswerWeight.objects.values_list("trait", flat=True).distinct())


# def get_all_generated_tests() -> list[dict]:
#     """
#     Получает все сгенерированные тесты с их ID, характеристиками и количеством вопросов.

#     :return: список словарей [{id, characteristics, question_count}]
#     """
#     tests = CombinedTest.objects.all()
    
#     result = []
#     for test in tests:
#         question_count = CombinedTestQuestion.objects.filter(combined_test=test).count()
#         result.append({
#             "id": test.id,
#             "characteristics": test.characteristics,
#             "question_count": question_count
#         })
    
#     return result
