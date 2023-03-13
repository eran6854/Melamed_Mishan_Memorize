from kivy.uix.label import Label
from kivy.core.window import Window


def pixels_to_relative_size(pixels):
    window_size = Window.size
    if window_size[0] == 0 and window_size[1] == 0:
        return 0
    else:
        return pixels / window_size[0], pixels / window_size[0]


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


if __name__ == '__main__':
    str1 = "א"
    str2 = "את"
    print(is_hebrew_characters_complete(str2, str1))

