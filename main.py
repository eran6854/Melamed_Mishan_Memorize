from kivy.app import App
from textModule import LinkWidget
import mishnayotText
from kivy.uix.boxlayout import BoxLayout
import extraFunctions
from firstLetterGame import FirstLetterGameHebrewPanel
from kivy.uix.label import Label
from statistics import mean


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):

        # Init operations
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = "vertical"

        # Creating mishnayot, perakim etc.
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

        # init where to go back to (None)
        self.current_parent = None

        # Top rectangle
        self.add_widget(Label(text='Top Rectangle', size_hint=(1, 0.05)))

        # Creating widgets for home screen setup
        for seder in self.shas.children:
            widget = LinkWidget(extraFunctions.reverse_string(seder.name), seder)
            widget.button.bind(on_press=lambda x, w=widget: self.on_press(w.link))
            self.add_widget(widget)

        # Bottom rectangle
        self.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))

    def on_press(self, link):

        # clear all widgets from main layout
        self.clear_widgets()

        # top part
        self.add_widget(Label(text='Top Rectangle', size_hint=(1, 0.05)))

        # set a way to go back
        self.current_parent = link  # seder/ masechet etc.

        # current is a mishna
        if self.current_parent.children is None:

            # test 0 - first letter game
            test_0_widget = LinkWidget(extraFunctions.reverse_string('מבחן אות ראשונה'), self.current_parent)
            test_0_widget.button.bind(on_press=lambda x: self.current_parent.on_press_test_1())
            self.add_widget(test_0_widget)

            # bottom part
            self.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))

        # current is at least a perek
        else:
            for child in self.current_parent.children:

                # creating widgets for all children and adding them
                widget = LinkWidget(extraFunctions.reverse_string(child.name), child)
                widget.button.bind(on_press=lambda x, w=widget: self.on_press(w.link))
                self.add_widget(widget)

            # bottom part
            self.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))


class Mishna:
    def __init__(self, name: str, text: str, main_layout):
        self.name = name
        self.test_grades = [0]  # test_0: first letter game
        self.grade = 0
        self.text = text
        self.children = None
        self.parent = None
        self.main_layout = main_layout

    def on_press_test_1(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(Label(text='Top Rectangle', size_hint=(1, 0.05)))
        game = FirstLetterGameHebrewPanel(self)
        self.main_layout.add_widget(game)
        self.main_layout.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))

    def set_grade(self, test_idx: int, test_grade: int):
        self.test_grades[test_idx] = test_grade
        self.grade = mean(self.test_grades)
        self.parent.set_grade()

    def refresh(self):

        # clear everything from main layout
        self.main_layout.clear_widgets()

        # top part
        self.main_layout.add_widget(Label(text='Top Rectangle', size_hint=(1, 0.05)))

        # set where to go back to
        self.main_layout.current_parent = self

        # test 0 - first letter game
        test_0_widget = LinkWidget(extraFunctions.reverse_string('מבחן אות ראשונה'), self)
        test_0_widget.button.bind(on_press=lambda x: self.on_press_test_1())
        self.main_layout.add_widget(test_0_widget)

        # bottom part
        self.main_layout.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))


class Perek:
    def __init__(self, name: str, mishnayot: list[Mishna], main_layout):
        self.name = name
        self.grade = 0
        self.children = mishnayot
        self.parent = None
        self.main_layout = main_layout

    def set_grade(self):
        self.grade = mean([child.grade for child in self.children])
        self.parent.set_grade()


class Masechet:
    def __init__(self, name: str, perakim: list[Perek], main_layout):
        self.name = name
        self.grade = 0
        self.children = perakim
        self.parent = None
        self.main_layout = main_layout

    def set_grade(self):
        self.grade = mean([child.grade for child in self.children])
        self.parent.set_grade()


class Seder:
    def __init__(self, name: str, mesachtot: list[Masechet], main_layout):
        self.name = name
        self.grade = 0
        self.children = mesachtot
        self.parent = None
        self.main_layout = main_layout

    def set_grade(self):
        self.grade = mean([child.grade for child in self.children])


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
