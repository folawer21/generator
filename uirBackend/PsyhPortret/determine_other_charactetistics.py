from adjust_scales import adjust_scale_values
def group_questions_by_trait(tests):
    """
    Группировка вопросов по психологическим характеристикам.
    Обрабатываются только тесты, которые не исключены.
    """
    trait_questions = {}

    print("🔍 Группируем вопросы по психологическим характеристикам...")

    for test_id, test in tests.items():
        for question in test["questions"]:
            for trait in question["traits"]:
                if trait not in trait_questions:
                    trait_questions[trait] = []
                trait_questions[trait].append(question)

    print(f"📝 Группировано {len(trait_questions)} характеристик.")
    return trait_questions


def process_user_responses(tests, trait_questions, responses):
    """
    Обработка ответов пользователя и подсчет баллов для каждой характеристики.
    Обрабатываются только тесты, которые не исключены.
    """
    scores = {trait: 0 for trait in trait_questions}

    print("📊 Подсчитываем баллы для каждой характеристики...")

    for trait, questions in trait_questions.items():
        for question in questions:
            answer_data = responses.get(question["question_id"])
            if answer_data:
                answer_weight = next((a["weight"].get(trait, 0) for a in question["answers"] if a["answer"] == answer_data), 0)
                scores[trait] += answer_weight
                print(f"✅ Вопрос {question['question_id']}: ответ '{answer_data}', вес для {trait}: {answer_weight}")

    print(f"📈 Подсчитаны баллы: {scores}")
    return scores


def adjust_scores_for_number_of_questions(scores, trait_questions):
    """
    Корректировка баллов на основе количества вопросов.
    """
    adjusted_scores = {}

    print("🔧 Корректируем баллы с учетом количества вопросов...")

    for trait, score in scores.items():
        M = len(trait_questions[trait])  # Изначальное количество вопросов
        N = len([q for q in trait_questions[trait] if q["question_id"] in scores])  # Количество вопросов после сокращения
        adjusted_score = score * M / N if N != 0 else score
        adjusted_scores[trait] = adjusted_score
        print(f"📊 Для характеристики '{trait}' баллы скорректированы: {adjusted_score:.2f}")

    return adjusted_scores


def limit_score_range(scores, min_score, max_score):
    """
    Ограничиваем баллы, если они выходят за пределы шкалы.
    """
    limited_scores = {}

    print("⚖️ Ограничиваем баллы, если они выходят за рамки шкалы...")

    for trait, score in scores.items():
        limited_score = min(max(score, min_score), max_score)
        limited_scores[trait] = limited_score
        print(f"✅ Для характеристики '{trait}' ограничены баллы: {limited_score:.2f}")

    return limited_scores


def interpret_scores(scores, scales):
    """
    Соотносим полученные баллы с интерпретационными шкалами.
    """
    interpretations = {}

    print("🔍 Соотносим баллы с интерпретационными шкалами...")

    for trait, score in scores.items():
        scale = scales.get(trait, {})
        if scale:
            min_score = scale.get("min_score", 0)
            max_score = scale.get("max_score", 100)
            interpretation = f"Баллы для '{trait}': {score:.2f}. В интервале: [{min_score}, {max_score}]"
        else:
            interpretation = f"Интерпретация для характеристики '{trait}' не найдена."

        interpretations[trait] = interpretation
        print(f"📋 {interpretation}")

    return interpretations

def determine_dominant_trait(scores, trait_pairs):
    """
    Определение доминирующей черты в случае, когда тест содержит пару характеристик (например, 'Оптимизм' vs 'Пессимизм').
    """
    dominant_traits = {}

    for pair in trait_pairs:
        # Сравниваем баллы для каждой пары характеристик
        trait_1, trait_2 = pair
        score_1 = scores.get(trait_1, 0)
        score_2 = scores.get(trait_2, 0)
        # Определяем доминирующую черту
        if score_1 > score_2:
            dominant_traits[trait_1] = "Доминирует"
            dominant_traits[trait_2] = "Не доминирует"
        elif score_2 > score_1:
            dominant_traits[trait_2] = "Доминирует"
            dominant_traits[trait_1] = "Не доминирует"
        else:
            # В случае равенства можно оставить оба значения как "Не доминирует"
            dominant_traits[trait_1] = "Не доминирует"
            dominant_traits[trait_2] = "Не доминирует"

    return dominant_traits

def filter_dominant_traits(all_scores):
    """
    Фильтруем только доминирующие черты из всех баллов.
    """
    dominant_traits = {trait: status for trait, status in all_scores.items() if status == "Доминирует"}

    return dominant_traits


def process_other_tests(tests, responses):
    print("🛠️ Обработка остальных тестов...")
    # Исключаем темперамент и репрезентативную систему личности
    excluded_traits = {"Сангвиник", "Холерик", "Меланхолик", "Флегматик", "Визуал", "Аудитив", "Кинестетик"}

    filtered_tests = {test_id: test_data for test_id, test_data in tests.items() if
                      test_id not in ["temperament_test", "representative_system_test"]}

    # Группировка вопросов по характеристикам
    trait_questions = group_questions_by_trait(filtered_tests)

    # Фильтруем ненужные характеристики
    trait_questions = {trait: questions for trait, questions in trait_questions.items() if trait not in excluded_traits}

    # Подсчет баллов для оставшихся характеристик
    scores = process_user_responses(filtered_tests, trait_questions, responses)

    # Определение доминирующих черт для парных характеристик (например, Оптимизм vs Пессимизм)
    trait_pairs = [
        ("Интроверсия","Экстраверсия"),
         ("Устойчивость","Возбудимость"),
        ("Активность", "Пассивность"),
        ("Ригидность", "Гибкость"),
        ("Быстрая реакция", "Медленная реакция")
    ]
    dominant_traits = determine_dominant_trait(scores, trait_pairs)
    # Корректировка баллов и ограничение диапазона значений
    adjusted_scores = adjust_scores_for_number_of_questions(scores, trait_questions)
    limited_scores = limit_score_range(adjusted_scores, min_score=0, max_score=100)

    # Интерпретация баллов
    updated_tests = adjust_scale_values(filtered_tests)
    interpretations = interpret_scores(limited_scores, updated_tests)
    only_dominant_traits = [x for x in dominant_traits if dominant_traits[x] == "Доминирует"]

    return {
        "scores": limited_scores,
        # "interpretations": interpretations,
        "dominant_traits": only_dominant_traits
    }