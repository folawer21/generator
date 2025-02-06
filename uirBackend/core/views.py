import json
from django.http import JsonResponse
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt  # для отключения CSRF для POST-запросов
from .utils import get_all_generated_tests, get_all_characteristics, get_all_questions_with_answers, get_unique_questions_with_answers,generate_test_by_characteristic
# Получите путь к файлу с моковыми данными
mock_data_path = os.path.join(settings.BASE_DIR, 'core', 'mock_data.json')

# Загрузите моковые данные из файла
with open(mock_data_path, 'r') as file:
    mock_data = json.load(file)

def get_questions(request):
    return JsonResponse(get_all_questions_with_answers(), safe=False)

@csrf_exempt  # Этот декоратор отключает проверку CSRF для этой функции
def generate_test(request):
    # Получаем данные из тела запроса
    if request.method == "POST":
        try:
            # Десериализуем JSON из тела запроса
            data = json.loads(request.body)
            
            # Извлекаем список характеристик
            characteristics = data.get("characteristics", [])
            
            if characteristics:
                return JsonResponse(generate_test_by_characteristic(characteristics), safe=False)
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