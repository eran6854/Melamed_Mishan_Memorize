from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import extraFunctions
from kivy.utils import get_color_from_hex
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
import database

"""
------------------------------------------------------------------------------------------------------------------------
Constants
------------------------------------------------------------------------------------------------------------------------
"""
FIRST_LETTER_TEST = "מבחן אות ראשונה"

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
        self.cursor_id = "shas"
        self.cursor_name = database.get_name(self.cursor_id)
        self.cursor_parent = database.get_parent(self.cursor_id)
        self.cursor_children_id = database.get_children(self.cursor_id)
        self.cursor_grade = database.get_grade(self.cursor_id)
        self.size = [Window.width, Window.height]
        self.show_item()

    def show_item(self):

        # current is a mishna
        if self.cursor_children_id is None:
            self.show_mishna_tests()

        # current is at least a perek
        else:
            self.show_at_least_a_perek_children()

    def show_home_screen(self):
        pass
        # # clear all widgets from main layout
        # self.clear_widgets()
        #
        # # top part
        # self.add_widget(TopPart(self, self.shas))
        #
        # # set where to go back to (None to go back)
        # self.current_parent = None
        #
        # # Creating widgets for home screen setup
        # for seder in self.shas.children:
        #     widget = LinkWidget(self, extraFunctions.reverse_string(seder.name), seder)
        #     widget.button.bind(on_press=lambda x, w=widget: self.show_item(w.link))
        #     self.add_widget(widget)
        #
        # # Bottom rectangle
        # self.add_widget(Label(text='Bottom Rectangle', size_hint_y=0.15))

    def show_at_least_a_perek_children(self):

        # clear all widgets from main layout
        self.clear_widgets()

        # top part
        self.add_widget(TopPart(self))

        widget_list = []
        for child_id in self.cursor_children_id:
            # creating widgets for all children and adding them
            child_name = database.get_name(child_id)
            widget = LinkWidget(self, extraFunctions.reverse_string(child_name), child_id)
            widget_list.append(widget)
        self.add_widget(MiddlePart(widget_list))

        # bottom part
        self.add_widget(Label(text='Bottom Rectangle', size_hint_y=0.15))

    def show_mishna_tests(self):

        # clear all widgets from main layout
        self.clear_widgets()

        # top part
        self.add_widget(TopPart(self))

        # test 1 - first letter game
        test_0_widget = LinkWidget(self,
                                   extraFunctions.reverse_string(FIRST_LETTER_TEST),
                                   self.cursor_id,
                                   1)
        self.add_widget(test_0_widget)

        # bottom part
        self.add_widget(Label(text='Bottom Rectangle', size_hint_y=0.15))

    def update_cursor(self, new_cursor_id):
        self.cursor_id = new_cursor_id
        self.cursor_name = database.get_name(self.cursor_id)
        self.cursor_parent = database.get_parent(self.cursor_id)
        self.cursor_children_id = database.get_children(self.cursor_id)
        self.cursor_grade = database.get_grade(self.cursor_id)

    def show_first_letter_game(self):
        self.clear_widgets()
        self.add_widget(TopPart(self, True))
        mishna_text = database.get_text(self.cursor_id)
        game = FirstLetterGameHebrewPanel(self, self.cursor_id, mishna_text)
        self.add_widget(game)
        self.add_widget(Label(text='Bottom Rectangle', size_hint_y=0.15))

# class Item:
#     def __init__(self, name: str, text: str, main_layout):
#         self.name = name
#         self.grade = 0
#         self.text = text
#         self.children = None
#         self.parent = None
#         self.main_layout = main_layout
#
#     def __str__(self):
#         return self.name
#
#     def __repr__(self):
#         return self.name
#
#
# class GenericItem(Item):
#     def __init__(self, name: str, main_layout: MainLayout):
#         super().__init__(name, "", main_layout)
#
#     def set_grade(self):
#         self.grade = int(mean([child.grade for child in self.children]))
#         self.parent.set_grade()
#
#
# class Mishna(Item):
#     def __init__(self, name: str, text: str, main_layout: MainLayout):
#         super().__init__(name, text, main_layout)
#         self.test_grades = [0]  # test_0: first letter game
#         self.main_layout = main_layout
#
#     def show_first_letter_game(self):
#         self.main_layout.clear_widgets()
#         self.main_layout.add_widget(TopPart(self.main_layout, self, True))
#         game = FirstLetterGameHebrewPanel(self)
#         self.main_layout.add_widget(game)
#         self.main_layout.add_widget(Label(text='Bottom Rectangle', size_hint_y=0.15))
#
#     def show_tests(self):
#         self.main_layout.show_mishna_tests(self)
#
#     def set_grade(self, test_idx: int, test_grade: int):
#         self.test_grades[test_idx] = test_grade
#         self.grade = int(mean(self.test_grades))
#         self.parent.set_grade()
#
#     def refresh(self):
#         self.main_layout.show_item()
#
#
# class Perek(GenericItem):
#     def __init__(self, name: str, mishnayot: list[Mishna], main_layout):
#         super().__init__(name, main_layout)
#         self.children = mishnayot
#
#
# class Masechet(GenericItem):
#     def __init__(self, name: str, perakim: list[Perek], main_layout):
#         super().__init__(name, main_layout)
#         self.children = perakim
#
#
# class Seder(GenericItem):
#     def __init__(self, name: str, mesachtot: list[Masechet], main_layout):
#         super().__init__(name, main_layout)
#         self.children = mesachtot
#
#
# class Shas(GenericItem):
#     def __init__(self, sedarim: list[Seder], main_layout):
#         super().__init__('ש"ס', main_layout)
#         self.children = sedarim
#
#     def set_grade(self):
#         self.grade = mean([child.grade for child in self.children])


class HebrewTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.is_reversed = False
        self.last_value = ""
        self.base_direction = "rtl"
        self.font_name = "Arial.ttf"
        self.halign = "right"

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

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
    def __init__(self, main_layout: MainLayout, button_text: str, item_id: str, test_num=None, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = main_layout
        self.item_id = item_id
        self.test_num = test_num
        self.button_text = button_text
        self.size_hint = [None, None]
        self.size = [Window.width, Window.height * 0.15]
        # Create the icon
        self.icon = Image(source='icons/torah256.png', size_hint_x=0.015)
        self.add_widget(self.icon)

        # Create the label
        if test_num is None:
            self.item_grade = database.get_grade(item_id)
        elif test_num == 1:
            self.item_grade = database.get_test_1_grade(self.item_id)
        self.label = Label(text=f'{self.item_grade}%', size_hint_x=0.015)
        self.add_widget(self.label)

        # Create the button
        self.button = Button(text=f'{button_text}',
                             size_hint_x=0.3,
                             background_color=(1, 0, 0, 1),
                             font_name="Arial.ttf",
                             on_press=self.on_button_press
                             )
        self.add_widget(self.button)

    def __str__(self):
        if not hasattr(self, 'link') or not hasattr(self, 'button_text'):
            return "Link Widget"
        else:
            return f'parent: {self.link}, text: {self.button_text}'

    def __repr__(self):
        if not hasattr(self, 'link') or not hasattr(self, 'button_text'):
            return "Link Widget"
        else:
            return f'parent: {self.link}, text: {self.button_text}'

    def set_percentile(self, percentile: int):
        self.label.text = f'{percentile}%'

    def set_icon(self, value: bool, icon_1: str, icon_2: str):
        if value:
            self.icon.source = f'icons/{icon_1}.png'
        else:
            self.icon.source = f'icons/{icon_2}.png'

    def on_button_press(self, instance):
        if self.test_num is None:
            self.main_layout.update_cursor(self.item_id)
            self.main_layout.show_item()
        elif self.test_num == 1:
            self.main_layout.show_first_letter_game()
        else:
            pass


class TopPart(BoxLayout):
    def __init__(self, main_layout: MainLayout, is_test=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.main_layout = main_layout
        self.size_hint = [None, None]
        self.size = [Window.width, Window.height * 0.09]
        self.is_test = is_test
        self.item_id = main_layout.cursor_id
        self.item_name = main_layout.cursor_name
        self.item_grade = main_layout.cursor_grade
        self.item_parent = main_layout.cursor_parent

        back_button = Button(text=f'back button',
                             size_hint_x=0.15,
                             on_press=self.on_back_button_press,
                             )
        middle_label = Label(text=f'{self.item_grade}%  :{extraFunctions.reverse_string(self.item_name)}',
                             base_direction="rtl",
                             font_name="Arial.ttf",
                             halign="right",
                             size_hint_x=0.7,
                             font_size='25sp'
                             )
        pop_up_button = Button(text="...",
                               on_press=extraFunctions.open_popup,
                               size_hint_x=0.15,
                               font_size=50
                               )

        if self.item_parent is not None:
            self.add_widget(back_button)
        else:
            self.add_widget(Label(text=f'',
                                  size_hint_x=0.15, )
                            )
        self.add_widget(middle_label)
        self.add_widget(pop_up_button)

    def __str__(self):
        if hasattr(self, 'item'):
            return f'Top part, item: {self.item_name}'
        else:
            return "Top part"

    def __repr__(self):
        if hasattr(self, 'item'):
            return f'Top part, item: {self.item_name}'
        else:
            return "Top part"

    def on_back_button_press(self, instance):
        if self.is_test:
            self.main_layout.show_item()
        else:
            self.main_layout.update_cursor(self.item_parent)
            self.main_layout.show_item()


class MiddlePart(ScrollView):
    def __init__(self, widgets: list, **kwargs):
        super().__init__(**kwargs)
        self.widgets = widgets
        self.scroll_x = 0
        self.scroll_y = 1
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.always_overscroll = False
        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)

        height = 0
        for widget in widgets:
            self.layout.add_widget(widget)
            height += widget.height  # assuming the widgets have height attribute

        # bottom spacer
        bottom_spacer = Widget()
        self.layout.add_widget(bottom_spacer)
        height += bottom_spacer.height  # assuming the bottom_spacer has height attribute

        # Update the height of the layout
        self.layout.height = height

        self.add_widget(self.layout)
    def __str__(self):
        if not hasattr(self, 'link'):
            return "Middle Part"
        else:
            return f'Middle part, link: {self.widgets[0].item_id}'

    def __repr__(self):
        if not hasattr(self, 'link'):
            return "Middle Part"
        else:
            return f'Middle part, link: {self.widgets[0].item_id}'


"""
------------------------------------------------------------------------------------------------------------------------
FIRST LETTER GAME
------------------------------------------------------------------------------------------------------------------------
"""


class FirstLetterGameHebrewTextInput(HebrewTextInput):  # add given mishna because it has main layout in it!
    def __init__(self, main_layout: MainLayout, game, mishna_id, text, next_w=None, **kwargs):
        if len(text) == 0:
            raise Exception("text length is 0")
        super().__init__(**kwargs)
        self.main_layout = main_layout
        self.mishna_id = mishna_id
        self.hint_text = text[0]
        self.font_size = 35
        self.hint_text_color = get_color_from_hex('#0000FF')
        self.foreground_color = get_color_from_hex('#0000FF')
        self.target_text = text
        self.background_color = [0, 0, 0, 1]
        self.next = next_w
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
            database.update_test_1(self.mishna_id, grade)
            self.main_layout.show_item()

    def focus_on_widget(self):
        self.focus = True


class FirstLetterGameHebrew(BoxLayout):
    def __init__(self, main_layout: MainLayout, mishna_id, mishna_text, scroll_view, **kwargs):

        # init operations
        super().__init__(orientation='vertical', **kwargs)
        self.main_layout = main_layout
        self.mishna_id = mishna_id
        self.scroll_view = scroll_view
        self.words_right = 0
        self.total_words = 0

        # transforming given_str into a str_matrix that will look as follows:
        # str_matrix = [
        #    [word4, word3, word2, word1],
        #    [word8, word7, word6, word5]
        # ]
        #
        str_matrix = extraFunctions.string_hebrew_to_matrix(mishna_text)

        # creating self.widgets from str_matrix
        reversed_widgets_matrix = []
        line_counter = 0
        col_counter = 0
        prev_widget = None
        for line in reversed(str_matrix):
            widgets_new_line = []
            for str_1 in line:
                if line_counter == 0 and col_counter == 0:
                    prev_widget = FirstLetterGameHebrewTextInput(self.main_layout, self, mishna_id, str_1, None)  # check
                    widgets_new_line.append(prev_widget)
                else:
                    prev_widget = FirstLetterGameHebrewTextInput(self.main_layout, self, mishna_id, str_1, prev_widget)
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
        bottom_spacer = Widget()
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
    def __init__(self, main_layout: MainLayout, mishna_id, mishna_text: str, **kwargs):
        super(FirstLetterGameHebrewPanel, self).__init__(**kwargs)
        self.game = FirstLetterGameHebrew(main_layout, mishna_id, mishna_text, self)
        self.main_layout = main_layout
        self.mishna_id = mishna_id
        self.mishna_text = mishna_text
        self.add_widget(self.game)
        self.always_overscroll = True
        self.scroll_x = 1

    def scroll_to_widget(self, widget):
        self.scroll_to(widget)
