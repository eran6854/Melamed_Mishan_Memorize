import speech_recognition as spr

r = spr.Recognizer()

with spr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("say something...")

    audio = r.listen(source)

    try:
        print("you have said: \n" + r.recognize_google(audio, language="he-HE"))
    except Exception as e:
        print(str(e))
