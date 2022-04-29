from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout  # размещение виджетов по сетке
from kivy.uix.stacklayout import StackLayout  # размещение виджетов сколько везет в строку
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

import sqlite3 as sl
from os.path import exists