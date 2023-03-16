from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Top rectangle
        self.add_widget(Label(text='Top Rectangle', size_hint=(1, 0.05)))

        # Scrollable area
        scroll_view = ScrollView(size_hint=(1, 0.9))
        grid_layout = GridLayout(cols=1, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for i in range(50):
            grid_layout.add_widget(Label(text=f'Text {i}', size_hint_y=None, height=40))

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

        # Bottom rectangle
        self.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))

    def get_window_size(self):
        return Window.width, Window.height * 0.6


class MyApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MyApp().run()
