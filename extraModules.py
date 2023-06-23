import time
import extraFunctions
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import database
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.metrics import dp
from datetime import datetime, timedelta
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup
import threading

"""
------------------------------------------------------------------------------------------------------------------------
Constants
------------------------------------------------------------------------------------------------------------------------
"""
FIRST_LETTER_TEST = "מבחן אות ראשונה"
READ_OUT_LOUD = "הקראה בקול"
IM_DONE = "סיימתי"
I_KNEW_THE_ANSWER = "ידעתי את התשובה"
I_WAS_WRONG = "טעיתי"
FINAL_TEST = "מבחן סוף"
FINISH_GAME = "סיים מבחן"
RESET = "אתחל את"
READ_OUT_LOUD_TIME = 5
CLOSE = "סגור"
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
        self.bottom_part = None
        self.current_game = None
        self.show_item()

    def show_item(self):
        self.cursor_grade = database.get_grade(self.cursor_id)
        self.bottom_part = None

        # current is a mishna
        if self.cursor_children_id is None:
            self.show_mishna_tests()

        # current is at least a perek
        else:
            self.show_at_least_a_perek_children()

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

        # test 0 - read out loud
        test_0_widget = LinkWidget(self,
                                   extraFunctions.reverse_string(READ_OUT_LOUD),
                                   self.cursor_id,
                                   0)
        self.add_widget(test_0_widget)

        # test 1 - first letter game
        test_1_widget = LinkWidget(self,
                                   extraFunctions.reverse_string(FIRST_LETTER_TEST),
                                   self.cursor_id,
                                   1)
        self.add_widget(test_1_widget)

        # test 2 - no hint test
        test_2_widget = LinkWidget(self,
                                   extraFunctions.reverse_string(FINAL_TEST),
                                   self.cursor_id,
                                   2)
        self.add_widget(test_2_widget)

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
        game = LetterGamePanel(self, self.cursor_id, mishna_text)
        self.current_game = game
        self.add_widget(game)
        bottom_part = BottomPartLetterGame(self)
        self.add_widget(bottom_part)
        self.bottom_part = bottom_part

    def show_read_out_loud_game(self):
        self.clear_widgets()
        self.add_widget(TopPart(self, True))
        mishna_text = database.get_text(self.cursor_id)
        game = ReadOutLoudGamePanel(self, self.cursor_id, mishna_text)
        timer = TimerWidget(self)
        self.add_widget(timer)
        self.add_widget(game)
        self.add_widget(timer.button)

    def show_final_test(self):
        self.clear_widgets()
        self.add_widget(TopPart(self, True))
        mishna_text = database.get_text(self.cursor_id)
        game = LetterGamePanel(self, self.cursor_id, mishna_text, False)
        self.current_game = game
        self.add_widget(game)
        bottom_part = BottomPartLetterGame(self)
        self.add_widget(bottom_part)
        self.bottom_part = bottom_part


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
        elif test_num == 0:
            self.item_grade = database.get_test_0_grade(self.item_id)
        else:
            self.item_grade = database.get_test_2_grade(self.item_id)
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
        elif self.test_num == 0:
            self.main_layout.show_read_out_loud_game()
        elif self.test_num == 1:
            self.main_layout.show_first_letter_game()
        else:
            self.main_layout.show_final_test()


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
                               on_press=self.open_popup,
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
        if hasattr(self, 'item_id'):
            return f'Top part, item: {self.item_id}'
        else:
            return "Top part"

    def __repr__(self):
        if hasattr(self, 'item_id'):
            return f'Top part, item: {self.item_id}'
        else:
            return "Top part"

    def on_back_button_press(self, instance):
        if self.is_test:
            self.main_layout.show_item()
        else:
            self.main_layout.update_cursor(self.item_parent)
            self.main_layout.show_item()

    def open_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical')

        button_box = BoxLayout(orientation='vertical')
        change_user_button = Button(
            text=extraFunctions.reverse_string("החלף משתמש"),
            base_direction="rtl",
            font_name="Arial.ttf",
            halign="right"
        )

        reset_instance_button = Button(
            text=extraFunctions.reverse_string(RESET + " " + self.main_layout.cursor_name),
            base_direction="rtl",
            font_name="Arial.ttf",
            halign="right",
            on_press=self.on_press_reset_instance_button
        )

        close_button = Button(
            text=extraFunctions.reverse_string(CLOSE),
            base_direction="rtl",
            font_name="Arial.ttf",
            halign="right"
        )

        close_button.bind(on_press=lambda x: popup.dismiss())
        button_box.add_widget(change_user_button)
        button_box.add_widget(reset_instance_button)
        button_box.add_widget(close_button)
        popup_layout.add_widget(button_box)

        popup = Popup(title='', content=popup_layout, size_hint=(0.4, 0.4),
                      background='', border=(0, 0, 0, 0), separator_height=0)
        popup.open()

    def on_press_reset_instance_button(self, instance):
        def heavy_task(dt):
            start_time = time.time()
            database.reset_item(self.main_layout.cursor_id)

            elapsed_time = time.time() - start_time
            remaining_time = max(5 - elapsed_time, 0)  # Calculate the remaining time to reach 5 seconds
            time.sleep(remaining_time)
            Clock.schedule_once(lambda x: self.main_layout.show_item())

        thread = threading.Thread(target=lambda: heavy_task(None))  # Pass None or any desired value
        thread.start()


class BottomPartLetterGame(BoxLayout):
    def __init__(self, main_layout: MainLayout, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.main_layout = main_layout
        self.size_hint = [None, None]
        self.size = [Window.width, Window.height * 0.09]

        self.item_id = main_layout.cursor_id
        self.item_name = main_layout.cursor_name
        self.item_grade = main_layout.cursor_grade
        self.item_parent = main_layout.cursor_parent

    def __str__(self):
        if hasattr(self, 'item_id'):
            return f'Bottom part, item: {self.item_id}'
        else:
            return "Bottom part"

    def __repr__(self):
        if hasattr(self, 'item_id'):
            return f'Bottom part, item: {self.item_id}'
        else:
            return "Bottom part"


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
LETTER GAME
------------------------------------------------------------------------------------------------------------------------
"""


class LetterGameTextInput(HebrewTextInput):  # add given mishna because it has main layout in it!
    def __init__(self, main_layout: MainLayout, game, mishna_id, text, next_w=None, is_first_letter=True, **kwargs):
        if len(text) == 0:
            raise Exception("text length is 0")
        super().__init__(**kwargs)
        self.main_layout = main_layout
        self.mishna_id = mishna_id
        self.is_first_letter = is_first_letter
        if self.is_first_letter:
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

        self.readonly = True
        self.disabled = True
        self.disabled_foreground_color = get_color_from_hex('#0000FF')
        self.process_on_text = True

    def on_text(self, instance, value):
        if self.process_on_text:
            value = value[::-1]
            if not extraFunctions.is_sub_str_from_start(value, self.target_text):
                self.decide_mistake()
            elif value == self.target_text or extraFunctions.is_hebrew_characters_complete(value, self.target_text):
                self.lock(False)
            else:
                pass
        else:
            self.process_on_text = True

    def lock(self, is_fail: bool):
        self.process_on_text = False
        self.readonly = True
        self.disabled = True
        self.text = self.target_text[::-1]
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
            self.next.readonly = False
            self.next.disabled = False
            self.parent.parent.parent.scroll_to_widget(self.next)
            Clock.schedule_once(lambda dt: self.focus_on_next_widget(), 0.1)

        else:
            grade = int((self.game.words_right / self.game.total_words) * 100)
            if self.is_first_letter:
                database.update_test_1(self.mishna_id, grade)
            else:
                database.update_test_2(self.mishna_id, grade)

            self.finish_game()

    def focus_on_widget(self):
        self.focus = True

    def focus_on_next_widget(self):
        self.next.focus = True

    def decide_mistake(self):
        self.readonly = True
        self.disabled = True

        was_right_button = Button(
            text=I_KNEW_THE_ANSWER[::-1],
            background_normal='',
            background_color=get_color_from_hex("#10dc40"),
            color=get_color_from_hex("#000000"),
            font_name="Arial.ttf",
            on_press=self.on_was_right_button_press)

        was_wrong_button = Button(
            text=I_WAS_WRONG[::-1],
            background_normal='',
            background_color=get_color_from_hex("#ff033e"),
            color=get_color_from_hex("#ffffff"),
            font_name="Arial.ttf",
            on_press=self.on_was_wrong_button_press)

        self.main_layout.bottom_part.add_widget(was_right_button)
        self.main_layout.bottom_part.add_widget(was_wrong_button)

    def on_was_right_button_press(self, instance):
        self.main_layout.bottom_part.clear_widgets()
        self.lock(False)

    def on_was_wrong_button_press(self, instance):
        self.main_layout.bottom_part.clear_widgets()
        self.lock(True)

    def finish_game(self):
        self.readonly = True
        self.disabled = True

        finish_button = Button(
            text=FINISH_GAME[::-1],
            background_normal='',
            background_color=get_color_from_hex("#10dc40"),
            color=get_color_from_hex("#000000"),
            font_name="Arial.ttf",
            on_press=self.on_finish_button_press)

        self.main_layout.bottom_part.add_widget(finish_button)

    def on_finish_button_press(self, instance):
        self.main_layout.show_item()


class LetterGame(BoxLayout):
    def __init__(self, main_layout: MainLayout, mishna_id, mishna_text, scroll_view, is_first_letter, **kwargs):

        # init operations
        super().__init__(orientation='vertical', **kwargs)
        self.main_layout = main_layout
        self.mishna_id = mishna_id
        self.scroll_view = scroll_view
        self.words_right = 0
        self.total_words = 0
        self.widgets = []

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
                    prev_widget = LetterGameTextInput(self.main_layout,
                                                      self, mishna_id,
                                                      str_1,
                                                      None,
                                                      is_first_letter)
                    widgets_new_line.append(prev_widget)
                else:
                    prev_widget = LetterGameTextInput(self.main_layout,
                                                      self,
                                                      mishna_id,
                                                      str_1,
                                                      prev_widget,
                                                      is_first_letter)
                    widgets_new_line.append(prev_widget)
                col_counter += 1
            reversed_widgets_matrix.append(widgets_new_line)
            line_counter += 1

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

        self.widgets[0][-1].readonly = False
        self.widgets[0][-1].disabled = False

    def on_parent(self, *args):
        if self.parent is not None:
            Clock.schedule_once(lambda dt: self.widgets[0][-1].focus_on_widget(), 0.5)
            self.scroll_view.scroll_to_widget(self.widgets[0][-1])


class LetterGamePanel(ScrollView):
    def __init__(self, main_layout: MainLayout, mishna_id, mishna_text: str, is_first_letter=True, **kwargs):
        super(LetterGamePanel, self).__init__(**kwargs)
        self.game = LetterGame(main_layout, mishna_id, mishna_text, self, is_first_letter)
        self.main_layout = main_layout
        self.mishna_id = mishna_id
        self.mishna_text = mishna_text
        self.add_widget(self.game)
        self.always_overscroll = True
        self.scroll_x = 1

    def scroll_to_widget(self, widget):
        self.scroll_to(widget)


"""
------------------------------------------------------------------------------------------------------------------------
READ OUT LOUD GAME
------------------------------------------------------------------------------------------------------------------------
"""


class TimerWidget(BoxLayout):
    def __init__(self, main_layout: MainLayout, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (1, 0.2)

        # Add timer container with desired width and centered alignment
        timer_container = BoxLayout(size_hint=(0.1, None), height=dp(40), pos_hint={'center_x': 0.5})
        timer_container.add_widget(self._create_timer_box())
        self.add_widget(timer_container)
        self.main_layout = main_layout
        self.add_widget(Widget())

        # Add bottom part with centered button
        button_text = IM_DONE[::-1]
        self.button = Button(
            text=button_text,
            background_normal='',
            background_color=(1, 0.5, 0, 1),
            color=(0, 0, 0.5, 1),
            opacity=0,
            disabled=True,
            size_hint=(0.3, 0.15),
            font_name="Arial.ttf",
            on_press=self.on_press
        )

        self.duration = timedelta(minutes=READ_OUT_LOUD_TIME)
        self.start_time = datetime.now()
        Clock.schedule_interval(self.update_timer, 0.1)

    def _create_timer_box(self):
        timer_box = BoxLayout()
        with timer_box.canvas.before:
            Color(1, 0.5, 0, 1)
            self.rect = Rectangle(size=timer_box.size, pos=timer_box.pos)
        timer_box.bind(size=self._update_rect, pos=self._update_rect)
        self.timer_label = Label(text='2:00', font_size='20sp', color=(0, 0, 0.5, 1))
        timer_box.add_widget(self.timer_label)
        return timer_box

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_timer(self, dt):
        elapsed = datetime.now() - self.start_time
        remaining = self.duration - elapsed
        if remaining <= timedelta(seconds=0):
            remaining = timedelta(seconds=0)
            self.button.opacity = 1
            self.button.disabled = False
        minutes, seconds = divmod(remaining.seconds, 60)
        if remaining <= timedelta(seconds=10):
            self.timer_label.color = (1, 0, 0, 1)  # red color for last 10 seconds
        self.timer_label.text = '%02d:%02d' % (minutes, seconds)

    def on_press(self, instance):
        database.update_test_0(self.main_layout.cursor_id, 100)
        self.main_layout.show_item()


class ReadOutLoudGame(BoxLayout):
    def __init__(self, main_layout: MainLayout, mishna_id, mishna_text, scroll_view, **kwargs):

        # init operations
        super().__init__(orientation='vertical', **kwargs)
        self.main_layout = main_layout
        self.mishna_id = mishna_id
        self.scroll_view = scroll_view
        self.font_name = "Arial.ttf"
        self.font_size = 35

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
        for line in reversed(str_matrix):
            widgets_new_line = []
            for str_1 in line:
                game_label = ReadOutLoudGameLabel(str_1)
                game_label.size = (extraFunctions.get_text_size(str_1, self.font_name, self.font_size)[0] + 12,
                                   extraFunctions.get_text_size(str_1, self.font_name, self.font_size)[1] + 15)
                widgets_new_line.append(game_label)
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


class ReadOutLoudGamePanel(ScrollView):
    def __init__(self, main_layout: MainLayout, mishna_id, mishna_text: str, **kwargs):
        super(ReadOutLoudGamePanel, self).__init__(**kwargs)
        self.game = ReadOutLoudGame(main_layout, mishna_id, mishna_text, self)
        self.main_layout = main_layout
        self.mishna_id = mishna_id
        self.mishna_text = mishna_text
        self.add_widget(self.game)
        self.always_overscroll = True
        self.scroll_x = 1


class ReadOutLoudGameLabel(TextInput):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.is_reversed = False
        self.last_value = ""
        self.base_direction = "rtl"
        self.font_name = "Arial.ttf"
        self.halign = "right"
        self.text = text[::-1]
        self.readonly = True
        self.focus = False
        self.disabled = True
        self.font_size = 35
        self.disabled_foreground_color = get_color_from_hex('#0000FF')
        self.size_hint = (None, None)
        self.background_disabled_normal = ""
        self.background_color = [0, 0, 0, 1]

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text
