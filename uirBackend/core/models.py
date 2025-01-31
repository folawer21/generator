from django.db import models

class Answer(models.Model):
    # Соответствует `export type answer = { id: number; text: string; };`
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Question(models.Model):
    # Соответствует `export type TQuestion = { id: number; text: string; answers: answer[]; };`
    text = models.CharField(max_length=255)
    answers = models.ManyToManyField(Answer, related_name='questions')

    def __str__(self):
        return self.text

class Characteristic(models.Model):
    name = models.CharField(max_length=255)
    usage = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class GeneratedTest(models.Model):
    # Соответствует `export type TGeneratedTests = { id: number; testName: string; charachteristicsList: string; questionCount: number };`
    # Изменение - 'charachteristicsList' исправлено на 'characteristicsList'
    test_name = models.CharField(max_length=255)
    characteristics_list = models.TextField()  # здесь используется текст, но может быть преобразовано в JSON, если это необходимо
    question_count = models.IntegerField()

    def __str__(self):
        return self.test_name