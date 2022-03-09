from email import message
from select import select
from sqlite3 import Cursor
from tkinter import Widget
from unicodedata import name
from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import TwoLineAvatarListItem, ImageLeftWidget
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.textfield import MDTextFieldRound
import mysql.connector
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

Window.size = 300, 600
Builder.load_file("main.kv")

class conn():
    def __init__(self, *args):
        try:
            self.query = args[0]
        except IndexError as e:
            print("Index error")
        self.cone = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Tucket$693",
            database = "Colab"
        )
        
    def con(self, **kwargs):
        c = self.cone.cursor()
        try:
            if self.query:
                c.execute(self.query)
                return c
            else:
                return False
        except AttributeError as e:
            print("AttributeError")

class MD3Card(MDCard, RoundedRectangularElevationBehavior):
    '''Implements a material design v3 card.'''

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()    


class Home(Screen):
    def on_enter(self):
        self.title = "Home"
        self.ids.groups.clear_widgets()
        s = "SELECT * FROM users"
        x= conn(s)
        r = x.con()
        if r != None:
            for i in r:
                smt = f"SELECT * FROM messages WHERE sender='{i[1]}'"
                db = conn(smt)
                result= db.con()
                for o in result:
                    message = o[2]
                sender = i[1]
                image = i[2]
                self.messeges(sender, message, image)
            
    def messeges(self, sender, message, image):
        my_item = TwoLineAvatarListItem(text= sender, secondary_text=message,on_press = self.clicked)
        my_item.add_widget(ImageLeftWidget(source=image,radius= (60, 60, 60, 60)))
        self.ids.groups.add_widget(my_item)

    def clicked(self, *args, **kwargs):
        MDApp.get_running_app().root.current = 'inner'
        App.get_running_app().title = args[0].text


class Inner(Screen):
    def __init__(self, *args, **kw):
        self.title = "Inner"
        self.messages = {}
        super().__init__(**kw)
    def on_pre_enter(self, *args):
        self.ids.iner.clear_widgets()
        return super().on_pre_enter(*args)
    def on_enter(self, *args):
        self.username= App.get_running_app().title
        smt = f"SELECT * FROM messages WHERE sender='{self.username}'"
        db = conn(smt)
        result= db.con()
        l = []
        for i in result:
            l.append(i[2])
        self.messages[self.username] = l
        self.fnt_color = 1, 0, 1, 1
        self.them= "Custom"
        for key in self.messages:
            if key in self.username:
                for i in self.messages[self.username]:
                    self.ids.iner.add_widget(MDLabel(
                        text=i,
                        halign="center"
                        ))
        return super().on_enter(*args)


class Chat(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)


class Login(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
    def on_enter(self, *args):
        return super().on_enter(*args)
    def logger(self):
        username= self.ids.user.text
        password= self.ids.password.text
        if username and password:
            if username == "Francis" and password == "Tucket":
                print("Loging In ...")
                MDApp.get_running_app().root.current = 'home'
            else:
                pass
    def clear(self):
        self.ids.user.text = ""
        self.ids.password.text = ""

class main(MDApp):
    def build(self):
        self.title = "Main"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "900"
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(Home(name="home"))
        self.sm.add_widget(Chat(name="chat"))
        self.sm.add_widget(Inner(name="inner"))
        self.sm.add_widget(Login(name="login"))
        return self.sm


main().run()