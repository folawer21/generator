from .determine_temp import process_temp_test
from .determine_reps_system import  process_rep_system_test
from .determine_other_charactetistics import determine_dominant_trait, process_other_tests
from .preffered_tasks import get_tasks_by_traits
import json
from core.models import *

def pretty_print_portrait(portrait):
    # Добавляем смайлик для Темперамента
    print(f"🌟 Темперамент: {portrait['Темперамент']}")

    # Добавляем смайлик для Репрезентативной системы личности
    print(f"🧠 Репрезентативная система личности: {portrait['Репрезентативная система личности']}")

    # Выводим остальные характеристики с красивыми смайликами
    print("📝 Остальные характеристики:")
    for category, traits in portrait["Остальные характеристики"].items():
        print(f"  ➡️ {category}:")
        for trait in traits:
            print(f"    - {trait}")

    # Выводим подходящие обучающие воздействия с эмодзи
    print("📚 Подходящие обучающие воздействия:")
    for uz in portrait["Подходящие обучающие воздействия"]:
        print(f"  - {uz} 🎯")


def save_portrait_to_json(portrait, filename="output/portrait.json"):
    # Сохраняем портрет в JSON без изменений
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(portrait, f, ensure_ascii=False, indent=4)
    print(f"Портрет сохранен в файл: {filename}")

def process_psychological_test(tests, responses, tasks):
    print("🛠️ Начинаем обработку психологического теста...")

    # Шаг 1: Обработка теста на темперамент
    dominant_temp, scores, temp_tests = process_temp_test(tests, responses)

    # Шаг 2: Обработка теста на репрезентативную систему личности
    dominant_rep_system, scores, rep_tests = process_rep_system_test(tests, responses)

    # Шаг 3: Обработка остальных тестов
    other_results = process_other_tests(tests, responses)
    remaining_scores = other_results["scores"]
    # interpretations = other_results["interpretations"]
    dominant_traits = other_results["dominant_traits"]
    print("✅ Обработка теста завершена.")

    # Фильтруем только доминирующие черты
    dominant_only_scores = other_results["dominant_traits"]
    dominant_charachteristics = dominant_only_scores + [dominant_temp, dominant_rep_system]
    preffered_utz = get_tasks_by_traits(traits= dominant_charachteristics, data=tasks)
    # Финальный портрет
    final_portrait = {
        "Темперамент": dominant_temp,
        "Репрезентативная система личности": dominant_rep_system,
        "Остальные характеристики": {
            "Доминирующие черты": dominant_only_scores,
            # "Интерпретации": all_interpretations
        },
        "Подходящие обучающие воздействия": preffered_utz
    }

    print("\n📝 Окончательный психологический портрет:")
    return final_portrait

from core.models import (
    Temperament, RepresentationalSystem,
    LearningRecommendation, Student, Group
)
def save_portrait_to_db(final_portrait: dict, student_id: int = 0):
    # Попробуем найти студента, если нет — создадим
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        print(f"⚠️ Студент с ID {student_id} не найден. Создаём нового студента...")
        
        # Создаём или получаем заглушечную группу
        group, _ = Group.objects.get_or_create(name="Заглушка-группа")
        
        # Создаём студента
        student = Student.objects.create(
            id=student_id,
            full_name=f"Студент {student_id}",
            group=group
        )

    # Создаем психологический портрет
    portrait = PsychologicalPortrait.objects.create(
        student=student,
        temperament=Temperament.objects.create(
            temperament_type=final_portrait.get("Темперамент", "Неизвестно")
        ),
        representational_system=RepresentationalSystem.objects.create(
            system_type=final_portrait.get("Репрезентативная система личности", "Неизвестно")
        ),
        recommendations="\n".join(final_portrait.get("Подходящие обучающие воздействия", []))
    )

    # Сохраняем черты личности
    traits = final_portrait.get("Остальные характеристики", {}).get("Доминирующие черты", [])
    for trait in traits:
        if isinstance(trait, str) and ":" in trait:
            trait_name, trait_value = map(str.strip, trait.split(":", 1))
        else:
            trait_name = "Характеристика"
            trait_value = trait if isinstance(trait, str) else str(trait)

        # Создаем черту личности для психологического портрета
        PsychProfileTrait.objects.create(
            portrait=portrait,
            trait_name=trait_name,
            trait_value=trait_value
        )

    print(f"✅ Психологический портрет для студента {student.full_name} сохранён в базе.")

def process_answers(full_name, group_name, answers):
    group, _ = Group.objects.get_or_create(name=group_name)
    student, _ = Student.objects.get_or_create(full_name=full_name, group=group)
    tests = list(Test.objects.all())
    tasks = list(LearningRecommendation.objects.all())  
    responses = {int(qid): aid for qid, aid in answers.items()}
    final_portret = process_psychological_test(tests= tests, tasks= tasks, responses= responses)
    pretty_print_portrait(final_portret)
    # student = Student.objects.create(full_name=full_name, group_name=group_name)
    # save_portrait_to_db(final_portret, student.id)
