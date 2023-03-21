from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import mishnayotText
import extraFunctions
from statistics import mean
from kivy.utils import get_color_from_hex
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget

"""
------------------------------------------------------------------------------------------------------------------------
GENERAL
------------------------------------------------------------------------------------------------------------------------
"""


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):

        # Init operations
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.current_parent = None

        # Creating mishnayot, perakim etc. and defining self.shas.
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

        self.show_home_screen()

    def show_item(self, item):

        # clear all widgets from main layout
        self.clear_widgets()

        # top part
        self.add_widget(TopPart(self, item))

        # set a way to go back
        self.current_parent = item  # seder/ masechet etc. where to go back to

        # current is a mishna
        if self.current_parent.children is None:

            # test 0 - first letter game
            test_0_widget = LinkWidget(extraFunctions.reverse_string('מבחן אות ראשונה'), self.current_parent)
            test_0_widget.button.bind(on_press=lambda x: self.current_parent.show_first_letter_game())
            self.add_widget(test_0_widget)

            # bottom part
            self.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))

        # current is at least a perek
        else:
            for child in self.current_parent.children:
                # creating widgets for all children and adding them
                widget = LinkWidget(extraFunctions.reverse_string(child.name), child)
                widget.button.bind(on_press=lambda x, w=widget: self.show_item(w.link))
                self.add_widget(widget)

            # bottom part
            self.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))

    def show_home_screen(self):

        # clear all widgets from main layout
        self.clear_widgets()

        # top part
        self.add_widget(TopPart(self, self.shas))

        # set where to go back to (None to go back)
        self.current_parent = None

        # Creating widgets for home screen setup
        for seder in self.shas.children:
            widget = LinkWidget(extraFunctions.reverse_string(seder.name), seder)
            widget.button.bind(on_press=lambda x, w=widget: self.show_item(w.link))
            self.add_widget(widget)

        # Bottom rectangle
        self.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))

    def show_at_least_a_perek_children(self, item):

        # clear all widgets from main layout
        self.clear_widgets()

        # top part
        self.add_widget(TopPart(self, item))

        # set a way to go back
        self.current_parent = item

        for child in self.current_parent.children:
            # creating widgets for all children and adding them
            widget = LinkWidget(extraFunctions.reverse_string(child.name), child)
            widget.button.bind(on_press=lambda x, w=widget: self.show_item(w.link))
            self.add_widget(widget)

        # bottom part
        self.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))

    def show_mishna_tests(self, mishna):

        # clear all widgets from main layout
        self.clear_widgets()

        # top part
        self.add_widget(TopPart(self, mishna))

        # set a way to go back
        self.current_parent = mishna

        # test 0 - first letter game
        test_0_widget = LinkWidget(extraFunctions.reverse_string('מבחן אות ראשונה'), self.current_parent)
        test_0_widget.button.bind(on_press=lambda x: self.current_parent.show_first_letter_game())
        self.add_widget(test_0_widget)

        # bottom part
        self.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))


class Item:
    def __init__(self, name: str, text: str, main_layout):
        self.name = name
        self.grade = 0
        self.text = text
        self.children = None
        self.parent = None
        self.main_layout = main_layout


class GenericItem(Item):
    def __init__(self, name: str, main_layout: MainLayout):
        super().__init__(name, "", main_layout)

    def set_grade(self):
        self.grade = mean([child.grade for child in self.children])
        self.parent.set_grade()


class Mishna(Item):
    def __init__(self, name: str, text: str, main_layout: MainLayout):
        super().__init__(name, text, main_layout)
        self.test_grades = [0]  # test_0: first letter game
        self.main_layout = main_layout

    def show_first_letter_game(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(TopPart(self.main_layout, self, True))
        game = FirstLetterGameHebrewPanel(self)
        self.main_layout.add_widget(game)
        self.main_layout.add_widget(Label(text='Bottom Rectangle', size_hint=(1, 0.05)))

    def show_tests(self):
        self.main_layout.show_mishna_tests(self)

    def set_grade(self, test_idx: int, test_grade: int):
        self.test_grades[test_idx] = test_grade
        self.grade = mean(self.test_grades)
        self.parent.set_grade()

    def refresh(self):
        self.main_layout.show_item(self)


class Perek(GenericItem):
    def __init__(self, name: str, mishnayot: list[Mishna], main_layout):
        super().__init__(name, main_layout)
        self.children = mishnayot


class Masechet(GenericItem):
    def __init__(self, name: str, perakim: list[Perek], main_layout):
        super().__init__(name, main_layout)
        self.children = perakim


class Seder(GenericItem):
    def __init__(self, name: str, mesachtot: list[Masechet], main_layout):
        super().__init__(name, main_layout)
        self.children = mesachtot


class Shas(GenericItem):
    def __init__(self, sedarim: list[Seder], main_layout):
        super().__init__('ש"ס', main_layout)
        self.children = sedarim

    def set_grade(self):
        self.grade = mean([child.grade for child in self.children])


class HebrewTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.is_reversed = False
        self.last_value = ""
        self.base_direction = "rtl"
        self.font_name = "Arial.ttf"
        self.halign = "right"

    def insert_text(self, substring, from_undo=False):
        # Override the default insert_text method to insert text at the beginning of the string
        substring = substring[::-1]  # Reverse the substring
        super().insert_text(substring, from_undo=from_undo)
        self.cursor = (0, self.cursor[1])  # Move the cursor to the beginning of the line after inserting text

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] == 8:  # backspace key
            self.text = self.text[1:]
            self.cursor = (0, self.cursor[1])
        else:
            super().keyboard_on_key_down(window, keycode, text, modifiers)


class LinkWidget(BoxLayout):
    def __init__(self, button_text: str, link, **kwargs):
        super().__init__(**kwargs)
        self.link = link  # seder/ masechet etc.

        # Create the icon
        self.icon = Image(source='icons/torah256.png', size_hint_x=0.015)
        self.add_widget(self.icon)

        # Create the label
        self.label = Label(text=f'{link.grade}%', size_hint_x=0.015)
        self.add_widget(self.label)

        # Create the button
        self.button = Button(text=f'{button_text}',
                             size_hint_x=0.3,
                             background_color=(1, 0, 0, 1),
                             font_name="Arial.ttf",
                             )
        self.add_widget(self.button)

    def set_percentile(self, percentile: int):
        self.label.text = f'{percentile}%'

    def set_icon(self, value: bool, icon_1: str, icon_2: str):
        if value:
            self.icon.source = f'icons/{icon_1}.png'
        else:
            self.icon.source = f'icons/{icon_2}.png'


class TopPart(BoxLayout):
    def __init__(self, main_layout: MainLayout, item, is_test=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.main_layout = main_layout
        self.item = item
        self.size_hint_y = 0.07
        if not is_test:
            back_button = Button(text=f'back button',
                                 size_hint_x=0.15,
                                 on_press=lambda x: self.main_layout.show_item(self.item.parent),
                                 )
        else:
            back_button = Button(text=f'back button',
                                 size_hint_x=0.15,
                                 on_press=lambda x: self.item.show_tests(),
                                 )
        middle_label = Label(text=f'{item.grade}%  :{extraFunctions.reverse_string(item.name)}',
                             base_direction="rtl",
                             font_name="Arial.ttf",
                             halign="right",
                             size_hint_x=0.7,
                             font_size='25sp'
                             )
        pop_up_button = Button(text="pop up", on_press=extraFunctions.open_popup, size_hint_x=0.15)

        if self.item.parent is not None:
            self.add_widget(back_button)
        else:
            self.add_widget(Label(text=f'',
                                  size_hint_x=0.15, )
                            )
        self.add_widget(middle_label)
        self.add_widget(pop_up_button)


"""
------------------------------------------------------------------------------------------------------------------------
FIRST LETTER GAME
------------------------------------------------------------------------------------------------------------------------
"""


class FirstLetterGameHebrewTextInput(HebrewTextInput):  # add given mishna because it has main layout in it!
    def __init__(self, game, given_mishna, text, next_w=None, **kwargs):
        if len(text) == 0:
            raise Exception("text length is 0")
        super().__init__(**kwargs)
        self.hint_text = text[0]
        self.font_size = 35
        self.hint_text_color = get_color_from_hex('#0000FF')
        self.foreground_color = get_color_from_hex('#0000FF')
        self.target_text = text
        self.background_color = [0, 0, 0, 1]
        self.next = next_w
        self.mishna = given_mishna
        self.game = game
        self.size_hint = (None, None)
        self.size = (extraFunctions.get_text_size(text, self.font_name, self.font_size)[0] + 12,
                     extraFunctions.get_text_size(text, self.font_name, self.font_size)[1] + 15)
        self.skip_on_text = False

    def on_text(self, instance, value):
        if self.skip_on_text:
            self.skip_on_text = False
            self.lock(True)
        else:
            value = value[::-1]
            if not extraFunctions.is_sub_str_from_start(value, self.target_text):
                self.skip_on_text = True
                self.text = self.target_text[::-1]  # here on_text will be triggered
            elif value == self.target_text:
                self.lock(False)
            elif extraFunctions.is_hebrew_characters_complete(value, self.target_text):
                self.text = self.target_text[::-1]  # here on_text will be triggered and the case before will...
                #  ...be executed

    def lock(self, is_fail: bool):
        self.readonly = True
        self.focus = False
        self.disabled = True
        self.background_disabled_normal = ""
        self.background_color = [0, 0, 0, 1]
        self.game.total_words += 1
        if is_fail:
            self.foreground_color = (1, 0, 0, 1)
            self.disabled_foreground_color = (1, 0, 0, 1)
        else:
            self.foreground_color = (0, 255, 0, 1)
            self.disabled_foreground_color = (0, 255, 0, 1)
            self.game.words_right += 1
            if self.next is not None:
                self.next.focus = True
        if self.next is not None:
            self.parent.parent.parent.scroll_to_widget(self.next)
        else:
            grade = int((self.game.words_right / self.game.total_words) * 100)
            self.mishna.set_grade(0, grade)
            self.mishna.refresh()

    def focus_on_widget(self):
        self.focus = True


class FirstLetterGameHebrew(BoxLayout):
    def __init__(self, given_mishna, scroll_view, **kwargs):
        """
        First game letter widget
        :param given_mishna: given_mishna.text in hebrew that can be multiline as follows:
        given_mishna.text = '''
            מאימתי קורין את שמע בערבית?
            משעה שהכהנים נכנסים לאכול בתרומתן.
        '''
        etc.
        :param scroll_view: The parent scroll view.
        :param kwargs: kwargs
        """

        # init operations
        super().__init__(orientation='vertical', **kwargs)
        self.scroll_view = scroll_view
        self.words_right = 0
        self.total_words = 0

        # transforming given_str into a str_matrix that will look as follows:
        # str_matrix = [
        #    [word4, word3, word2, word1],
        #    [word8, word7, word6, word5]
        # ]
        #
        str_matrix = extraFunctions.string_hebrew_to_matrix(given_mishna.text)

        # creating self.widgets from str_matrix
        reversed_widgets_matrix = []
        line_counter = 0
        col_counter = 0
        prev_widget = None
        for line in reversed(str_matrix):
            widgets_new_line = []
            for str_1 in line:
                if line_counter == 0 and col_counter == 0:
                    prev_widget = FirstLetterGameHebrewTextInput(self, given_mishna, str_1, None)
                    widgets_new_line.append(prev_widget)
                else:
                    prev_widget = FirstLetterGameHebrewTextInput(self, given_mishna, str_1, prev_widget)
                    widgets_new_line.append(prev_widget)
                col_counter += 1
            reversed_widgets_matrix.append(widgets_new_line)
            line_counter += 1
        self.widgets = []
        for line in reversed(reversed_widgets_matrix):
            self.widgets.append(line)

        max_width_line = 0
        col_height = 0
        for line in self.widgets:
            col_height += line[0].height
            cur_line_width = 0
            for widget in line:
                cur_line_width += widget.width
            if cur_line_width >= max_width_line:
                max_width_line = cur_line_width
        max_width_line = max(max_width_line, Window.width)
        max_width_col = max(col_height, Window.height)
        self.size_hint = [None, None]
        self.size = [max_width_line, max_width_col]

        for line in self.widgets:
            line_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=line[0].height)

            spacer = Widget()
            line_layout.add_widget(spacer)

            for widget in line:
                line_layout.add_widget(widget)
            self.add_widget(line_layout)

        # Add a spacer widget at the bottom of the layout
        bottom_spacer = Widget(size_hint_y=None, height=max(0, Window.height - col_height))
        self.add_widget(bottom_spacer)

    def on_parent(self, *args):
        if self.parent is not None:
            Clock.schedule_once(lambda dt: self.widgets[0][-1].focus_on_widget(), 0.5)
            self.scroll_view.scroll_to_widget(self.widgets[0][-1])

    def get_total_lines_height(self):
        total_height = 0
        for line in self.widgets:
            total_height += line[0].height
        return total_height


class FirstLetterGameHebrewPanel(ScrollView):
    def __init__(self, mishna, **kwargs):
        super(FirstLetterGameHebrewPanel, self).__init__(**kwargs)
        self.game = FirstLetterGameHebrew(mishna, self)
        self.mishna = mishna
        self.add_widget(self.game)
        self.always_overscroll = True
        self.scroll_x = 1

    def scroll_to_widget(self, widget):
        self.scroll_to(widget)
