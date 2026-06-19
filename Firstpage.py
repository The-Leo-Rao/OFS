from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from main_data import *
from kivy.lang import Builder
from kivy.properties import StringProperty

import sqlite3
con = sqlite3.connect("os1.db")
myc = con.cursor()

Window.clearcolor = (1, 1, 1, 1)


class StartScreen(Screen):
    def check_username(self, instance, value):
        if len(value) < 5 or any(char.isdigit() for char in value):
            self.ids.error_usr.text = "Invalid Value! Minimum length-5. No numbers allowed."
        else:
            self.ids.error_usr.text = ""
            login['Name'] = self.ids.username_input.text

    def check_password(self, instance, value):
        if len(value) < 8:
            self.ids.error_passwrd.text = "Invalid Value! Minimum length-8."
        else:
            self.ids.error_passwrd.text = ""

    def final_pass(self):
        if self.ids.error_passwrd.text == "" and self.ids.error_usr.text == "":
            usrn = self.ids.username_input.text
            pswd = self.ids.password_input.text
            myc.execute('insert into logins values(%s,%s)', (usrn, pswd))
            con.commit()
            self.manager.current = 'next'
            self.clear_widgets()
        else:
            None


class NextScreen(Screen):
    def check_petname(self, instance, value):
        if any(char.isdigit() for char in value):
            self.ids.error_pet.text = "Invalid Name!"
        else:
            self.ids.error_pet.text = ""
            Pet_basic['Pname'] = self.ids.pname_input.text

    def spinner_selected(self, instance, value, value2):
        if value == 'Select' or value2 == 'Select':
            self.ids.error_spinner.text = 'Invalid selection'
        else:
            self.ids.error_spinner.text = ''
            Pet_basic['Age'] = self.ids.first_spin.text
            Pet_basic['Breed'] = self.ids.second_spin.text

    def next_pass(self):
        if self.ids.error_pet.text == "" and self.ids.error_spinner.text == "":
            pname = self.ids.pname_input.text
            pbreed = self.ids.second_spin.text
            page = self.ids.first_spin.text
            myc.execute('insert into pet_info values(%s,%s,%s)', (pname, page, pbreed))
            con.commit()
            self.manager.current = 'home'
            self.clear_widgets()
        else:
            None


class HomePage(Screen):
    def on_enter(self):
        self.ids.welcome_label.text = f"Welcome! {login.get('Name', '')}"
        self.ids.pet_name_label.text = f"Pet Name: {Pet_basic.get('Pname', '')}"
        self.ids.pet_age_label.text = f"Pet Age: {Pet_basic.get('Age', '')}"
        self.ids.pet_breed_label.text = f"Pet Breed: {Pet_basic.get('Breed', '')}"

    def info_pass(self):
        self.manager.current = 'info'

    def Settings_pass(self):
        self.manager.current = 'Settings'


class Getinfo(Screen):
    info_text = StringProperty('hi')

    def on_pre_enter(self):
        if Pet_basic.get('Breed', '') == 'Indie':
            self.info_text = f"since {Pet_basic.get('Pname', '')} is a {Pet_basic.get('Breed', '')}, {indie_data}"
        elif Pet_basic.get('Breed', '') == 'Golden retriever':
            self.info_text = f"since {Pet_basic.get('Pname', '')} is a {Pet_basic.get('Breed', '')}, {golden_data}"
        elif Pet_basic.get('Breed', '') == 'Labrador':
            self.info_text = f"since {Pet_basic.get('Pname', '')} is a {Pet_basic.get('Breed', '')}, {lab_data}"
        elif Pet_basic.get('Breed', '') == 'German shepheard':
            self.info_text = f"since {Pet_basic.get('Pname', '')} is a {Pet_basic.get('Breed', '')}, {german_data}"
        else:
            self.info_text = 'error'

    def on_plus_button_press(self):
        self.manager.current = 'home'


class Settings(Screen):
    def Change1_pass(self):
        self.manager.current = 'Change1'

    def on_plus_button_press_2(self):
        self.manager.current = 'home'

    def Change2_pass(self):
        self.manager.current = 'Change2'


class Change1(Screen):
    def check_changepassword(self, instance, value1):
        if len(value1) < 8:
            self.ids.error_passwrd0.text = "Invalid password. Minimum length is 8."
        else:
            self.ids.error_passwrd0.text = ""

    def check_verifypassword(self, instance, value2):
        if self.ids.verifypassword_input.text != self.ids.changepassword_input.text:
            self.ids.error_passwrd1.text = "Password doesn't match, Re-enter."
        else:
            self.ids.error_passwrd1.text = ""

    def Change1(self):
        if self.ids.error_passwrd0.text == "" and self.ids.error_passwrd1.text == "":
            self.manager.current = 'home'
        else:
            None


class Change2(Screen):
    def check_petname(self, instance, value):
        if any(char.isdigit() for char in value):
            self.ids.error_pet.text = "Invalid Name!"
        else:
            self.ids.error_pet.text = ""
            Pet_basic['Pname'] = self.ids.pname_input.text

    def spinner_selected(self, instance, value, value2):
        if value == 'Select' and value2 == 'Select':
            self.ids.error_spinner.text = '*'
        else:
            self.ids.error_spinner.text = ''
            Pet_basic['Age'] = self.ids.first_spin.text
            Pet_basic['Breed'] = self.ids.second_spin.text

    def Change2(self):
        self.manager.current = 'home'


class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(NextScreen(name="next"))
        sm.add_widget(HomePage(name="home"))
        sm.add_widget(Getinfo(name='info'))
        sm.add_widget(Settings(name='Settings'))
        sm.add_widget(Change1(name='Change1'))
        sm.add_widget(Change2(name='Change2'))
        return sm

    def on_plus_button_press(self):
        print('hi')


if __name__ == "__main__":
    MyApp().run()
