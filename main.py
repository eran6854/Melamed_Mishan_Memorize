from kivy.app import App
from textModule import LinkWidget
import mishnayotText
from kivy.uix.boxlayout import BoxLayout
import extraFunctions
from firstLetterGame import FirstLetterGameHebrewPanel


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = "vertical"

        berakhot_1_1 = Mishna("משנה א", mishnayotText.berakhot_1_1_text, self)
        berakhot_1_2 = Mishna("משנה ב", mishnayotText.berakhot_1_2_text, self)
        berakhot_1 = Perek("פרק א", [berakhot_1_1, berakhot_1_2], self)
        berakhot = Masechet("מסכת ברכות", [berakhot_1], self)
        zeraim = Seder("סדר זרעים", [berakhot], self)
        shas = Shas([zeraim], self)

        for child in berakhot_1.children:
            child.parent = berakhot_1

        for child in berakhot.children:
            child.parent = berakhot

        for child in zeraim.children:
            child.parent = zeraim

        for child in shas.children:
            child.parent = shas

        self.shas = shas

        self.present_back = None
        self.widgets = []

        # Creating widgets
        for seder in self.shas.children:
            widget = LinkWidget(extraFunctions.reverse_string(seder.name), seder)
            widget.button.bind(on_press=lambda x, w=widget: self.on_press(w))
            self.widgets.append(widget)
            self.add_widget(widget)

    def on_press(self, widget):
        self.clear_widgets()
        self.present_back = widget.link
        self.widgets = []

        # current is a mishna
        if self.present_back.children is None:
            for test in self.present_back.test_widgets:
                self.widgets.append(test)
                self.add_widget(test)

        # current is at least a perek
        else:
            for child in self.present_back.children:
                widget = LinkWidget(extraFunctions.reverse_string(child.name), child)
                widget.button.bind(on_press=lambda x, w=widget: self.on_press(w))
                self.widgets.append(widget)
                self.add_widget(widget)


class Mishna:
    def __init__(self, name: str, text: str, main_layout):
        self.name = name
        self.test_1_grade = 0
        self.text = text
        self.children = None
        self.parent = None
        self.main_layout = main_layout

        test_1_widget = LinkWidget(extraFunctions.reverse_string('מבחן אות ראשונה'), main_layout)

        test_1_widget.button.bind(on_press=lambda x: self.on_press_test_1())
        self.test_widgets = [test_1_widget]

    def on_press_test_1(self):
        self.main_layout.clear_widgets()
        game = FirstLetterGameHebrewPanel(self.text)
        self.main_layout.add_widget(game)



class Perek:
    def __init__(self, name: str, mishnayot: list[Mishna], main_layout):
        self.name = name
        self.grade = 0
        self.children = mishnayot
        self.parent = None
        self.main_layout = main_layout


class Masechet:
    def __init__(self, name: str, perakim: list[Perek], main_layout):
        self.name = name
        self.grade = 0
        self.children = perakim
        self.parent = None
        self.main_layout = main_layout


class Seder:
    def __init__(self, name: str, mesachtot: list[Masechet], main_layout):
        self.name = name
        self.grade = 0
        self.children = mesachtot
        self.parent = None
        self.main_layout = main_layout


class Shas:
    def __init__(self, sedarim: list[Seder], main_layout):
        self.children = sedarim
        self.parent = None
        self.main_layout = main_layout


class MyApp(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    MyApp().run()
