from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from database import Database
import subprocess
import os

class testApp(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Login(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        self.db = Database(host='localhost', user='root', password='', database='calorie')
        return testApp() 
    
    def validate_login(self):
        username = self.root.ids.Username.text
        password = self.root.ids.Password.text
        
        
        if self.db.check_user(username, password):
            subprocess.Popen(["python", "main.py"])
            os._exit(0)
        else:
            self.root.ids.error_label.text = "Invalid "

    def validate_signup(self):
        username = self.root.ids.Username.text
        password = self.root.ids.Password.text
       
        signup_successful = self.db.signup(username, password)
        if signup_successful:
            self.root.ids.error_label.text = "Success"
        else:
            self.root.ids.error_label.text = "Already exists"
        

if __name__ == "__main__":
    Window.size = (368, 640)
    Builder.load_file("login.kv")
    Login().run()
