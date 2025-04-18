# from core.models import CombinedTestQuestion, Question, Answer, AnswerWeight
# import json

# def get_temp_trait_questions(tests, responses):
#     temperament_traits = {"Сангвиник", "Холерик", "Флегматик", "Меланхолик"}
#     temperament_questions = {}

#     print("📥 responses:", responses)
#     print("🔍 Начинаем извлечение вопросов, касающихся темперамента...")

#     try:
#         # Извлекаем вопросы, соответствующие ID в responses
#         combined_qs = CombinedTestQuestion.objects.filter(id__in=responses.keys()).select_related('question')

#         for cq in combined_qs:
#             question = cq.question
#             traits = set(aw.trait.name.strip() for aw in question.answerweight_set.all())
#             relevant_traits = traits.intersection(temperament_traits)

#             if relevant_traits:
#                 answer = responses.get(cq.id)
#                 print(f"🔸 CombinedQuestion ID {cq.id} → Вопрос ID={question.id}, Черты: {traits}, Пересечение: {relevant_traits}, Ответ: {answer}")

#                 if answer:
#                     temperament_questions[cq.id] = {
#                         "question_text": question.question_text,
#                         "traits": relevant_traits,
#                         "answer": answer,
#                         "question": question
#                     }
#                     print(f"✅ Добавлен вопрос ID={cq.id}")
#         print(f"📝 Всего отобрано {len(temperament_questions)} вопросов для анализа темперамента.")
#     except Exception as e:
#         print(f"❌ Ошибка при извлечении: {e}")

#     return temperament_questions


# def calculate_temp_scores(temperament_questions):
#     scores = {trait: 0 for trait in ["Сангвиник", "Холерик", "Флегматик", "Меланхолик"]}

#     print("📊 Начинаем подсчет баллов для каждого типа темперамента...")
#     try:
#         for question_id, question_data in temperament_questions.items():
#             question = question_data["question"]  # это Question или CombinedTestQuestion
#             answer_id = question_data["answer"]   # это ID ответа

#             # Если вопрос комбинированный, обрабатываем его напрямую
#             if isinstance(question, CombinedTestQuestion):
#                 # В случае комбинированного вопроса ищем исходный вопрос
#                 question = question.question
#                 print(f"🔄 Комбинированный вопрос ID {question_id} -> исходный вопрос ID {question.id}")

#             # Ищем ответ с нужным ID для текущего вопроса
#             answer = question.answer_set.filter(id=answer_id).first()
#             if not answer:
#                 print(f"⚠️ Не найден ответ с id {answer_id} для вопроса {question_id}")
#                 continue

#             # Подсчитываем баллы для всех черт
#             for aw in answer.answerweight_set.all():
#                 trait = aw.trait.name.strip()
#                 if trait in scores:
#                     scores[trait] += aw.weight
#                     print(f"✅ Вопрос {question_id}: ответ '{answer.answer_text}', вес для {trait}: {aw.weight}")

#         print(f"📈 Подсчитаны баллы: {scores}")
#     except Exception as e:
#         print(f"❌ Ошибка при подсчёте баллов: {e}")
#     return scores

# def determine_dominant_temp(scores):
#     print("🔍 Определяем доминирующий тип темперамента...")
#     try:
#         sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

#         if sorted_scores[0][1] > sorted_scores[1][1]:
#             dominant_type = sorted_scores[0][0]
#             print(f"🏆 Доминирующий тип темперамента: {dominant_type}")
#             return dominant_type
#         elif sorted_scores[0][1] == sorted_scores[1][1]:
#             mixed_type = f"{sorted_scores[0][0]}-{sorted_scores[1][0]}"
#             print(f"⚖️ Смешанный тип темперамента: {mixed_type}")
#             return mixed_type
#         else:
#             print("❓ Неопределённый тип темперамента.")
#             return "Смешанный тип (неопределённый)"
#     except Exception as e:
#         print(e)


# def process_temp_test(tests, responses):
#     print("🛠️ Начинаем обработку теста на темперамент...")

#     # Шаг 1.1 - Извлечение вопросов, которые касаются темперамента
#     temperament_questions = get_temp_trait_questions(tests, responses)

#     # Шаг 1.2 - Подсчет баллов для каждого типа темперамента
#     scores = calculate_temp_scores(temperament_questions)
#     # Шаг 1.3 - Определение доминирующего типа темперамента
#     dominant_temp = determine_dominant_temp(scores)

#     print(f"✅ Обработка теста завершена. Доминирующий тип темперамента: {dominant_temp}")

#     return dominant_temp, scores, temperament_questions

from core.models import CombinedTestQuestion, Question, Answer, AnswerWeight, Characteristic
import json

from django.db.models import Prefetch

def get_temp_trait_questions(tests, responses):
    temperament_traits = {"Сангвиник", "Холерик", "Флегматик", "Меланхолик"}
    temperament_questions = {}

    print("📥 responses:", responses)
    print("🔍 Начинаем извлечение вопросов, касающихся темперамента...")

    try:
        # Извлекаем вопросы по ID из обычной таблицы Question и предварительно подгружаем связанные AnswerWeight
        question_ids = list(responses.keys())  # Собираем ID вопросов из responses
        answerweight_prefetch = Prefetch('answerweight_set', queryset=AnswerWeight.objects.all())

        questions = Question.objects.filter(id__in=question_ids).prefetch_related(answerweight_prefetch)

        if not questions:
            print(f"❌ Не найдены вопросы с такими ID в базе данных: {question_ids}")

        for question in questions:
            traits = set(aw.trait.name.strip() for aw in question.answerweight_set.all())
            relevant_traits = traits.intersection(temperament_traits)

            if relevant_traits:
                answer_id = responses.get(question.id)  # Получаем ID ответа из responses
                print(f"🔸 Вопрос ID {question.id} → Черты: {traits}, Пересечение: {relevant_traits}, Ответ: {answer_id}")

                if answer_id:
                    temperament_questions[question.id] = {
                        "question_text": question.question_text,
                        "traits": relevant_traits,
                        "answer": answer_id,
                        "question": question
                    }
                    print(f"✅ Добавлен вопрос ID={question.id}")
        print(f"📝 Всего отобрано {len(temperament_questions)} вопросов для анализа темперамента.")
    except Exception as e:
        print(f"❌ Ошибка при извлечении: {e}")

    return temperament_questions



def calculate_temp_scores(temperament_questions):
    scores = {trait: 0 for trait in ["Сангвиник", "Холерик", "Флегматик", "Меланхолик"]}

    print("📊 Начинаем подсчет баллов для каждого типа темперамента...")
    try:
        for question_id, question_data in temperament_questions.items():
            question = question_data["question"]
            answer_id = question_data["answer"]

            # Получаем ответ
            answer = Answer.objects.filter(id=answer_id).first()
            if not answer:
                print(f"⚠️ Не найден ответ с id {answer_id} для вопроса {question_id}")
                continue

            # Теперь получаем веса, связанные с этим конкретным ответом
            answer_weights = AnswerWeight.objects.filter(answer=answer)

            for aw in answer_weights:
                trait = aw.trait.name.strip()
                if trait in scores:
                    scores[trait] += aw.weight
                    print(f"✅ Вопрос {question_id}: ответ '{answer.answer_text}', вес для {trait}: {aw.weight}")
                else:
                    print(f"⚠️ Черта {trait} не входит в перечень темпераментов")

        print(f"📈 Подсчитаны баллы: {scores}")
    except Exception as e:
        print(f"❌ Ошибка при подсчёте баллов: {e}")
    return scores




def determine_dominant_temp(scores):
    print("🔍 Определяем доминирующий тип темперамента...")
    try:
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        if sorted_scores[0][1] > sorted_scores[1][1]:
            dominant_type = sorted_scores[0][0]
            print(f"🏆 Доминирующий тип темперамента: {dominant_type}")
            return dominant_type
        elif sorted_scores[0][1] == sorted_scores[1][1]:
            mixed_type = f"{sorted_scores[0][0]}-{sorted_scores[1][0]}"
            print(f"⚖️ Смешанный тип темперамента: {mixed_type}")
            return mixed_type
        else:
            print("❓ Неопределённый тип темперамента.")
            return "Смешанный тип (неопределённый)"
    except Exception as e:
        print(e)

def process_temp_test(tests, responses):
    print("🛠️ Начинаем обработку теста на темперамент...")

    # Шаг 1.1 - Извлечение вопросов, которые касаются темперамента
    temperament_questions = get_temp_trait_questions(tests, responses)

    # Шаг 1.2 - Подсчет баллов для каждого типа темперамента
    scores = calculate_temp_scores(temperament_questions)
    # Шаг 1.3 - Определение доминирующего типа темперамента
    dominant_temp = determine_dominant_temp(scores)

    print(f"✅ Обработка теста завершена. Доминирующий тип темперамента: {dominant_temp}")

    return dominant_temp, scores, temperament_questions
