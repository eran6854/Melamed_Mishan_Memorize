from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from extraFunctions import is_sub_str_from_start


class HebrewTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.is_reversed = False
        self.last_value = ""
        self.base_direction = "rtl"
        self.font_name = "Arial.ttf"
        self.halign = "right"

    def insert_text(self, substring, from_undo=False):
        # Override the default insert_text method to insert text at the beginning of the string
        substring = substring[::-1]  # Reverse the substring
        super().insert_text(substring, from_undo=from_undo)
        self.cursor = (0, self.cursor[1])  # Move the cursor to the beginning of the line after inserting text

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] == 8:  # backspace key
            self.text = self.text[1:]
            self.cursor = (0, self.cursor[1])
        else:
            super().keyboard_on_key_down(window, keycode, text, modifiers)


class LinkWidget(BoxLayout):
    def __init__(self, button_text: str, **kwargs):
        super().__init__(**kwargs)

        # Create the icon
        self.icon = Image(source='torah256.png', size_hint_x=0.015)
        self.add_widget(self.icon)

        # Create the label
        self.label = Label(text='0%', size_hint_x=0.015)
        self.add_widget(self.label)

        # Create the button
        self.button = Button(text=f'{button_text}',
                             size_hint_x=0.3,
                             background_color=(1, 0, 0, 1),
                             font_name="Arial.ttf",
                             )
        self.add_widget(self.button)

    def set_percentile(self, percentile: int):
        self.label.text = f'{percentile}%'

    def set_icon(self, value: bool, icon_1: str, icon_2: str):
        if value:
            self.icon.source = f'{icon_1}.png'
        else:
            self.icon.source = f'{icon_2}.png'


class FirstLetterGameHebrewTextInput(HebrewTextInput):
    def __init__(self, text, **kwargs):
        if len(text) == 0:
            raise Exception("text length is 0")
        super().__init__(**kwargs)
        self.hint_text = text[0]
        self.hint_text_color = get_color_from_hex('#0000FF')
        self.foreground_color = get_color_from_hex('#0000FF')
        self.target_text = text
        self.background_color = [0, 0, 0, 1]

    def on_text(self, instance, value):
        value = value[::-1]
        if not is_sub_str_from_start(value, self.target_text):
            self.text = self.target_text[::-1]
            self.lock(True)
        elif value == self.target_text:
            self.lock(False)

    def lock(self, is_fail: bool):
        self.readonly = True
        self.focus = False
        self.disabled = True
        self.background_disabled_normal = ""
        self.background_color = [0, 0, 0, 1]
        if is_fail:
            self.foreground_color = (1, 0, 0, 1)
            self.disabled_foreground_color = (1, 0, 0, 1)
        else:
            self.foreground_color = (0, 255, 0, 1)
            self.disabled_foreground_color = (0, 255, 0, 1)


class Mishna:
    def __init__(self, seder: str, masechet: str, perek: str, number: int, text: str):
        self.seder = seder
        self.masechet = masechet
        self.perek = perek
        self.number = number
        self.text = text
        self.test_1_grade = 0
        self.memorized = 0
