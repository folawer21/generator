# from .adjust_scales import adjust_scale_values

# def group_questions_by_trait(tests):
#     """
#     Группировка вопросов по психологическим характеристикам.
#     Обрабатываются только тесты, которые не исключены.
#     """
#     trait_questions = {}

#     print("🔍 Группируем вопросы по психологическим характеристикам...")

#     for test_id, test in tests.items():
#         for question in test["questions"]:
#             for trait in question["traits"]:
#                 if trait not in trait_questions:
#                     trait_questions[trait] = []
#                 trait_questions[trait].append(question)

#     print(f"📝 Группировано {len(trait_questions)} характеристик.")
#     return trait_questions


# def process_user_responses(tests, trait_questions, responses):
#     """
#     Обработка ответов пользователя и подсчет баллов для каждой характеристики.
#     Обрабатываются только тесты, которые не исключены.
#     """
#     scores = {trait: 0 for trait in trait_questions}

#     print("📊 Подсчитываем баллы для каждой характеристики...")

#     for trait, questions in trait_questions.items():
#         for question in questions:
#             answer_data = responses.get(question["question_id"])
#             if answer_data:
#                 answer_weight = next((a["weight"].get(trait, 0) for a in question["answers"] if a["answer"] == answer_data), 0)
#                 scores[trait] += answer_weight
#                 print(f"✅ Вопрос {question['question_id']}: ответ '{answer_data}', вес для {trait}: {answer_weight}")

#     print(f"📈 Подсчитаны баллы: {scores}")
#     return scores


# def adjust_scores_for_number_of_questions(scores, trait_questions):
#     """
#     Корректировка баллов на основе количества вопросов.
#     """
#     adjusted_scores = {}

#     print("🔧 Корректируем баллы с учетом количества вопросов...")

#     for trait, score in scores.items():
#         M = len(trait_questions[trait])  # Изначальное количество вопросов
#         N = len([q for q in trait_questions[trait] if q["question_id"] in scores])  # Количество вопросов после сокращения
#         adjusted_score = score * M / N if N != 0 else score
#         adjusted_scores[trait] = adjusted_score
#         print(f"📊 Для характеристики '{trait}' баллы скорректированы: {adjusted_score:.2f}")

#     return adjusted_scores


# def limit_score_range(scores, min_score, max_score):
#     """
#     Ограничиваем баллы, если они выходят за пределы шкалы.
#     """
#     limited_scores = {}

#     print("⚖️ Ограничиваем баллы, если они выходят за рамки шкалы...")

#     for trait, score in scores.items():
#         limited_score = min(max(score, min_score), max_score)
#         limited_scores[trait] = limited_score
#         print(f"✅ Для характеристики '{trait}' ограничены баллы: {limited_score:.2f}")

#     return limited_scores


# def interpret_scores(scores, scales):
#     """
#     Соотносим полученные баллы с интерпретационными шкалами.
#     """
#     interpretations = {}

#     print("🔍 Соотносим баллы с интерпретационными шкалами...")

#     for trait, score in scores.items():
#         scale = scales.get(trait, {})
#         if scale:
#             min_score = scale.get("min_score", 0)
#             max_score = scale.get("max_score", 100)
#             interpretation = f"Баллы для '{trait}': {score:.2f}. В интервале: [{min_score}, {max_score}]"
#         else:
#             interpretation = f"Интерпретация для характеристики '{trait}' не найдена."

#         interpretations[trait] = interpretation
#         print(f"📋 {interpretation}")

#     return interpretations

# def determine_dominant_trait(scores, trait_pairs):
#     """
#     Определение доминирующей черты в случае, когда тест содержит пару характеристик (например, 'Оптимизм' vs 'Пессимизм').
#     """
#     dominant_traits = {}

#     for pair in trait_pairs:
#         # Сравниваем баллы для каждой пары характеристик
#         trait_1, trait_2 = pair
#         score_1 = scores.get(trait_1, 0)
#         score_2 = scores.get(trait_2, 0)
#         # Определяем доминирующую черту
#         if score_1 > score_2:
#             dominant_traits[trait_1] = "Доминирует"
#             dominant_traits[trait_2] = "Не доминирует"
#         elif score_2 > score_1:
#             dominant_traits[trait_2] = "Доминирует"
#             dominant_traits[trait_1] = "Не доминирует"
#         else:
#             # В случае равенства можно оставить оба значения как "Не доминирует"
#             dominant_traits[trait_1] = "Не доминирует"
#             dominant_traits[trait_2] = "Не доминирует"

#     return dominant_traits

# def filter_dominant_traits(all_scores):
#     """
#     Фильтруем только доминирующие черты из всех баллов.
#     """
#     dominant_traits = {trait: status for trait, status in all_scores.items() if status == "Доминирует"}

#     return dominant_traits


# def process_other_tests(tests, responses):
#     print("🛠️ Обработка остальных тестов...")
#     # Исключаем темперамент и репрезентативную систему личности
#     excluded_traits = {"Сангвиник", "Холерик", "Меланхолик", "Флегматик", "Визуал", "Аудитив", "Кинестетик"}

#     filtered_tests = {test_id: test_data for test_id, test_data in tests.items() if
#                       test_id not in ["temperament_test", "representative_system_test"]}

#     # Группировка вопросов по характеристикам
#     trait_questions = group_questions_by_trait(filtered_tests)

#     # Фильтруем ненужные характеристики
#     trait_questions = {trait: questions for trait, questions in trait_questions.items() if trait not in excluded_traits}

#     # Подсчет баллов для оставшихся характеристик
#     scores = process_user_responses(filtered_tests, trait_questions, responses)

#     # Определение доминирующих черт для парных характеристик (например, Оптимизм vs Пессимизм)
#     trait_pairs = [
#         ("Интроверсия","Экстраверсия"),
#          ("Устойчивость","Возбудимость"),
#         ("Активность", "Пассивность"),
#         ("Ригидность", "Гибкость"),
#         ("Быстрая реакция", "Медленная реакция")
#     ]
#     dominant_traits = determine_dominant_trait(scores, trait_pairs)
#     # Корректировка баллов и ограничение диапазона значений
#     adjusted_scores = adjust_scores_for_number_of_questions(scores, trait_questions)
#     limited_scores = limit_score_range(adjusted_scores, min_score=0, max_score=100)

#     # Интерпретация баллов
#     updated_tests = adjust_scale_values(filtered_tests)
#     interpretations = interpret_scores(limited_scores, updated_tests)
#     only_dominant_traits = [x for x in dominant_traits if dominant_traits[x] == "Доминирует"]

#     return {
#         "scores": limited_scores,
#         # "interpretations": interpretations,
#         "dominant_traits": only_dominant_traits
#     }








#!#$!@$!#$!#$!#$!#$!#$!#$!#$!#$!#$!#$!#$!#$!#$#!#$#$#!$!#!##$!$
# from .adjust_scales import adjust_scale_values

# def group_questions_by_trait(tests):
#     """
#     Группировка вопросов по психологическим характеристикам.
#     """
#     trait_questions = {}

#     print("🔍 Группируем вопросы по психологическим характеристикам...")

#     for test in tests:
#         for question in test.questions.all():  # Вместо test["questions"]
#             for trait in question.get_traits():  # Используем get_traits()
#                 if trait not in trait_questions:
#                     trait_questions[trait] = []
#                 trait_questions[trait].append(question)

#     print(f"📝 Группировано {len(trait_questions)} характеристик.")
#     return trait_questions

# from core.models import AnswerWeight 

# def process_user_responses(tests, trait_questions, responses):
#     """
#     Обрабатывает ответы пользователя и подсчитывает баллы по характеристикам.
#     """
#     print(f"responses: {responses}")

#     print("📊 Подсчет баллов по характеристикам...")
#     scores = {trait: 0 for trait in trait_questions}

#     for trait, questions in trait_questions.items():
#         for question in questions:
#             print(f"\n🟨 Обрабатывается вопрос {question.id} (тема: {trait})")
#             # ID ответа приходит как строка — приводим к int
#             user_answer_id = responses.get(str(question.id)) or responses.get(question.id)
#             print(f"🔹 ID ответа пользователя: {user_answer_id}")

#             if user_answer_id:
#                 for answer in question.answers.all():
#                     print(f"🔸 Проверка: {answer.answer_text} (ID: {answer.id})")
#                     if str(answer.id) == str(user_answer_id):  # Сравнение по ID
#                         print(f"✅ Найден совпадающий ответ: {answer.answer_text}")
#                         try:
#                             weight = AnswerWeight.objects.get(answer=answer, trait__name=trait).weight
#                         except AnswerWeight.DoesNotExist:
#                             print(f"⚠️ Нет веса для ответа {answer.id} и черты {trait}")
#                             weight = 0
#                         scores[trait] += weight
#                         break

#     print(f"📈 Результаты: {scores}")
#     return scores

# def adjust_scores_for_number_of_questions(scores, trait_questions):
#     """
#     Корректирует баллы с учетом количества вопросов.
#     """
#     print("🔧 Корректировка баллов по количеству вопросов...")
#     adjusted = {}

#     for trait, raw_score in scores.items():
#         total_q = len(trait_questions[trait])
#         answered_q = sum(1 for q in trait_questions[trait] if q.id in scores)  # Используем q.id вместо q["question_id"]
#         adjusted[trait] = raw_score * total_q / answered_q if answered_q else raw_score
#         print(f"📊 '{trait}': скорректировано до {adjusted[trait]:.2f}")

#     return adjusted



# def limit_score_range(scores, min_score=0, max_score=100):
#     """
#     Ограничивает значения баллов в пределах заданной шкалы.
#     """
#     print("⚖️ Ограничение баллов по шкале...")
#     return {
#         trait: max(min(score, max_score), min_score)
#         for trait, score in scores.items()
#     }


# def interpret_scores(scores, tests):
#     """
#     Интерпретирует баллы на основе заданных шкал.
#     """
#     print("🔍 Интерпретация результатов...")
#     interpretations = {}

#     # Получаем шкалы из тестов
#     scales = []
#     for test in tests:
#         scales.extend(test.scales.all())  # Получаем все шкалы, связанные с тестом

#     for trait, score in scores.items():
#         # Ищем шкалу по имени характеристики (trait)
#         scale = next((s for s in scales if s.trait == trait), None)

#         if scale:
#             min_s, max_s = scale.min_score, scale.max_score  # Получаем min и max для шкалы
#             result = f"'{trait}': {score:.2f} (шкала: {min_s}-{max_s})"
#         else:
#             result = f"Нет интерпретации для '{trait}'"
#         interpretations[trait] = result
#         print(f"📋 {result}")

#     return interpretations



# def determine_dominant_trait(scores, trait_pairs):
#     """
#     Определяет доминирующую черту в каждой паре противоположных характеристик.
#     """
#     dominant = {}
#     for trait1, trait2 in trait_pairs:
#         s1, s2 = scores.get(trait1, 0), scores.get(trait2, 0)
#         if s1 > s2:
#             dominant[trait1], dominant[trait2] = "Доминирует", "Не доминирует"
#         elif s2 > s1:
#             dominant[trait2], dominant[trait1] = "Доминирует", "Не доминирует"
#         else:
#             dominant[trait1] = dominant[trait2] = "Не доминирует"
#     return dominant


# def filter_dominant_traits(all_traits):
#     """
#     Возвращает только доминирующие черты.
#     """
#     return [trait for trait, status in all_traits.items() if status == "Доминирует"]


# def process_other_tests(tests, responses):
#     """
#     Обрабатывает все тесты, кроме темперамента и представлений.
#     """
#     print("🛠️ Обработка дополнительных тестов...")
#     try:
#         excluded_traits = {"Сангвиник", "Холерик", "Меланхолик", "Флегматик", "Визуал", "Аудитив", "Кинестетик"}
#         excluded_test_ids = {"temperament_test", "representative_system_test"}

#         filtered_tests = [t for t in tests if t.id not in excluded_test_ids] 
#         trait_questions = group_questions_by_trait(filtered_tests)
#         trait_questions = {trait: q for trait, q in trait_questions.items() if trait not in excluded_traits}

#         scores = process_user_responses(filtered_tests, trait_questions, responses)

#         trait_pairs = [
#             ("Интроверсия", "Экстраверсия"),
#             ("Устойчивость", "Возбудимость"),
#             ("Активность", "Пассивность"),
#             ("Ригидность", "Гибкость"),
#             ("Быстрая реакция", "Медленная реакция")
#         ]
#         dominant_traits = determine_dominant_trait(scores, trait_pairs)
#         print(f"dominant_traits: {dominant_traits}")
#         only_dominant = filter_dominant_traits(dominant_traits)
#         print(f"only_dominant_traits: {only_dominant}")


#         adjusted = adjust_scores_for_number_of_questions(scores, trait_questions)
#         limited = limit_score_range(adjusted)
#         # interpreted_scales = interpret_scores(limited, adjust_scale_values(filtered_tests))

#         return {
#             "scores": limited,
#             # "interpretations": interpreted_scales,
#             "dominant_traits": only_dominant
#         }
#     except Exception as e:
#         print(e)
#         return 


from .adjust_scales import adjust_scale_values
from core.models import AnswerWeight

def group_questions_by_trait(tests):
    """
    Группировка вопросов по психологическим характеристикам.
    """
    trait_questions = {}

    print("🔍 Группируем вопросы по психологическим характеристикам...")

    for test in tests:
        for question in test.questions.all():
            for trait in question.get_traits():
                trait_name = trait.name.strip()  # Нормализуем имя
                if trait_name not in trait_questions:
                    trait_questions[trait_name] = []
                trait_questions[trait_name].append(question)

    print(f"📝 Группировано {len(trait_questions)} характеристик.")
    return trait_questions


def process_user_responses(tests, trait_questions, responses):
    """
    Обрабатывает ответы пользователя и подсчитывает баллы по характеристикам.
    """
    print(f"responses: {responses}")
    print("📊 Подсчет баллов по характеристикам...")

    scores = {trait: 0 for trait in trait_questions}

    for trait, questions in trait_questions.items():
        for question in questions:
            print(f"\n🟨 Обрабатывается вопрос {question.id} (тема: {trait})")
            user_answer_id = responses.get(str(question.id)) or responses.get(question.id)
            print(f"🔹 ID ответа пользователя: {user_answer_id}")

            if user_answer_id:
                for answer in question.answers.all():
                    print(f"🔸 Проверка: {answer.answer_text} (ID: {answer.id})")
                    if str(answer.id) == str(user_answer_id):
                        print(f"✅ Найден совпадающий ответ: {answer.answer_text}")
                        try:
                            answer_weight = AnswerWeight.objects.get(answer=answer, trait__name=trait)
                            weight = answer_weight.weight
                            print(f"✅ Вес ответа {answer.id} для черты '{trait}': {weight}")
                        except AnswerWeight.DoesNotExist:
                            print(f"⚠️ Нет веса для ответа {answer.id} и черты '{trait}'")
                            weight = 0
                        scores[trait] += weight
                        break

    print(f"📈 Результаты: {scores}")
    return scores


def adjust_scores_for_number_of_questions(scores, trait_questions):
    """
    Корректирует баллы с учетом количества вопросов.
    """
    print("🔧 Корректировка баллов по количеству вопросов...")
    adjusted = {}

    for trait, raw_score in scores.items():
        total_q = len(trait_questions[trait])
        answered_q = sum(1 for q in trait_questions[trait] if str(q.id) in scores)
        adjusted[trait] = raw_score * total_q / answered_q if answered_q else raw_score
        print(f"📊 '{trait}': скорректировано до {adjusted[trait]:.2f}")

    return adjusted


def limit_score_range(scores, min_score=0, max_score=100):
    """
    Ограничивает значения баллов в пределах заданной шкалы.
    """
    print("⚖️ Ограничение баллов по шкале...")
    return {
        trait: max(min(score, max_score), min_score)
        for trait, score in scores.items()
    }


def interpret_scores(scores, tests):
    """
    Интерпретирует баллы на основе заданных шкал.
    """
    print("🔍 Интерпретация результатов...")
    interpretations = {}

    scales = []
    for test in tests:
        scales.extend(test.scales.all())

    for trait, score in scores.items():
        scale = next((s for s in scales if s.trait.name.strip() == trait), None)
        if scale:
            min_s, max_s = scale.min_score, scale.max_score
            result = f"'{trait}': {score:.2f} (шкала: {min_s}-{max_s})"
        else:
            result = f"Нет интерпретации для '{trait}'"
        interpretations[trait] = result
        print(f"📋 {result}")

    return interpretations


def determine_dominant_trait(scores, trait_pairs):
    """
    Определяет доминирующую черту в каждой паре противоположных характеристик.
    """
    print("📊 Определение доминирующих черт...")
    dominant = {}

    # Нормализуем имена черт
    scores = {k.strip(): v for k, v in scores.items()}
    trait_pairs = [(t1.strip(), t2.strip()) for t1, t2 in trait_pairs]

    for trait1, trait2 in trait_pairs:
        s1 = scores.get(trait1, 0)
        s2 = scores.get(trait2, 0)

        if s1 > s2:
            dominant[trait1], dominant[trait2] = "Доминирует", "Не доминирует"
        elif s2 > s1:
            dominant[trait2], dominant[trait1] = "Доминирует", "Не доминирует"
        else:
            dominant[trait1] = dominant[trait2] = "Не доминирует"

    return dominant


def filter_dominant_traits(all_traits):
    """
    Возвращает только доминирующие черты.
    """
    return [trait for trait, status in all_traits.items() if status == "Доминирует"]


def process_other_tests(tests, responses):
    """
    Обрабатывает все тесты, кроме темперамента и представлений.
    """
    print("🛠️ Обработка дополнительных тестов...")

    try:
        excluded_traits = {"Сангвиник", "Холерик", "Меланхолик", "Флегматик", "Визуал", "Аудиал", "Кинестетик"}
        excluded_test_ids = {"temperament_test", "representative_system_test"}

        filtered_tests = [t for t in tests if t.id not in excluded_test_ids]
        trait_questions = group_questions_by_trait(filtered_tests)

        # Убираем исключенные черты
        trait_questions = {
            trait: qs for trait, qs in trait_questions.items()
            if trait.strip() not in excluded_traits
        }

        scores = process_user_responses(filtered_tests, trait_questions, responses)

        print("📊 ИТОГОВЫЕ БАЛЛЫ:")
        for trait, score in scores.items():
            print(f"{trait}: {score}")

        trait_pairs = [
            ("Интроверсия", "Экстраверсия"),
            ("Устойчивость", "Возбудимость"),
            ("Активность", "Пассивность"),
            ("Ригидность", "Гибкость"),
            ("Быстрая реакция", "Медленная реакция")
        ]
        dominant_traits = determine_dominant_trait(scores, trait_pairs)
        print(f"dominant_traits: {dominant_traits}")

        only_dominant = filter_dominant_traits(dominant_traits)
        print(f"only_dominant_traits: {only_dominant}")

        adjusted = adjust_scores_for_number_of_questions(scores, trait_questions)
        limited = limit_score_range(adjusted)

        # Можно раскомментировать, если хочешь выводить интерпретации
        # interpreted_scales = interpret_scores(limited, adjust_scale_values(filtered_tests))

        return {
            "scores": limited,
            # "interpretations": interpreted_scales,
            "dominant_traits": only_dominant
        }

    except Exception as e:
        print(f"❌ Ошибка при обработке тестов: {e}")
        return
