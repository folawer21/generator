# from rest_framework import viewsets
# from .models import Question, Answer, Characteristic, GeneratedTest
# from .serializers import QuestionSerializer, AnswerSerializer, CharacteristicSerializer, GeneratedTestSerializer

# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

# class AnswerViewSet(viewsets.ModelViewSet):
#     queryset = Answer.objects.all()
#     serializer_class = AnswerSerializer

# class CharacteristicViewSet(viewsets.ModelViewSet):
#     queryset = Characteristic.objects.all()
#     serializer_class = CharacteristicSerializer

# class GeneratedTestViewSet(viewsets.ModelViewSet):
#     queryset = GeneratedTest.objects.all()
#     serializer_class = GeneratedTestSerializer

import json
from django.http import JsonResponse
from django.conf import settings
import os

# Получите путь к файлу с моковыми данными
mock_data_path = os.path.join(settings.BASE_DIR, 'core', 'mock_data.json')

# Загрузите моковые данные из файла
with open(mock_data_path, 'r') as file:
    mock_data = json.load(file)

def get_questions(request):
    return JsonResponse(mock_data['questions'], safe=False)

def get_characteristics(request):
    return JsonResponse(mock_data['characteristics'], safe=False)

def get_generated_tests(request):
    return JsonResponse(mock_data['generated_tests'], safe=False)