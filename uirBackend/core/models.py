from django.db import models

class Test(models.Model):
    test_name = models.CharField(max_length=255)
    question_count = models.IntegerField()
    characteristics = models.TextField()

    def __str__(self):
        return self.test_name
class Scale(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='scales')
    trait = models.CharField(max_length=255)
    min_score = models.IntegerField()
    max_score = models.IntegerField()

    def __str__(self):
        return f"{self.trait} ({self.min_score}-{self.max_score})"
    
class Characteristic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()

    def __str__(self):
        return self.question_text
    
    def get_traits(self):
        """
        Получает список характеристик для этого вопроса через AnswerWeight.
        """
        return [aw.trait for aw in self.answerweight_set.all()]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.TextField()

    def __str__(self):
        return self.answer_text

class AnswerWeight(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    trait = models.ForeignKey(Characteristic, on_delete=models.CASCADE)
    weight = models.IntegerField()
    answer = models.ForeignKey(Answer, related_name='weights', on_delete=models.CASCADE)  # Связь с ответом

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

class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return f"{self.full_name} ({self.group.name})"


class Temperament(models.Model):
    temperament_type = models.CharField(max_length=255)

    def __str__(self):
        return self.temperament_type


class RepresentationalSystem(models.Model):
    system_type = models.CharField(max_length=255)

    def __str__(self):
        return self.system_type


class LearningRecommendation(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="learning_recommendation")
    recommendation_text = models.TextField()

    def __str__(self):
        return f"Рекомендация для {self.student.full_name}: {self.recommendation_text}"


class PsychProfileTrait(models.Model):
    portrait = models.ForeignKey("PsychologicalPortrait", on_delete=models.CASCADE, related_name="traits")
    trait_name = models.CharField(max_length=255)  
    trait_value = models.CharField(max_length=255)  

    def __str__(self):
        return f"{self.trait_name}: {self.trait_value}"


class PsychologicalPortrait(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="psychological_portrait")
    temperament = models.ForeignKey(Temperament, on_delete=models.SET_NULL, null=True, blank=True, related_name="portraits")
    representational_system = models.ForeignKey(RepresentationalSystem, on_delete=models.SET_NULL, null=True, blank=True, related_name="portraits")
    recommendations = models.TextField(blank=True)

    def __str__(self):
        return f"Психологический портрет для {self.student.full_name}"

    def create_traits(self, trait_objs):
        for trait in trait_objs:
            PsychProfileTrait.objects.create(
                portrait=self,
                trait_name=trait.trait_name,
                trait_value=random.choice([trait.name_left, trait.name_right])
            )