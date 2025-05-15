from data_manager import DataManager
from constants import JSON_FILE
from ui_layer import UIManager
from utils import PlantProvider

if __name__ == '__main__':

    plant_provider = PlantProvider()
    data_manager = DataManager()
    plant_provider.write_new_plants(data_manager.load_plants(JSON_FILE))
    ui_manager = UIManager(plant_provider, data_manager)

    ui_manager.get_root().mainloop()
