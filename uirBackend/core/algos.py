import random

def genetic_algorithm(characteristics_list, population_size=100, generations=500):
    population = generate_initial_population(population_size, characteristics_list)
    
    for generation in range(generations):
        # Оценка приспособленности
        fitness_scores = [evaluate_fitness(test, characteristics_list) for test in population]
        
        # Отбор лучших тестов
        selected_tests = select_best_tests(population, fitness_scores)
        
        # Создание нового поколения через скрещивание и мутацию
        next_generation = []
        while len(next_generation) < population_size:
            parent1, parent2 = select_parents(selected_tests)
            offspring = crossover(parent1, parent2)
            offspring = mutate(offspring)
            next_generation.append(offspring)
        
        population = next_generation
    
    # Возвращаем лучший тест
    best_test = max(population, key=lambda test: evaluate_fitness(test, characteristics_list))
    return best_test

def generate_initial_population(size, characteristics_list):
    # Генерация начальной популяции (случайные комбинации вопросов)
    return [generate_random_test(characteristics_list) for _ in range(size)]

def generate_random_test(characteristics_list):
    # Генерация случайного теста
    test = set()  # Сет вопросов
    for characteristic in characteristics_list:
        questions = get_questions_for_characteristic(characteristic)
        selected_questions = random.sample(questions, k=random.randint(1, len(questions)))
        test.update(selected_questions)
    return test

def evaluate_fitness(test, characteristics_list):
    # Оценка теста по точности и эффективности
    accuracy = calculate_accuracy(test, characteristics_list)
    efficiency = len(test)  # Количество вопросов
    return accuracy / efficiency  # Чем больше точность и меньше вопросы, тем лучше

def calculate_accuracy(test, characteristics_list):
    total_accuracy = 0
    total_weight = 0
    for characteristic in characteristics_list:
        characteristic_accuracy = 0
        characteristic_weight = 0
        for question in test:
            weight = get_weight(question, characteristic)
            characteristic_accuracy += weight
            characteristic_weight += weight
        
        if characteristic_weight > 0:
            # Нормируем точность по характеру на вес
            total_accuracy += characteristic_accuracy / characteristic_weight
            total_weight += 1
    
    return total_accuracy / total_weight if total_weight > 0 else 0

def get_weight(question, characteristic):
    # Возвращаем вес для характеристики и вопроса
    answer_weights = AnswerWeight.objects.filter(question=question, trait=characteristic)
    return sum([answer_weight.weight for answer_weight in answer_weights])

def crossover(parent1, parent2):
    # Скрещивание двух родителей
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(test):
    # Мутация — случайное изменение вопроса
    mutation_point = random.randint(0, len(test) - 1)
    test[mutation_point] = random.choice(get_all_possible_questions())
    return test

def select_best_tests(population, fitness_scores):
    # Отбор лучших тестов
    return sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)[:len(population)//2]

def select_parents(selected_tests):
    # Селекция родителей
    return random.sample(selected_tests, 2)
