"""
basic popup app
"""


import kivy
kivy.require('2.0.0') # replace with your current kivy version if necessary
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20
        self.add_widget(Button(text='Open Popup', on_press=self.open_popup))

    def open_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        for i in range(1, 5):
            popup_layout.add_widget(Button(text=f'Button {i}'))
        popup = Popup(title='Popup Window', content=popup_layout, size_hint=(None, None), size=(400, 400))
        popup.open()


class MyApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
