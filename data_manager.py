import json
import os
import shutil
from collections import defaultdict
from tkinter import filedialog
import re

from constants import PICTURES_DIR
from plant import Plant

class DataManager:

    def add_new_plants(self, plant_provider):
        new_filenames: list[str] = []
        os.makedirs(PICTURES_DIR, exist_ok=True)
        files = filedialog.askopenfilenames()
        for file in files:
            filename = os.path.basename(file)
            new_filenames.append(filename)
            shutil.copy2(file, os.path.join(PICTURES_DIR, filename))
        self.create_plant_objects(new_filenames, plant_provider)


    def create_plant_objects(self, new_files: list[str], plant_provider):
        current_plant_objects = plant_provider.plant_list
        groups = defaultdict(list)
        for filename in new_files:
            # take string up to the first parenthesis
            match = re.match(r"^(.*?)\s*\(", filename)
            if match:
                key = f"{match.group(1)}"
                groups[key].append(filename)
        plant_objects = []
        for key, group in groups.items():
            plant_objects.append(Plant(key, group))

        # assures that there are no duplicities
        existing_names = {plant.name for plant in current_plant_objects}
        for plant in plant_objects:
            if plant.name not in existing_names:
                current_plant_objects.append(plant)
                existing_names.add(plant.name)
        self.save_plant_objects(current_plant_objects)
        plant_provider.write_new_plants(current_plant_objects)

    @staticmethod
    def save_plant_objects(plants: list[Plant]):
        with open("plants.json", "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in plants], f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_plants(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Plant.from_dict(d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
