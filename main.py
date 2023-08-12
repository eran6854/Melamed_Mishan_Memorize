from kivy.app import App
from extraModules import MainLayout


class MyApp(App):
    def build(self):
        # Set the title of the app
        self.title = 'EzMemorize'
        return MainLayout()


if __name__ == '__main__':
    MyApp().run()
