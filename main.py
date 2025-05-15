from business_logic import load_plants
from constants import JSON_FILE
from ui_layer import UIManager
from utils import PlantProvider





if __name__ == '__main__':

    plant_provider = PlantProvider()
    plant_provider.write_new_plants(load_plants(JSON_FILE))
    ui_manager = UIManager(plant_provider)

    ui_manager.get_root().mainloop()
