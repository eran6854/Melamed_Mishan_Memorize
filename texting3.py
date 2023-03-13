from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class MyTextInput(TextInput):
    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
        self.bind(texture_size=self.setter('size'))


class MyBoxLayout(BoxLayout):
    text_input = ObjectProperty()

    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20

        self.text_input = MyTextInput(hint_text='Type here...')
        self.add_widget(self.text_input)


class MyKivyApp(App):
    def build(self):
        box = MyBoxLayout()
        return box


if __name__ == '__main__':
    MyKivyApp().run()
