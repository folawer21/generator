# def get_rep_system_trait_questions(tests, responses):
#     rep_system_traits = ["Визуал", "Аудиал", "Кинестетик"]
#     rep_system_questions = {}

#     print("🔍 Начинаем извлечение вопросов, касающихся репрезентативной системы личности...")

#     for test_id, test in tests.items():
#         for question in test["questions"]:
#             relevant_traits = set(question["traits"]).intersection(set(rep_system_traits))
#             if relevant_traits:
#                 answer = responses.get(question["question_id"])
#                 if answer:
#                     rep_system_questions[question["question_id"]] = {
#                         "question_text": question["text"],
#                         "traits": relevant_traits,
#                         "answer": answer
#                     }
#                     print(f"✅ Вопрос {question['question_id']} найден, относится к характеристикам: {', '.join(relevant_traits)}")

#     print(f"📝 Извлечено {len(rep_system_questions)} вопросов для определения репрезентативной системы личности.")
#     return rep_system_questions


# def calculate_rep_system_scores(tests, rep_system_questions):
#     scores = {trait: 0 for trait in ["Визуал", "Аудиал", "Кинестетик"]}

#     print("📊 Начинаем подсчет баллов для каждого типа репрезентативной системы личности...")

#     for question_id, question_data in rep_system_questions.items():
#         for trait in question_data["traits"]:
#             question = next(q for test in tests.values() for q in test["questions"] if q["question_id"] == question_id)
#             answer_data = next(a for a in question["answers"] if a["answer"] == question_data["answer"])
#             weight = answer_data["weight"].get(trait, 0)
#             scores[trait] += weight
#             print(f"✅ Вопрос {question_id}: ответ '{question_data['answer']}', вес для {trait}: {weight}")

#     print(f"📈 Подсчитаны баллы: {scores}")
#     return scores


# def determine_dominant_rep_system(scores):
#     sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

#     print("🔍 Определяем ведущую репрезентативную систему...")

#     if sorted_scores[0][1] > sorted_scores[1][1]:
#         dominant_system = sorted_scores[0][0]
#         print(f"🏆 Ведущая репрезентативная система: {dominant_system}")
#         return dominant_system
#     elif sorted_scores[0][1] == sorted_scores[1][1]:
#         mixed_system = f"{sorted_scores[0][0]}-{sorted_scores[1][0]}"
#         print(f"⚖️ Смешанная репрезентативная система: {mixed_system}")
#         return mixed_system
#     else:
#         print("❓ Неопределённая репрезентативная система.")
#         return "Смешанная система (неопределённая)"


# def process_rep_system_test(tests, responses):
#     print("🛠️ Начинаем обработку теста на репрезентативную систему личности...")

#     # Шаг 2.1 - Извлечение вопросов, которые касаются репрезентативной системы
#     rep_system_questions = get_rep_system_trait_questions(tests, responses)

#     # Шаг 2.2 - Подсчет баллов для каждого типа репрезентативной системы личности
#     scores = calculate_rep_system_scores(tests, rep_system_questions)

#     # Шаг 2.4 - Определение ведущей репрезентативной системы
#     dominant_rep_system = determine_dominant_rep_system(scores)

#     print(f"✅ Обработка теста завершена. Ведущая репрезентативная система: {dominant_rep_system}")

#     return dominant_rep_system, scores, tests
from core.models import Question, Answer, AnswerWeight
from django.db.models import Prefetch

def get_rep_system_trait_questions(tests, responses):
    rep_system_traits = {"Визуал", "Аудиал", "Кинестетик"}
    rep_system_questions = {}

    print("📥 responses:", responses)
    print("🔍 Начинаем извлечение вопросов, касающихся репрезентативной системы...")

    try:
        question_ids = list(responses.keys())
        answerweight_prefetch = Prefetch('answerweight_set', queryset=AnswerWeight.objects.all())

        questions = Question.objects.filter(id__in=question_ids).prefetch_related(answerweight_prefetch)

        if not questions:
            print(f"❌ Не найдены вопросы с такими ID в базе данных: {question_ids}")

        for question in questions:
            traits = set(aw.trait.name.strip() for aw in question.answerweight_set.all())
            relevant_traits = traits.intersection(rep_system_traits)

            if relevant_traits:
                answer_id = responses.get(question.id)
                print(f"🔸 Вопрос ID {question.id} → Черты: {traits}, Пересечение: {relevant_traits}, Ответ: {answer_id}")

                if answer_id:
                    rep_system_questions[question.id] = {
                        "question_text": question.question_text,
                        "traits": relevant_traits,
                        "answer": answer_id,
                        "question": question
                    }
                    print(f"✅ Добавлен вопрос ID={question.id}")
        print(f"📝 Всего отобрано {len(rep_system_questions)} вопросов для анализа репрезентативной системы.")
    except Exception as e:
        print(f"❌ Ошибка при извлечении: {e}")

    return rep_system_questions


def calculate_rep_system_scores(rep_system_questions):
    scores = {trait: 0 for trait in ["Визуал", "Аудиал", "Кинестетик"]}

    print("📊 Начинаем подсчет баллов для каждого типа репрезентативной системы...")

    try:
        for question_id, question_data in rep_system_questions.items():
            question = question_data["question"]
            answer_id = question_data["answer"]

            answer = Answer.objects.filter(id=answer_id).first()
            if not answer:
                print(f"⚠️ Не найден ответ с id {answer_id} для вопроса {question_id}")
                continue

            answer_weights = AnswerWeight.objects.filter(answer=answer)

            for aw in answer_weights:
                trait = aw.trait.name.strip()
                if trait in scores:
                    scores[trait] += aw.weight
                    print(f"✅ Вопрос {question_id}: ответ '{answer.answer_text}', вес для {trait}: {aw.weight}")
                else:
                    print(f"⚠️ Черта {trait} не входит в перечень репрезентативных систем")

        print(f"📈 Подсчитаны баллы: {scores}")
    except Exception as e:
        print(f"❌ Ошибка при подсчёте баллов: {e}")

    return scores


def determine_dominant_rep_system(scores):
    print("🔍 Определяем ведущую репрезентативную систему...")

    try:
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        if sorted_scores[0][1] > sorted_scores[1][1]:
            dominant_type = sorted_scores[0][0]
            print(f"🏆 Ведущая репрезентативная система: {dominant_type}")
            return dominant_type
        elif sorted_scores[0][1] == sorted_scores[1][1]:
            mixed_type = f"{sorted_scores[0][0]}-{sorted_scores[1][0]}"
            print(f"⚖️ Смешанная репрезентативная система: {mixed_type}")
            return mixed_type
        else:
            print("❓ Неопределённая репрезентативная система.")
            return "Смешанная система (неопределённая)"
    except Exception as e:
        print(f"❌ Ошибка при определении доминирующей системы: {e}")


def process_rep_system_test(tests, responses):
    print("🛠️ Начинаем обработку теста на репрезентативную систему личности...")

    # Шаг 1 - Извлечение вопросов
    rep_system_questions = get_rep_system_trait_questions(tests, responses)

    # Шаг 2 - Подсчет баллов
    scores = calculate_rep_system_scores(rep_system_questions)

    # Шаг 3 - Определение ведущей системы
    dominant_rep_system = determine_dominant_rep_system(scores)

    print(f"✅ Обработка завершена. Ведущая репрезентативная система: {dominant_rep_system}")

    return dominant_rep_system, scores, rep_system_questions
