from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.metrics import dp
from datetime import datetime, timedelta
from kivy.graphics import Color, Rectangle


class ReadOutLoudGamePanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Add timer container with desired width and centered alignment
        timer_container = BoxLayout(size_hint=(0.6, None), height=dp(40), pos_hint={'center_x': 0.5})
        timer_container.add_widget(self._create_timer_box())
        self.add_widget(timer_container)

        self.add_widget(Widget())

        # Add bottom part with centered button
        bottom_box = BoxLayout(orientation='horizontal', size_hint=(1, 1))
        bottom_box.add_widget(Widget(size_hint=(0.3, 0.15)))
        self.button = Button(
            text='Click Me!',
            background_normal='',
            background_color=(1, 0.5, 0, 1),
            color=(0, 0, 0.5, 1),
            opacity=0,
            disabled=True,
            size_hint=(0.4, 0.15)
        )
        bottom_box.add_widget(self.button)
        bottom_box.add_widget(Widget(size_hint=(0.3, 0.15)))
        self.add_widget(bottom_box)

        self.duration = timedelta(minutes=0.1)
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


class MyApp(App):
    def build(self):
        return ReadOutLoudGamePanel()


if __name__ == '__main__':
    MyApp().run()
