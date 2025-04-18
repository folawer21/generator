def calculate_conversion_coefficients(tests):
    """
    Вычисление коэффициентов пересчета для шкал в каждом тесте
    """
    print("🔄 Вычисляем коэффициенты пересчета для каждой шкалы...")

    conversion_coefficients = {}

    for test in tests:  # Перебираем объекты Test
        scales = test.scales.all()  # Получаем все шкалы для данного теста через .all()
        original_question_count = test.questions.count()  # Получаем количество вопросов через .count()
        new_question_count = test.questions.count()  # Можно также получить количество вопросов через .count()

        # Вычисляем коэффициенты пересчета для каждой шкалы
        for scale in scales:  # scales — это набор объектов, перебираем их напрямую
            original_max_score = scale.max_score  # Предполагаем, что у шкалы есть max_score
            coefficient = (new_question_count / original_question_count)
            conversion_coefficients[scale.trait] = coefficient  # Используем имя шкалы в качестве ключа
            print(
                f"  ➡️ Для шкалы {scale.trait}: K = ({new_question_count}/{original_question_count}) = {coefficient:.2f}")

    return conversion_coefficients


def adjust_scale_values(tests):
    """
    Корректировка максимальных значений шкал для каждого теста
    """
    print("\n🔧 Корректируем значения баллов для каждой шкалы...")
    conversion_coefficients = calculate_conversion_coefficients(tests)
    
    for test in tests:  # Перебираем объекты Test
        scales = test.scales.all()  # Получаем все шкалы для данного теста через .all()

        for scale in scales:  # scales — это набор объектов, перебираем их напрямую
            # Получаем коэффициент пересчета для шкалы
            coefficient = conversion_coefficients.get(scale.trait, 1)  # Используем имя шкалы в качестве ключа
            original_max_score = scale.max_score  # Предполагаем, что у шкалы есть max_score

            # Корректируем новые максимальные баллы
            adjusted_max_score = original_max_score * coefficient
            scale.adjusted_max_score = adjusted_max_score  # Корректируем max_score шкалы
            print(f"  ➡️ Шкала {scale.trait} скорректирована. Новый максимум: {adjusted_max_score:.2f}")

    return tests
