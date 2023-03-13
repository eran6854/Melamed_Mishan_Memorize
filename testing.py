from kivy.app import App
from modulsKivy import HebrewTextInput
from extraFunctions import is_sub_str_from_start, get_text_size, pixels_to_relative_size
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout
from mishnayotText import brachot_1_1


class FirstLetterGameHebrewTextInput(HebrewTextInput):
    def __init__(self, text, next_w=None, **kwargs):
        if len(text) == 0:
            raise Exception("text length is 0")
        super().__init__(**kwargs)
        self.hint_text = text[0]
        self.font_size = 25
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
        print(value)
        print(self.target_text)
        if not is_sub_str_from_start(value, self.target_text):
            self.text = self.target_text[::-1]
            self.lock(True)
        elif value == self.target_text:
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


class FirstLetterGameHebrew(FloatLayout):
    def __init__(self, str_matrix, **kwargs):
        """
        First game letter widget
        :param str_matrix: given in the following form:
        str_matrix = [
            [str4, str3, str2, str1],
            [str8, str7, str6, str5]
        ]
        etc.
        :param kwargs: kwargs
        """

        super().__init__(**kwargs)

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

        # adding the widgets to self, sizing them and positioning them
        # at this point self.widgets should look like this:
        # self.widgets = [[widget_4, widget_3, widget_2, widget_1],
        #                [widget_8, widget_7, widget_6, widget_5]]
        reversed_widgets = []
        for line in self.widgets:
            reversed_widgets_new_line = []
            for widget in reversed(line):
                reversed_widgets_new_line.append(widget)
            reversed_widgets.append(reversed_widgets_new_line)

        for line_idx, line in enumerate(reversed_widgets):
            if line_idx == 0:
                for w_idx, widget in enumerate(line):
                    if w_idx == 0:
                        widget.pos_hint = {"right": 1, "top": 1}
                    else:
                        prev_widget = line[w_idx - 1]
                        widget.pos_hint = {
                            "right": prev_widget.pos_hint["right"] - pixels_to_relative_size(prev_widget.width)[0],
                            "top": 1}
            else:
                prev_line = reversed_widgets[line_idx - 1]
                for w_idx, widget in enumerate(line):
                    dist_from_top = prev_line[0].pos_hint["top"] - pixels_to_relative_size(prev_line[0].height)[1]
                    if w_idx == 0:
                        widget.pos_hint = {"right": 1, "top": dist_from_top}
                    else:
                        prev_widget = line[w_idx - 1]
                        widget.pos_hint = {
                            "right": prev_widget.pos_hint["right"] - pixels_to_relative_size(prev_widget.width)[0],
                            "top": dist_from_top}

        for line in self.widgets:
            for widget in line:
                self.add_widget(widget)
        self.widgets[0][-1].focus = True

        # calc size of max line and col for scroll
        max_width_line = 0
        col_height = 0
        for line in self.widgets:
            col_height += line[0].height
            cur_line_width = 0
            for widget in line:
                cur_line_width += widget.width
            if cur_line_width >= max_width_line:
                max_width_line = cur_line_width
        self.size_for_scroll_view = [max_width_line + 20, col_height + 20]
        print(max_width_line, col_height)


class MyApp(App):
    def build(self):
        str1 = "אחת"
        str2 = "שתיים"
        str3 = "שלוששששש"
        str4 = "ארבע?"
        str5 = "שלום"
        str6 = "עליך"
        str7 = "רבי"
        str8 = "עקיבא."

        str_matrix = [
            [str4, str3, str2, str1],
            [str8, str7, str6, str5]
        ]

        return FirstLetterGameHebrew(brachot_1_1)


if __name__ == '__main__':
    MyApp().run()
