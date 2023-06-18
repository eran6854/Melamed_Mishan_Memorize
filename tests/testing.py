import re

def extract_hebrew_words(text):
    # Remove line breaks
    text = text.replace('\n', ' ')

    # Remove non-Hebrew characters and white spaces
    hebrew_regex = re.compile(r'[\u0590-\u05FF]+')
    words = hebrew_regex.findall(text)

    return words

# Example usage
input_text = '''
מאימתי קורין את שמע בשחרית?
משיכיר בין תכלת ללבן.
רבי אליעזר אומר: בין תכלת לכרתי,
וגומרה עד הנץ החמה.
רבי יהושע אומר: עד שלש שעות,
שכן דרך בני מלכים לעמוד בשלש שעות.
הקורא מכאן ואילך לא הפסיד, כאדם הקורא בתורה.
'''
output = extract_hebrew_words(input_text)
print(output)
