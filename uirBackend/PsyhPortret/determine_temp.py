def get_temp_trait_questions(tests, responses):
    temperament_traits = ["Сангвиник", "Холерик", "Флегматик", "Меланхолик"]
    temperament_questions = {}

    print("🔍 Начинаем извлечение вопросов, касающихся темперамента...")

    for test_id, test in tests.items():
        for question in test["questions"]:
            relevant_traits = set(question["traits"]).intersection(set(temperament_traits))
            if relevant_traits:
                answer = responses.get(question["question_id"])
                if answer:
                    temperament_questions[question["question_id"]] = {
                        "question_text": question["text"],
                        "traits": relevant_traits,
                        "answer": answer
                    }
                    print(f"✅ Вопрос {question['question_id']} найден, относится к характеристикам: {', '.join(relevant_traits)}")

    print(f"📝 Извлечено {len(temperament_questions)} вопросов для определения темперамента.")
    return temperament_questions


def calculate_temp_scores(tests, temperament_questions):
    scores = {trait: 0 for trait in ["Сангвиник", "Холерик", "Флегматик", "Меланхолик"]}

    print("📊 Начинаем подсчет баллов для каждого типа темперамента...")

    for question_id, question_data in temperament_questions.items():
        for trait in question_data["traits"]:
            question = next(q for test in tests.values() for q in test["questions"] if q["question_id"] == question_id)
            answer_data = next(a for a in question["answers"] if a["answer"] == question_data["answer"])
            weight = answer_data["weight"].get(trait, 0)
            scores[trait] += weight
            print(f"✅ Вопрос {question_id}: ответ '{question_data['answer']}', вес для {trait}: {weight}")

    print(f"📈 Подсчитаны баллы: {scores}")
    return scores


def determine_dominant_temp(scores):
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    print("🔍 Определяем доминирующий тип темперамента...")

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


def process_temp_test(tests, responses):
    print("🛠️ Начинаем обработку теста на темперамент...")

    # Шаг 1.1 - Извлечение вопросов, которые касаются темперамента
    temperament_questions = get_temp_trait_questions(tests, responses)

    # Шаг 1.2 - Подсчет баллов для каждого типа темперамента
    scores = calculate_temp_scores(tests, temperament_questions)

    # Шаг 1.4 - Определение доминирующего типа темперамента
    dominant_temp = determine_dominant_temp(scores)

    print(f"✅ Обработка теста завершена. Доминирующий тип темперамента: {dominant_temp}")

    return dominant_temp, scores, tests