from enum import Enum
import random

class Answer(Enum):
    CORRECT = 1
    FIRST_CORRECT = 2
    SECOND_CORRECT = 3
    INCORRECT = 4

class Plant:
    def __init__(self, name: str, images: list[str] ):
        self.name = name
        self.images = images
        self.answers: list[Answer] = []

    def to_dict(self):
        return {
            "name": self.name,
            "images": self.images,
            "answers": [a.name for a in self.answers]
        }
    def add_answer(self, answer: Answer):
        self.answers.append(answer)

    @staticmethod
    def from_dict(data: dict):
        plant = Plant(data["name"], data["images"])
        plant.answers = [Answer[a] for a in data.get("answers", [])]
        return plant

    def pick_random_images(self):
        return random.sample(self.images, min(4, len(self.images)))
