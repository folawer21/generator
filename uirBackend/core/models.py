from django.db import models

class Test(models.Model):
    test_name = models.CharField(max_length=255)
    question_count = models.IntegerField()
    characteristics = models.TextField()

    def __str__(self):
        return self.test_name

class Characteristic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return self.answer_text

class AnswerWeight(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    trait = models.ForeignKey(Characteristic, on_delete=models.CASCADE)  # Изменили на ForeignKey
    weight = models.IntegerField()

    def __str__(self):
        return f"{self.trait}: {self.weight}"


class CombinedTest(models.Model):
    combined_test_name = models.CharField(max_length=255)
    characteristics = models.TextField()

    def __str__(self):
        return self.combined_test_name

class CombinedTestQuestion(models.Model):
    combined_test = models.ForeignKey(CombinedTest, on_delete=models.CASCADE)
    original_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.combined_test} - {self.question}"

