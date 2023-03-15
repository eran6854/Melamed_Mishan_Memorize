from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import screens


class MyApp(App):
    def build(self):
        # init screen manager
        screen_manager = ScreenManager(transition=NoTransition())

        # Creating screens
        home_screen = screens.HomeScreen()
        about_screen = screens.AboutScreen()
        zeraim_screen = screens.ZeraimScreen()
        berakhot_screen = screens.BerakhotScreen()
        berakhot_perek_1_screen = screens.BerakhotPerek1Screen()

        # Adding screens
        screen_manager.add_widget(home_screen)
        screen_manager.add_widget(about_screen)
        screen_manager.add_widget(zeraim_screen)
        screen_manager.add_widget(berakhot_screen)
        screen_manager.add_widget(berakhot_perek_1_screen)

        return screen_manager


if __name__ == '__main__':
    MyApp().run()
