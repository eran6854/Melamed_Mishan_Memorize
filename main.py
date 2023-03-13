from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from screens import HomeScreen, AboutScreen


class MyApp(App):
    def build(self):
        screen_manager = ScreenManager(transition=NoTransition())

        home_screen = HomeScreen(name='home')
        about_screen = AboutScreen(name='about')

        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(about_screen)

        return screen_manager


if __name__ == '__main__':
    MyApp().run()
