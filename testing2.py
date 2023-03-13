from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label


class MyFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MyFloatLayout, self).__init__(**kwargs)
        for i in range(10):
            label = Label(text=f"Label {i}", size_hint=(None, None),
                          size=(200, 50), pos=(i * 200, 0))
            self.add_widget(label)


class MyScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(MyScrollView, self).__init__(**kwargs)
        self.float_layout = MyFloatLayout(size_hint=(None, None), size=(20000, 50))
        self.add_widget(self.float_layout)


class MyApp(App):
    def build(self):
        return MyScrollView()


if __name__ == '__main__':
    MyApp().run()
