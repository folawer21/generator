import random
from django.db.models import Sum
from itertools import combinations
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Получаем список всех вопросов по характеристикам
def get_questions_by_characteristics(characteristics_list):
    questions_by_trait = defaultdict(set)
    all_questions = set()

    for characteristic in characteristics_list:
        answer_weights = AnswerWeight.objects.filter(trait__name=characteristic)
        for answer_weight in answer_weights:
            question = answer_weight.question
            questions_by_trait[characteristic].add(question)
            all_questions.add(question)

    return questions_by_trait, all_questions


def question_correlation(q1, q2):
    """ Оценивает корреляцию (избыточность) двух вопросов на основе их характеристик """
    # Получаем характеристики и их веса для обоих вопросов
    traits_q1 = {aw.trait.name: aw.weight for aw in AnswerWeight.objects.filter(question=q1)}
    traits_q2 = {aw.trait.name: aw.weight for aw in AnswerWeight.objects.filter(question=q2)}

    # Все уникальные характеристики
    all_traits = set(traits_q1.keys()) | set(traits_q2.keys())

    # Формируем векторы весов (0 если характеристика не связана с вопросом)
    vector_q1 = np.array([traits_q1.get(trait, 0) for trait in all_traits])
    vector_q2 = np.array([traits_q2.get(trait, 0) for trait in all_traits])

    # Вычисляем косинусное сходство (от 0 до 1, где 1 - максимальная схожесть)
    if np.linalg.norm(vector_q1) == 0 or np.linalg.norm(vector_q2) == 0:
        return 0  # Если у вопроса нет характеристик, считаем их независимыми
    return cosine_similarity([vector_q1], [vector_q2])[0][0]


# Фитнес-функция оценивает, насколько тест хорош
def evaluate_fitness(test_questions, characteristics_list, questions_by_trait):
    total_score = 0
    covered_traits = defaultdict(int)

    # Оценка информативности
    for question in test_questions:
        for trait in characteristics_list:
            if question in questions_by_trait[trait]:
                covered_traits[trait] += 1

    # Проверяем, что все характеристики покрыты равномерно
    balance_penalty = sum(abs(len(test_questions) / len(characteristics_list) - count) for count in covered_traits.values())

    # Оценка избыточности (корреляция между вопросами)
    redundancy_penalty = sum(question_correlation(q1, q2) for q1, q2 in combinations(test_questions, 2))

    # Итоговый фитнес
    total_score = sum(covered_traits.values()) - (balance_penalty + redundancy_penalty)
    return total_score


# Генерация начальной популяции случайных тестов
def generate_initial_population(pop_size, characteristics_list, questions_by_trait):
    population = []
    for _ in range(pop_size):
        test = set()
        for trait in characteristics_list:
            if questions_by_trait[trait]:
                test.add(random.choice(list(questions_by_trait[trait])))
        population.append(test)
    return population


# Скрещивание: обмен вопросами между тестами
def crossover(parent1, parent2):
    split = len(parent1) // 2
    child = set(list(parent1)[:split] + list(parent2)[split:])
    return child


# Мутация: добавление или удаление случайного вопроса
def mutate(test_questions, all_questions):
    if random.random() < 0.5 and len(test_questions) > 1:
        test_questions.remove(random.choice(list(test_questions)))
    else:
        test_questions.add(random.choice(list(all_questions)))
    return test_questions


# Основной генетический алгоритм
def genetic_algorithm(characteristics_list, pop_size=50, generations=100):
    questions_by_trait, all_questions = get_questions_by_characteristics(characteristics_list)
    population = generate_initial_population(pop_size, characteristics_list, questions_by_trait)

    for generation in range(generations):
        fitness_scores = [(test, evaluate_fitness(test, characteristics_list, questions_by_trait)) for test in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)

        # Лучшие тесты сохраняем
        next_generation = [x[0] for x in fitness_scores[:pop_size // 2]]

        # Скрещивание
        while len(next_generation) < pop_size:
            parent1, parent2 = random.sample(next_generation, 2)
            child = crossover(parent1, parent2)
            child = mutate(child, all_questions)
            next_generation.append(child)

        population = next_generation

    # Возвращаем лучший найденный тест
    best_test = max(population, key=lambda test: evaluate_fitness(test, characteristics_list, questions_by_trait))
    return best_test
