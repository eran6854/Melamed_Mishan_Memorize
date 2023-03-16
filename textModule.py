from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


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
    def __init__(self, button_text: str, link, **kwargs):
        super().__init__(**kwargs)
        self.link = link

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
