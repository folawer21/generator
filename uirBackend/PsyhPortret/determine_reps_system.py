def get_rep_system_trait_questions(tests, responses):
    rep_system_traits = ["Визуал", "Аудиал", "Кинестетик"]
    rep_system_questions = {}

    print("🔍 Начинаем извлечение вопросов, касающихся репрезентативной системы личности...")

    for test_id, test in tests.items():
        for question in test["questions"]:
            relevant_traits = set(question["traits"]).intersection(set(rep_system_traits))
            if relevant_traits:
                answer = responses.get(question["question_id"])
                if answer:
                    rep_system_questions[question["question_id"]] = {
                        "question_text": question["text"],
                        "traits": relevant_traits,
                        "answer": answer
                    }
                    print(f"✅ Вопрос {question['question_id']} найден, относится к характеристикам: {', '.join(relevant_traits)}")

    print(f"📝 Извлечено {len(rep_system_questions)} вопросов для определения репрезентативной системы личности.")
    return rep_system_questions


def calculate_rep_system_scores(tests, rep_system_questions):
    scores = {trait: 0 for trait in ["Визуал", "Аудиал", "Кинестетик"]}

    print("📊 Начинаем подсчет баллов для каждого типа репрезентативной системы личности...")

    for question_id, question_data in rep_system_questions.items():
        for trait in question_data["traits"]:
            question = next(q for test in tests.values() for q in test["questions"] if q["question_id"] == question_id)
            answer_data = next(a for a in question["answers"] if a["answer"] == question_data["answer"])
            weight = answer_data["weight"].get(trait, 0)
            scores[trait] += weight
            print(f"✅ Вопрос {question_id}: ответ '{question_data['answer']}', вес для {trait}: {weight}")

    print(f"📈 Подсчитаны баллы: {scores}")
    return scores


def determine_dominant_rep_system(scores):
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    print("🔍 Определяем ведущую репрезентативную систему...")

    if sorted_scores[0][1] > sorted_scores[1][1]:
        dominant_system = sorted_scores[0][0]
        print(f"🏆 Ведущая репрезентативная система: {dominant_system}")
        return dominant_system
    elif sorted_scores[0][1] == sorted_scores[1][1]:
        mixed_system = f"{sorted_scores[0][0]}-{sorted_scores[1][0]}"
        print(f"⚖️ Смешанная репрезентативная система: {mixed_system}")
        return mixed_system
    else:
        print("❓ Неопределённая репрезентативная система.")
        return "Смешанная система (неопределённая)"


def process_rep_system_test(tests, responses):
    print("🛠️ Начинаем обработку теста на репрезентативную систему личности...")

    # Шаг 2.1 - Извлечение вопросов, которые касаются репрезентативной системы
    rep_system_questions = get_rep_system_trait_questions(tests, responses)

    # Шаг 2.2 - Подсчет баллов для каждого типа репрезентативной системы личности
    scores = calculate_rep_system_scores(tests, rep_system_questions)

    # Шаг 2.4 - Определение ведущей репрезентативной системы
    dominant_rep_system = determine_dominant_rep_system(scores)

    print(f"✅ Обработка теста завершена. Ведущая репрезентативная система: {dominant_rep_system}")

    return dominant_rep_system, scores, tests
