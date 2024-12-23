from rest_framework import serializers
from .models import Question, Answer, Characteristic, GeneratedTest

class AnswerSerializer(serializers.ModelSerializer):
    # Соответствует `export type answer = { id: number; text: string; };`
    class Meta:
        model = Answer
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    # Используем AnswerSerializer для представления связанных объектов
    answers = AnswerSerializer(many=True)

    # Соответствует `export type TQuestion = { id: number; text: string; answers: answer[]; };`
    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']

class CharacteristicSerializer(serializers.ModelSerializer):
    # Соответствует `export type TCharacteristics = { id: number; name: string; usage: boolean; };`
    class Meta:
        model = Characteristic
        fields = ['id', 'name', 'usage']

class GeneratedTestSerializer(serializers.ModelSerializer):
    # Соответствует `export type TGeneratedTests = { id: number; testName: string; characteristicsList: string; questionCount: number };`
    # Обратите внимание на изменение имени поля 'test_name' на 'testName' и 'characteristics_list' на 'characteristicsList'

    testName = serializers.CharField(source='test_name')
    characteristicsList = serializers.CharField(source='characteristics_list')

    class Meta:
        model = GeneratedTest
        fields = ['id', 'testName', 'characteristicsList', 'question_count']