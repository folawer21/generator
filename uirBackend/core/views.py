import json
from django.http import JsonResponse
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt  # для отключения CSRF для POST-запросов
from .utils import get_all_generated_tests, get_all_characteristics, get_all_questions_with_answers, delete_combined_test_by_id, get_combined_test_questions, get_all_groups_with_students, get_student_psychological_portrait, submit_test_results, generate_test_by_characteristics 
# Получите путь к файлу с моковыми данными
mock_data_path = os.path.join(settings.BASE_DIR, 'core', 'mock_data.json')

# Загрузите моковые данные из файла
with open(mock_data_path, 'r') as file:
    mock_data = json.load(file)

def get_questions(request):
    return JsonResponse(get_all_questions_with_answers(), safe=False)

# @csrf_exempt  # Этот декоратор отключает проверку CSRF для этой функции
# def generate_test(request):
#     # Получаем данные из тела запроса
#     if request.method == "POST":
#         try:
#             # Десериализуем JSON из тела запроса
#             data = json.loads(request.body)
            
#             # Извлекаем список характеристик
#             characteristics = data.get("characteristics", [])
#             name = data.get("test_name")
            
#             if characteristics:
#                 if name:
#                     return JsonResponse(generate_test_by_characteristic(characteristics,name), safe=False)
#                 return JsonResponse(generate_test_by_characteristic(characteristics), safe=False)
                
#             else:
#                 return JsonResponse({"error": "Характеристики ил не переданы"}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Неверный формат данных"}, status=400)
#     else:
#         return JsonResponse({"error": "Метод запроса должен быть POST"}, status=405)

@csrf_exempt  # Этот декоратор отключает проверку CSRF для этой функции
def generate_test(request):
    if request.method == "POST":
        try:
            # Десериализуем JSON из тела запроса
            data = json.loads(request.body)
            
            # Извлекаем список характеристик
            characteristics = data.get("characteristics", [])
            name = data.get("test_name")
            
            if characteristics:
                # Вызов функции для генерации теста
                result = generate_test_by_characteristics(characteristics, name)
                
                return JsonResponse(result, safe=False)
            else:
                return JsonResponse({"error": "Характеристики не переданы"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный формат данных"}, status=400)
    else:
        return JsonResponse({"error": "Метод запроса должен быть POST"}, status=405)

def get_characteristics(request):
    return JsonResponse(get_all_characteristics(), safe=False)

def get_generated_tests(request):
    return JsonResponse(get_all_generated_tests(), safe=False)

@csrf_exempt  # Отключает CSRF-защиту для тестирования, удалите это в продакшене
def delete_combined_test(request):
    """
    Удаляет комбинированный тест по ID, полученному из JSON-запроса.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Метод не разрешен'}, status=405)

    try:
        data = json.loads(request.body)
        test_id = data.get('id')  # ID теста передается в теле запроса
        if not test_id:
            return JsonResponse({'status': 'error', 'message': 'ID теста не передан'}, status=400)

        delete_combined_test_by_id(test_id)
        return JsonResponse({'status': 'success', 'message': 'Тест успешно удален'})
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Некорректный JSON'}, status=400)
    
    except CombinedTest.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Комбинированный тест не найден'}, status=404)
    
@csrf_exempt
def get_combined_test(request):
    """
    Возвращает список вопросов комбинированного теста по ID, полученному из JSON-запроса.
    """
    print("Request received")  # Выводим, когда запрос пришел

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Data received:", data)  # Печатаем полученные данные
            test_id = data.get('id')  # Получаем ID из тела запроса
            if not test_id:
                return JsonResponse([], status=400)

            questions = get_combined_test_questions(test_id)

            print(f"questions: {questions} ")
            return JsonResponse(questions, safe=False)  # Передаем вопросы в ответе

        except json.JSONDecodeError:
            return JsonResponse([], status=400)
        except CombinedTest.DoesNotExist:
            return JsonResponse([], status=404)
        except Exception as e:
            print(f"Error: {e}")  # Печатаем ошибку, если возникла проблема
            return JsonResponse([], status=500)
    else:
        return JsonResponse([], status=405)

def get_characteristics(request):
    return JsonResponse(get_all_characteristics(), safe=False)


def get_generated_tests(request):
    return JsonResponse(get_all_generated_tests(), safe=False)


def get_groups_with_students(request):
    """
    Возвращает список групп с вложенными списками студентов.
    """
    return JsonResponse(get_all_groups_with_students(), safe=False)


def get_psychological_portrait(request, student_id):
    """
    Возвращает психологический портрет конкретного студента по его ID.
    """
    return JsonResponse(get_student_psychological_portrait(student_id), safe=False)

@csrf_exempt
def submit_results_from_test(request):
    return submit_test_results(request)

