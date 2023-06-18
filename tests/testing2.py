from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)


class MyApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')

        open_popup_button = Button(text='Open Popup')
        open_popup_button.bind(on_press=self.open_popup)
        main_layout.add_widget(open_popup_button)

        return main_layout

    def open_popup(self, *args):
        popup_layout = BoxLayout(orientation='vertical')

        button_box = BoxLayout(orientation='vertical')
        for i in range(1, 6):
            button = Button(text=f'Button {i}')
            if i == 5:
                button.bind(on_press=lambda x: popup.dismiss())
            button_box.add_widget(button)
        popup_layout.add_widget(button_box)

        popup = Popup(title='', content=popup_layout, size_hint=(None, None), size=(400, 400),
                      background='', border=(0, 0, 0, 0), separator_height=0)
        popup.open()


if __name__ == '__main__':
    MyApp().run()
