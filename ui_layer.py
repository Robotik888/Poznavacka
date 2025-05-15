import tkinter as tk
import os
from tkinter import ttk
from screeninfo import get_monitors
from PIL import Image, ImageTk


from business_logic import save_plant_objects, get_files
from constants import PICTURES_DIR
from plant import Plant, Answer
from utils import PlantProvider
from utils import AnswerChecker


class UIManager:

    @staticmethod
    def find_screen_native():
        # Find main screen resolution
        for monitor in get_monitors():
            if monitor.is_primary:
                return monitor.width, monitor.height
        return 1920, 1080

    def create_base_ui_structure(self):
        print("hello")


    def __init__(self, plant_provider: PlantProvider):

        self.images = []
        self.image_labels = []
        self.plant_provider = plant_provider

        width, height = UIManager.find_screen_native()
        size_divider = 2.7
        self.image_frame_width = width // size_divider
        self.image_frame_height = height // size_divider

        self.root = tk.Tk()
        self.root.iconbitmap("phyton_app_shrubs.ico")
        self.root.configure(bg="white")
        self.root.title("Poznavacka")
        self.root.geometry(str(width) + "x" + str(height))

        # 🧱 Kontejner pro vrstvení frame-ů
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Všechny frame-y musí mít stejný parent: `container`
        self.menu_frame = tk.Frame(container)
        self.quiz_frame = tk.Frame(container)
        self.summary_frame = tk.Frame(container)

        for frame in (self.menu_frame, self.quiz_frame, self.summary_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        ### -- MAIN PART-- ###
        buttons_frame = tk.Frame(self.menu_frame, bg="green")
        buttons_frame.pack(pady=80)
        quiz_button = tk.Button(buttons_frame, text="Start Quiz", bg="lightgreen", font=("Arial", 20),
                                command=lambda: self.fill_image_frame(), height=10, width=20)
        quiz_button.grid(row=0, column=1)

        # 🟩 Tlačítko
        load_button = tk.Button(buttons_frame, text="Load Plants", bg="light goldenrod", font=("Arial", 20),
                           command=lambda: get_files(self.plant_provider), height=10, width=20)
        load_button.grid(row=1, column=1)

        # 🟩 Tlačítko
        delete_button = tk.Button(buttons_frame, text="Show All", bg="lightcoral", font=("Arial", 20),
                                  command=self.show_plants,
                                  height=10, width=20)
        delete_button.grid(row=2, column=1)

        ### -- MAIN PART-- ###

        ### --QUIZ PART-- ###
        back_frame = tk.Frame(self.quiz_frame, bg="white")
        back_frame.pack()
        self.go_back_quiz_button = tk.Button(back_frame, text="Back to Menu", bg="light goldenrod",
                                        font=("Arial", 12),
                                        command=self.return_to_menu)
        self.go_back_quiz_button.pack()
        # 📦 Horní frame na obrázky
        self.image_frame = tk.Frame(self.quiz_frame, bg="PaleTurquoise1")
        self.image_frame.pack(pady=20)

        # 📦 Spodní frame na vstup a tlačítko
        bottom_frame = tk.Frame(self.quiz_frame, bg="white")
        bottom_frame.pack(pady=30)

        # 🔴 Textové pole (Entry)
        self.entry = tk.Entry(bottom_frame, width=30, font=("Arial", 14))
        self.entry.grid(row=0, column=0, padx=10)

        # 🟩 Tlačítko
        self.confirm_button = tk.Button(bottom_frame, text="Confirm", bg="lightgreen", font=("Arial", 12), command=self.evaluate_answer)
        self.confirm_button.grid(row=0, column=1, padx=10)

        # 🟩 Tlačítko
        self.next_button = tk.Button(bottom_frame, text="Next Plant", bg="PaleTurquoise1", font=("Arial", 12),
                                        command=self.fill_image_frame)
        self.next_button.grid(row=0, column=2, padx=10)

        self.label_correct = tk.Label(bottom_frame, text="", font=("Arial", 12), bg="white")
        self.label_correct.grid(row=0, column=3, padx=10)
        self.label_first_correct = tk.Label(bottom_frame, text="", font=("Arial", 12), bg="white")
        self.label_first_correct.grid(row=0, column=4, padx=10)
        self.label_second_correct = tk.Label(bottom_frame, text="", font=("Arial", 12), bg="white")
        self.label_second_correct.grid(row=0, column=5, padx=10)
        self.label_incorrect = tk.Label(bottom_frame, text="", font=("Arial", 12), bg="white")
        self.label_incorrect.grid(row=0, column=6, padx=10)


        self.label_result = tk.Label(bottom_frame, text="", font=("Arial", 14), bg="white")
        self.label_result.grid(row=1, column=0, padx=10)

        ### --QUIZ PART-- ###
        self.menu_frame.tkraise()
    def evaluate_answer(self):
        self.confirm_button.config(state="disabled")
        result = AnswerChecker.checkAnswer(self.entry.get(), self.plant_provider.current_plant)
        self.plant_provider.current_plant.add_answer(result)
        save_plant_objects(self.plant_provider.plant_list)
        if result == Answer.CORRECT:
            self.image_frame.config(bg="green")
        elif result == Answer.INCORRECT:
            self.image_frame.config(bg="red")
        else:
            self.image_frame.config(bg="orange")
        self.show_score()

    def show_score(self):
        self.label_result.config(text=self.plant_provider.current_plant.name)
        self.label_correct.config(text="Correct Answers: " + str(self.plant_provider.current_plant.answers.count(Answer.CORRECT)))
        self.label_first_correct.config(text="Correct Genus: " + str(self.plant_provider.current_plant.answers.count(Answer.FIRST_CORRECT)))
        self.label_second_correct.config(text="Correct Species: " + str(self.plant_provider.current_plant.answers.count(Answer.SECOND_CORRECT)))
        self.label_incorrect.config(text="Incorrect Answers: " + str(self.plant_provider.current_plant.answers.count(Answer.INCORRECT)))


    def get_image_size(self):
        return self.image_frame_width, self.image_frame_height

    def get_image_frame(self):
        return self.image_frame
    def get_root(self):
        return self.root

    def fill_image_frame(self):

        self.label_incorrect.config(text="")
        self.label_first_correct.config(text="")
        self.label_second_correct.config(text="")
        self.label_correct.config(text="")
        self.label_result.config(text="")

        self.confirm_button.config(state="normal")
        self.image_frame.config(bg="PaleTurquoise1")
        self.entry.delete(0, tk.END)
        self.quiz_frame.tkraise()
        self.plant_provider.choose_new_plant()
        image_paths = [os.path.join(PICTURES_DIR, path) for path in self.plant_provider.current_plant.pick_random_images()]
        print(image_paths)
        self.images = []
        self.image_labels = []
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        for i in range(len(image_paths)):
            # Načti a zmenši obrázek
            image = Image.open(image_paths[i])
            image_width, image_height = image.size
            image_ratio = image_width / image_height
            image_frame_width, image_frame_height = self.get_image_size()
            image = image.resize((int(image_frame_height * image_ratio), int(image_frame_height)))

            photo = ImageTk.PhotoImage(image)
            self.images.append(photo)  # uchovej referenci

            # Rámeček + label s obrázkem
            frame = tk.Frame(self.image_frame, width=image_frame_width, height=image_frame_height, bg="orange", bd=2,
                             relief="solid")
            frame.grid(row=i // 2, column=i % 2, padx=20, pady=20)

            label = tk.Label(frame, image=photo)
            label.pack()
            self.image_labels.append(label)

    def show_plants(self):

        self.go_back_button = tk.Button(self.summary_frame, text="Back to Menu", bg="light goldenrod", font=("Arial", 12),
                                        command=self.return_to_menu)
        self.go_back_button.pack()

        self.summary_frame.tkraise()
        self.tree = ttk.Treeview(self.summary_frame, columns=("name", "number of photos", "correct", "correct genus", "correct species", "incorrect"), show="headings")
        self.tree.pack(fill="both", expand=True)

        # Hlavičky sloupců
        self.tree.heading("name", text="Name")
        self.tree.heading("number of photos", text="Number of photos")
        self.tree.heading("correct", text="Correct")
        self.tree.heading("correct genus", text="Correct Genus")
        self.tree.heading("correct species", text="Correct Species")
        self.tree.heading("incorrect", text="Incorrect")

        # Naplnění tabulky
        for plant in self.plant_provider.plant_list:
            name = plant.name
            number_of_photos = len(plant.images)
            correct = plant.answers.count(Answer.CORRECT)
            correct_genus = plant.answers.count(Answer.FIRST_CORRECT)
            correct_species = plant.answers.count(Answer.SECOND_CORRECT)
            incorrect = plant.answers.count(Answer.INCORRECT)

            self.tree.insert("", "end", values=(name, number_of_photos, correct, correct_genus, correct_species, incorrect))
            self.tree.bind("<Delete>", self.delete_selected)

    def delete_selected(self, event=None):
        selected_items = self.tree.selection()

        for item_id in selected_items:
            values = self.tree.item(item_id, "values")
            plant_name = values[0]

            # Smazat z modelu

            self.plant_provider.plant_list = [p for p in self.plant_provider.plant_list if p.name != plant_name]
            save_plant_objects(self.plant_provider.plant_list)

            # Smazat z tabulky
            self.tree.delete(item_id)

    def return_to_menu(self):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        self.menu_frame.tkraise()
