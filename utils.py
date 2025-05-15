import random

from screeninfo import get_monitors

from plant import Plant, Answer
import re

class AnswerChecker:
    @staticmethod
    def checkAnswer(answer: str, plant: Plant):
        genus, species = plant.name.lower().split(" ", 1)
        if " " not in answer:
            if answer == genus:
                return Answer.FIRST_CORRECT
            elif answer == species:
                return Answer.SECOND_CORRECT
            return Answer.INCORRECT

        answered_genus, answered_species = answer.lower().split(" ", 1)
        answered_genus = re.sub(r"\s+", "", answered_genus)
        answered_species = re.sub(r"\s+", "", answered_species)
        genus = re.sub(r"\s+", "", genus)
        species = re.sub(r"\s+", "", species)

        if answered_genus == genus and answered_species == species:
            return Answer.CORRECT
        elif answered_genus == genus:
            return Answer.FIRST_CORRECT
        elif answered_species == species:
            return Answer.SECOND_CORRECT
        return Answer.INCORRECT


class PlantProvider:
    def __init__(self):
        self.plant_list = []
        self.current_plant = None

    def get_plants(self):
        return self.plant_list

    def get_current_plant(self):
        return self.current_plant

    def write_new_plants(self, new_plants):
        self.plant_list = new_plants


    def choose_new_plant(self):
        self.current_plant = random.choice(self.plant_list)


# Find main screen resolution
def find_screen_native():
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor.width, monitor.height
    return 1920, 1080