from kivy.uix.label import Label
from kivy.core.window import Window
from mishnayotText import berakhot_1_1_text
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from re import compile

def pixels_to_relative_size(pixels, size_to_relate):
    if size_to_relate[0] == 0 or size_to_relate[1] == 0:
        return 0
    else:
        return float(pixels / size_to_relate[0]), float(pixels / size_to_relate[1])


def reverse_string(string: str) -> str:
    return string[::-1]


def is_sub_str_from_start(sub: str, org: str) -> bool:
    if len(sub) > len(org):
        return False
    if sub == org[:len(sub)]:
        return True
    return False


def is_hebrew_letter(char: str) -> bool:
    # Check if the character is in the Hebrew letters Unicode range
    return 1488 <= ord(char) <= 1514


def is_hebrew_characters_complete(sub: str, org: str) -> bool:
    if sub == org[:-1] and not is_hebrew_letter(org[-1]):
        return True
    else:
        return False


def get_text_relative_size(text, font_name, font_size):
    label = Label(text=text, font_name=font_name, font_size=font_size)
    label.texture_update()
    return label.texture_size[0] / float(Window.width), label.texture_size[1] / float(Window.height)


def get_text_size(text, font_name, font_size):
    # Create a new label with the given text and font properties
    label = Label(text=text, font_name=font_name, font_size=font_size, size_hint=(None, None))

    label.texture_update()

    # Get the texture size of the label (i.e. the size needed to display the text)
    texture_size = label.texture_size

    # Return the size as a tuple (width, height)
    return texture_size[0], texture_size[1]


def string_hebrew_to_matrix(s):
    # Split the string into lines
    lines = s.split('\n')
    # Split each line into words
    words = [line.split() for line in lines]
    words.pop(0)
    words.pop(-1)
    reversed_words = []
    for line in words:
        new_reversed_line = []
        for word in reversed(line):
            new_reversed_line.append(word)
        reversed_words.append(new_reversed_line)
    return reversed_words


def extract_hebrew_words(text):
    # Remove line breaks
    text = text.replace('\n', ' ')

    # Remove non-Hebrew characters and white spaces
    hebrew_regex = re.compile(r'[\u0590-\u05FF]+')
    words = hebrew_regex.findall(text)

    return words


def open_popup(instance):
    popup_layout = BoxLayout(orientation='vertical')

    button_box = BoxLayout(orientation='vertical')
    change_user_button = Button(text=reverse_string("החלף משתמש"),
                                base_direction="rtl",
                                font_name="Arial.ttf",
                                halign="right"
                                )

    settings_button = Button(text=reverse_string("הגדרות"),
                             base_direction="rtl",
                             font_name="Arial.ttf",
                             halign="right"
                             )

    close_button = Button(text=reverse_string("סגור"),
                          base_direction="rtl",
                          font_name="Arial.ttf",
                          halign="right"
                          )

    close_button.bind(on_press=lambda x: popup.dismiss())
    button_box.add_widget(change_user_button)
    button_box.add_widget(settings_button)
    button_box.add_widget(close_button)
    popup_layout.add_widget(button_box)

    popup = Popup(title='', content=popup_layout, size_hint=(0.4, 0.4),
                  background='', border=(0, 0, 0, 0), separator_height=0)
    popup.open()


if __name__ == '__main__':
    str1 = "א"
    str2 = "את"
    print(string_hebrew_to_matrix(berakhot_1_1_text))
