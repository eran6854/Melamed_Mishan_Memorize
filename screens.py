from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import extraFunctions
from modulsKivy import LinkWidget


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.name = 'home'

        # Create the BoxLayout and add it to the screen
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Creating widgets
        widget_1 = LinkWidget(extraFunctions.reverse_string('זרעים'))
        widget_1.button.bind(on_press=lambda x: self.on_press_zeraim())
        self.zeraim = widget_1

        widget_2 = LinkWidget(extraFunctions.reverse_string('מועד'))
        widget_2.button.bind(on_press=lambda x: self.on_press())
        self.moed = widget_2

        widget_3 = LinkWidget(extraFunctions.reverse_string('נשים'))
        widget_3.button.bind(on_press=lambda x: self.on_press())
        self.nashim = widget_3

        widget_4 = LinkWidget(extraFunctions.reverse_string('נזיקין'))
        widget_4.button.bind(on_press=lambda x: self.on_press())
        self.nezikin = widget_4

        widget_5 = LinkWidget(extraFunctions.reverse_string('קודשים'))
        widget_5.button.bind(on_press=lambda x: self.on_press())
        self.kodashim = widget_5

        widget_6 = LinkWidget(extraFunctions.reverse_string('טהרות'))
        widget_6.button.bind(on_press=lambda x: self.on_press())
        self.taharot = widget_6

        # Adding widgets to the layout
        self.layout.add_widget(self.zeraim)
        self.layout.add_widget(self.moed)
        self.layout.add_widget(self.nashim)
        self.layout.add_widget(self.nezikin)
        self.layout.add_widget(self.kodashim)
        self.layout.add_widget(self.taharot)

    def on_press(self):
        self.manager.current = 'about'

    def on_press_zeraim(self):
        self.manager.current = 'zeraim'

    def on_press_moed(self):
        self.manager.current = 'moed'

    def on_press_nashim(self):
        self.manager.current = 'nashim'

    def on_press_nezikin(self):
        self.manager.current = 'nezikin'

    def on_press_kodashim(self):
        self.manager.current = 'kodashim'

    def on_press_taharot(self):
        self.manager.current = 'taharot'


class ZeraimScreen(Screen):
    def __init__(self, **kwargs):
        super(ZeraimScreen, self).__init__(**kwargs)
        self.name = 'zeraim'

        # Create the BoxLayout and add it to the screen
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Creating widgets
        widget_1 = LinkWidget(extraFunctions.reverse_string('ברכות'))
        widget_1.button.bind(on_press=lambda x: self.on_press_berakhot())
        self.berakhot = widget_1

        widget_2 = LinkWidget(extraFunctions.reverse_string('פאה'))
        widget_2.button.bind(on_press=lambda x: self.on_press())
        self.peah = widget_2

        widget_3 = LinkWidget(extraFunctions.reverse_string('דמאי'))
        widget_3.button.bind(on_press=lambda x: self.on_press())
        self.demai = widget_3

        widget_4 = LinkWidget(extraFunctions.reverse_string('כלאיים'))
        widget_4.button.bind(on_press=lambda x: self.on_press())
        self.kilayim = widget_4

        widget_5 = LinkWidget(extraFunctions.reverse_string('שביעית'))
        widget_5.button.bind(on_press=lambda x: self.on_press())
        self.sheviit = widget_5

        widget_6 = LinkWidget(extraFunctions.reverse_string('תרומות'))
        widget_6.button.bind(on_press=lambda x: self.on_press())
        self.terumot = widget_6

        widget_7 = LinkWidget(extraFunctions.reverse_string('מעשרות'))
        widget_7.button.bind(on_press=lambda x: self.on_press())
        self.maaserot = widget_7

        widget_8 = LinkWidget(extraFunctions.reverse_string('מעשר שני'))
        widget_8.button.bind(on_press=lambda x: self.on_press())
        self.maaser_sheni = widget_8

        widget_9 = LinkWidget(extraFunctions.reverse_string('חלה'))
        widget_9.button.bind(on_press=lambda x: self.on_press())
        self.challah = widget_9

        widget_10 = LinkWidget(extraFunctions.reverse_string('ערלה'))
        widget_10.button.bind(on_press=lambda x: self.on_press())
        self.orlah = widget_10

        widget_11 = LinkWidget(extraFunctions.reverse_string('ביכורים'))
        widget_11.button.bind(on_press=lambda x: self.on_press())
        self.bikkurim = widget_11

        # Adding widgets to the layout
        self.sedarim = [self.berakhot, self.peah, self.demai, self.kilayim, self.sheviit,
                        self.terumot, self.maaserot, self.maaser_sheni, self.challah,
                        self.orlah, self.bikkurim]
        for seder in self.sedarim:
            self.layout.add_widget(seder)

    def on_press(self):
        self.manager.current = 'about'

    def on_press_berakhot(self):
        self.manager.current = 'berakhot'


class BerakhotScreen(Screen):
    def __init__(self, **kwargs):
        super(BerakhotScreen, self).__init__(**kwargs)
        self.name = 'berakhot'

        # Create the BoxLayout and add it to the screen
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Creating widgets
        widget_1 = LinkWidget(extraFunctions.reverse_string('פרק א'))
        widget_1.button.bind(on_press=lambda x: self.on_press_perek_1())
        self.perek_1 = widget_1

        widget_2 = LinkWidget(extraFunctions.reverse_string('פרק ב'))
        widget_2.button.bind(on_press=lambda x: self.on_press())
        self.perek_2 = widget_2

        widget_3 = LinkWidget(extraFunctions.reverse_string('פרק ג'))
        widget_3.button.bind(on_press=lambda x: self.on_press())
        self.perek_3 = widget_3

        widget_4 = LinkWidget(extraFunctions.reverse_string('פרק ד'))
        widget_4.button.bind(on_press=lambda x: self.on_press())
        self.perek_4 = widget_4

        widget_5 = LinkWidget(extraFunctions.reverse_string('פרק ה'))
        widget_5.button.bind(on_press=lambda x: self.on_press())
        self.perek_5 = widget_5

        widget_6 = LinkWidget(extraFunctions.reverse_string('פרק ו'))
        widget_6.button.bind(on_press=lambda x: self.on_press())
        self.perek_6 = widget_6

        widget_7 = LinkWidget(extraFunctions.reverse_string('פרק ז'))
        widget_7.button.bind(on_press=lambda x: self.on_press())
        self.perek_7 = widget_7

        widget_8 = LinkWidget(extraFunctions.reverse_string('פרק ח'))
        widget_8.button.bind(on_press=lambda x: self.on_press())
        self.perek_8 = widget_8

        widget_9 = LinkWidget(extraFunctions.reverse_string('פרק ט'))
        widget_9.button.bind(on_press=lambda x: self.on_press())
        self.perek_9 = widget_9

        # Adding widgets to the layout
        self.perakim = [self.perek_1, self.perek_2, self.perek_3, self.perek_4, self.perek_5,
                        self.perek_6, self.perek_7, self.perek_8, self.perek_9]
        for perek in self.perakim:
            self.layout.add_widget(perek)

    def on_press(self):
        self.manager.current = 'about'

    def on_press_perek_1(self):
        self.manager.current = 'berakhot_perek_1'


class BerakhotPerek1Screen(Screen):
    def __init__(self, **kwargs):
        super(BerakhotPerek1Screen, self).__init__(**kwargs)
        self.name = 'berakhot_perek_1'

        # Create the BoxLayout and add it to the screen
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Creating widgets
        widget_1 = LinkWidget(extraFunctions.reverse_string('משנה א'))
        widget_1.button.bind(on_press=lambda x: self.on_press())
        self.mishna_1 = widget_1

        widget_2 = LinkWidget(extraFunctions.reverse_string('משנה ב'))
        widget_2.button.bind(on_press=lambda x: self.on_press())
        self.mishna_2 = widget_2

        widget_3 = LinkWidget(extraFunctions.reverse_string('משנה ג'))
        widget_3.button.bind(on_press=lambda x: self.on_press())
        self.mishna_3 = widget_3

        widget_4 = LinkWidget(extraFunctions.reverse_string('משנה ד'))
        widget_4.button.bind(on_press=lambda x: self.on_press())
        self.mishna_4 = widget_4

        widget_5 = LinkWidget(extraFunctions.reverse_string('משנה ה'))
        widget_5.button.bind(on_press=lambda x: self.on_press())
        self.mishna_5 = widget_5

        # Adding widgets to the layout
        self.mishnayot = [self.mishna_1, self.mishna_2, self.mishna_3, self.mishna_4, self.mishna_5]
        for mishna in self.mishnayot:
            self.layout.add_widget(mishna)

    def on_press(self):
        self.manager.current = 'about'


class AboutScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = 'about'
        about_widget = LinkWidget("Go To Home")
        about_widget.button.bind(on_press=lambda x: self.on_press())

        self.add_widget(about_widget)

    def on_press(self):
        self.manager.current = 'home'
