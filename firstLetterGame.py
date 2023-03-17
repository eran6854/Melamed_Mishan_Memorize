from kivy.app import App
from textModule import HebrewTextInput
from extraFunctions import is_sub_str_from_start, get_text_size, is_hebrew_characters_complete, \
    string_hebrew_to_matrix
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from mishnayotText import berakhot_1_1_text
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget


class FirstLetterGameHebrewTextInput(HebrewTextInput):
    def __init__(self, text, next_w=None, **kwargs):
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
        self.size_hint = (None, None)
        self.size = (get_text_size(text, self.font_name, self.font_size)[0] + 12,
                     get_text_size(text, self.font_name, self.font_size)[1] + 15)

    def on_text(self, instance, value):
        value = value[::-1]
        if not is_sub_str_from_start(value, self.target_text):
            self.text = self.target_text[::-1]
            self.lock(True)
        elif value == self.target_text:
            self.lock(False)
        elif is_hebrew_characters_complete(value, self.target_text):
            self.text = self.target_text[::-1]
            self.lock(False)

    def lock(self, is_fail: bool):
        self.readonly = True
        self.focus = False
        self.disabled = True
        self.background_disabled_normal = ""
        self.background_color = [0, 0, 0, 1]
        if is_fail:
            self.foreground_color = (1, 0, 0, 1)
            self.disabled_foreground_color = (1, 0, 0, 1)
        else:
            self.foreground_color = (0, 255, 0, 1)
            self.disabled_foreground_color = (0, 255, 0, 1)
        if self.next is not None:
            self.next.focus = True
            self.parent.parent.parent.scroll_to_widget(self.next)

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

        super().__init__(orientation='vertical', **kwargs)
        self.scroll_view = scroll_view

        # transforming given_str into a str_matrix that will look as follows:
        # str_matrix = [
        #    [word4, word3, word2, word1],
        #    [word8, word7, word6, word5]
        # ]
        #
        str_matrix = string_hebrew_to_matrix(given_mishna.text)

        # creating self.widgets from str_matrix
        reversed_widgets_matrix = []
        line_counter = 0
        col_counter = 0
        prev_widget = None
        for line in reversed(str_matrix):
            widgets_new_line = []
            for str_1 in line:
                if line_counter == 0 and col_counter == 0:
                    prev_widget = FirstLetterGameHebrewTextInput(str_1, None)
                    widgets_new_line.append(prev_widget)
                else:
                    prev_widget = FirstLetterGameHebrewTextInput(str_1, prev_widget)
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


class MyApp(App):
    def build(self):
        return FirstLetterGameHebrewPanel(berakhot_1_1_text)


if __name__ == '__main__':
    MyApp().run()
