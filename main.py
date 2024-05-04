from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import mysql.connector
from kivy.core.window import Window

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="calorie"
)
db_cursor = db_connection.cursor()

# Create table if not exists
db_cursor.execute("CREATE TABLE IF NOT EXISTS food (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), calorie INT)")


class MainScreen(Screen):
    def on_enter(self):
        self.update_total_calories()
        self.update_food_list()

    def update_food_list(self):
        db_cursor.execute("SELECT name, calorie FROM food")
        food_items = db_cursor.fetchall()
        food_list_text = "[b]Name[/b] [b]Calorie[/b]\n"
        for food in food_items:
            food_list_text += f"{food[0]} - {food[1]} calories\n"
        self.ids.food_list.text = food_list_text

    def update_total_calories(self):
        db_cursor.execute("SELECT SUM(calorie) FROM food")
        total_calories = db_cursor.fetchone()[0]
        if total_calories:
            self.ids.total_calories.text = f"Total Calorie intake for today: {total_calories}"
        else:
            self.ids.total_calories.text = "Total Calories: 0"

    def add_food(self):
        food_name = self.ids.food_name.text
        calorie = self.ids.calorie.text

        if food_name and calorie:
            db_cursor.execute("INSERT INTO food (name, calorie) VALUES (%s, %s)", (food_name, calorie))
            db_connection.commit()
            self.ids.status.text = "Food added successfully."
            self.ids.food_name.text = ""
            self.ids.calorie.text = ""
            self.update_total_calories()
            self.update_food_list()
        else:
            self.ids.status.text = "Please enter both food name and calorie."



        
class MyFitnessPal(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("keyV.kv")


if __name__ == "__main__":
    Window.size = (368, 640)
    MyFitnessPal().run()
