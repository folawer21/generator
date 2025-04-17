def calculate_conversion_coefficients(tests):
    """
    Вычисление коэффициентов пересчета для шкал в каждом тесте
    """
    print("🔄 Вычисляем коэффициенты пересчета для каждой шкалы...")

    conversion_coefficients = {}

    for test_id, test_data in tests.items():
        scales = test_data["scales"]
        original_question_count = test_data["original_question_count"]
        new_question_count = len(test_data["questions"])

        # Вычисляем коэффициенты пересчета для каждой шкалы
        for scale, scale_data in scales.items():
            original_max_score = scale_data["max_score"]
            coefficient = (new_question_count / original_question_count)
            conversion_coefficients[scale] = coefficient
            print(
                f"  ➡️ Для шкалы {scale}: K = ({new_question_count}/{original_question_count}) = {coefficient:.2f}")

    return conversion_coefficients


def adjust_scale_values(tests):
    """
    Корректировка максимальных значений шкал для каждого теста
    """
    print("\n🔧 Корректируем значения баллов для каждой шкалы...")
    conversion_coefficients = calculate_conversion_coefficients(tests)
    for test_id, test_data in tests.items():
        scales = test_data["scales"]

        for scale, scale_data in scales.items():
            # Получаем коэффициент пересчета для шкалы
            coefficient = conversion_coefficients.get(scale, 1)
            original_max_score = scale_data["max_score"]

            # Корректируем новые максимальные баллы
            adjusted_max_score = original_max_score * coefficient
            scale_data["adjusted_max_score"] = adjusted_max_score
            print(f"  ➡️ Шкала {scale} скорректирована. Новый максимум: {adjusted_max_score:.2f}")

    return tests