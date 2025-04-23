import numpy as np
class QuestionWrapper:
    def __init__(self, question):
        self.original = question
        self.trait_weights = self._get_trait_weights()

    def _get_trait_weights(self):
        return {
            aw.trait.name: aw.weight
            for aw in self.original.answerweight_set.all()
        }

    def get_total_weight(self):
        return sum(abs(w) for w in self.trait_weights.values())

    def get_traits(self):
        return list(self.trait_weights.keys())

    def correlation_with(self, other: 'QuestionWrapper') -> float:
        all_traits = set(self.trait_weights.keys()) | set(other.trait_weights.keys())
        vec1 = np.array([self.trait_weights.get(trait, 0.0) for trait in all_traits])
        vec2 = np.array([other.trait_weights.get(trait, 0.0) for trait in all_traits])
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return np.dot(vec1, vec2) / (norm1 * norm2)

    @property
    def text(self):
        return self.original.question_text  # если нужно .text — проксируй это поле

    def __str__(self):
        return self.text
