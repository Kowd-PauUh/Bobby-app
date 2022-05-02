from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, Property
from kivy.config import Config
from kivy.clock import Clock

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import sqlite3 as sl
from os.path import exists
