from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import extraFunctions
from modulsKivy import LinkWidget


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create the BoxLayout and add it to the screen
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        home_widget_1 = LinkWidget(extraFunctions.reverse_string('זרעים'))
        home_widget_1.button.bind(on_press=lambda x: self.on_press())
        self.zraim = home_widget_1

        home_widget_2 = LinkWidget(extraFunctions.reverse_string('מועד'))
        home_widget_2.button.bind(on_press=lambda x: self.on_press())
        self.moed = home_widget_2

        home_widget_3 = LinkWidget(extraFunctions.reverse_string('נשים'))
        home_widget_3.button.bind(on_press=lambda x: self.on_press())
        self.nashim = home_widget_3

        home_widget_4 = LinkWidget(extraFunctions.reverse_string('נזיקין'))
        home_widget_4.button.bind(on_press=lambda x: self.on_press())
        self.nezikin = home_widget_4

        home_widget_5 = LinkWidget(extraFunctions.reverse_string('קודשים'))
        home_widget_5.button.bind(on_press=lambda x: self.on_press())
        self.kodashim = home_widget_5

        home_widget_6 = LinkWidget(extraFunctions.reverse_string('טהרות'))
        home_widget_6.button.bind(on_press=lambda x: self.on_press())
        self.taharot = home_widget_6

        self.layout.add_widget(self.zraim)
        self.layout.add_widget(self.moed)
        self.layout.add_widget(self.nashim)
        self.layout.add_widget(self.nezikin)
        self.layout.add_widget(self.kodashim)
        self.layout.add_widget(self.taharot)

    def on_press(self):
        self.manager.current = 'about'


class AboutScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        about_widget = LinkWidget("Go To Home")
        about_widget.button.bind(on_press=lambda x: self.on_press())

        self.add_widget(about_widget)

    def on_press(self):
        self.manager.current = 'home'
