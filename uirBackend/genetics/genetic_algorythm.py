# import logging
# import random
# import numpy as np
# from .question_wrapper import QuestionWrapper

# logger = logging.getLogger(__name__)

# class GeneticTestGenerator:
#     def __init__(self, questions, num_generations=20, population_size=30, mutation_rate=0.1, lambda1=0.5, lambda2=0.3):
#         self.questions = questions  # список всех доступных вопросов (объекты)
#         self.num_generations = num_generations
#         self.population_size = population_size
#         self.mutation_rate = mutation_rate
#         self.lambda1 = lambda1
#         self.lambda2 = lambda2

#     def generate(self):
#         logger.info("🔄 Генерация начальной популяции")
#         population = self._initialize_population()

#         for generation in range(self.num_generations):
#             logger.info(f"📊 Поколение {generation + 1}")
#             fitness_scores = [self._fitness(chromosome) for chromosome in population]
#             logger.info(f"⚙️  Фитнес текущего поколения: {fitness_scores}")

#             selected = self._selection(population, fitness_scores)
#             logger.info("✅ Отбор завершен")

#             offspring = self._crossover(selected)
#             logger.info("🧬 Скрещивание завершено")

#             mutated = self._mutation(offspring)
#             logger.info("🎲 Мутация завершена")

#             population = mutated

#         best_chromosome = max(population, key=self._fitness)
#         logger.info("🏁 Алгоритм завершен. Лучшая хромосома найдена.")

#         return best_chromosome

#     def _initialize_population(self):
#         return [self._random_chromosome() for _ in range(self.population_size)]

#     def _random_chromosome(self):
#         return [random.choice([0, 1]) for _ in self.questions]

#     def _fitness(self, chromosome):
#         selected_questions = [self.questions[i] for i in range(len(chromosome)) if chromosome[i] == 1]

#         if not selected_questions:
#             return 0.0  # Пустой набор — нулевая пригодность

#         informativeness = self._calculate_informativeness(chromosome)
#         redundancy = self.calculate_redundancy(selected_questions)
#         balance_penalty = self._calculate_balance(chromosome)

#         fitness = informativeness - self.lambda1 * redundancy - self.lambda2 * balance_penalty
#         logger.info(f"Fitness: {fitness:.4f} = {informativeness:.4f} - "
#                      f"{self.lambda1:.2f}*{redundancy:.4f} - {self.lambda2:.2f}*{balance_penalty:.4f}")
#         return fitness

#     def _calculate_informativeness(self, chromosome):
#         return sum(
#             question.get_total_weight() for gene, question in zip(chromosome, self.questions) if gene
#         )

#     def calculate_redundancy(self, selected_questions):
#         """Считает сумму корреляций между всеми парами вопросов выше заданного порога."""
#         redundancy = 0.0
#         n = len(selected_questions)

#         for i in range(n):
#             for j in range(i + 1, n):
#                 corr = selected_questions[i].correlation_with(selected_questions[j])
#                 if corr > 0.5:  # Ты можешь изменить порог, если нужно
#                     redundancy += corr

#         logger.info(f"Redundancy penalty: {redundancy:.4f}")
#         return redundancy

#     def _calculate_balance(self, chromosome):
#         trait_count = {}
#         for gene, question in zip(chromosome, self.questions):
#             if gene:
#                 for trait in question.get_traits():  # метод возвращает список черт, которые выявляет вопрос
#                     trait_count[trait] = trait_count.get(trait, 0) + 1
#         if not trait_count:
#             return 999  # штраф за полную дисбалансировку
#         values = list(trait_count.values())
#         return np.std(values)

#     def _selection(self, population, fitness_scores):
#         sorted_pop = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
#         return sorted_pop[:self.population_size // 2]

#     def _crossover(self, selected):
#         next_generation = []
#         while len(next_generation) < self.population_size:
#             parent1, parent2 = random.sample(selected, 2)
#             split_point = random.randint(1, len(parent1) - 1)
#             child = parent1[:split_point] + parent2[split_point:]
#             next_generation.append(child)
#         return next_generation

#     def _mutation(self, population):
#         for chromosome in population:
#             if random.random() < self.mutation_rate:
#                 idx = random.randint(0, len(chromosome) - 1)
#                 chromosome[idx] = 1 - chromosome[idx]
#         return population
import logging
import random
import numpy as np
from .question_wrapper import QuestionWrapper

logger = logging.getLogger(__name__)

class GeneticTestGenerator:
    def __init__(self, questions, num_generations=20, population_size=30, mutation_rate=0.1, lambda1=0.5, lambda2=0.3):
        self.questions = questions
        self.num_generations = num_generations
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.lambda1 = lambda1
        self.lambda2 = lambda2

    def generate(self):
        logger.info("🔄 Генерация начальной популяции")
        population = self._initialize_population()
        logger.info(f"👶 Начальная популяция: {population}")

        for generation in range(self.num_generations):
            logger.info(f"📊 Поколение {generation + 1}")
            fitness_scores = [self._fitness(chromosome) for chromosome in population]
            logger.info(f"📈 Фитнес текущего поколения: {fitness_scores}")

            selected = self._selection(population, fitness_scores)
            logger.info(f"🏅 Отобранные хромосомы (топ-{len(selected)}): {selected}")

            offspring = self._crossover(selected)
            logger.info(f"🔀 Потомки после скрещивания: {offspring}")

            mutated = self._mutation(offspring)
            logger.info(f"🧬 Популяция после мутаций: {mutated}")

            population = mutated

        best_chromosome = max(population, key=self._fitness)
        logger.info("🏁 Алгоритм завершен. Лучшая хромосома найдена.")
        logger.info(f"🌟 Лучшая хромосома: {best_chromosome}")

        return best_chromosome

    def _initialize_population(self):
        return [self._random_chromosome() for _ in range(self.population_size)]

    def _random_chromosome(self):
        chromosome = [random.choice([0, 1]) for _ in self.questions]
        logger.info(f"🧪 Сгенерирована хромосома: {chromosome}")
        return chromosome

    def _fitness(self, chromosome):
        selected_questions = [self.questions[i] for i in range(len(chromosome)) if chromosome[i] == 1]

        if not selected_questions:
            return 0.0

        informativeness = self._calculate_informativeness(chromosome)
        redundancy = self.calculate_redundancy(selected_questions)
        balance_penalty = self._calculate_balance(chromosome)

        fitness = informativeness - self.lambda1 * redundancy - self.lambda2 * balance_penalty
        logger.info(f"⚖️ Fitness: {fitness:.4f} = {informativeness:.4f} - "
                     f"{self.lambda1:.2f}*{redundancy:.4f} - {self.lambda2:.2f}*{balance_penalty:.4f}")
        return fitness

    def _calculate_informativeness(self, chromosome):
        return sum(
            question.get_total_weight() for gene, question in zip(chromosome, self.questions) if gene
        )

    def calculate_redundancy(self, selected_questions):
        redundancy = 0.0
        n = len(selected_questions)
        for i in range(n):
            for j in range(i + 1, n):
                corr = selected_questions[i].correlation_with(selected_questions[j])
                if corr > 0.5:
                    redundancy += corr
        logger.info(f"🌀 Redundancy penalty: {redundancy:.4f}")
        return redundancy

    def _calculate_balance(self, chromosome):
        trait_count = {}
        for gene, question in zip(chromosome, self.questions):
            if gene:
                for trait in question.get_traits():
                    trait_count[trait] = trait_count.get(trait, 0) + 1
        if not trait_count:
            return 999
        values = list(trait_count.values())
        std_dev = np.std(values)
        logger.info(f"📊 Std dev по характеристикам: {std_dev:.4f}, counts: {trait_count}")
        return std_dev

    def _selection(self, population, fitness_scores):
        sorted_pop = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
        return sorted_pop[:self.population_size // 2]

    def _crossover(self, selected):
        next_generation = []
        while len(next_generation) < self.population_size:
            parent1, parent2 = random.sample(selected, 2)
            split_point = random.randint(1, len(parent1) - 1)
            child = parent1[:split_point] + parent2[split_point:]
            logger.info(f"🤝 Скрещивание: {parent1} x {parent2} => {child}")
            next_generation.append(child)
        return next_generation

    def _mutation(self, population):
        for chromosome in population:
            if random.random() < self.mutation_rate:
                idx = random.randint(0, len(chromosome) - 1)
                old_gene = chromosome[idx]
                chromosome[idx] = 1 - chromosome[idx]
                logger.info(f"⚡ Мутация в хромосоме: индекс {idx}, {old_gene} → {chromosome[idx]}")
        return population
