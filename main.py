from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager
from login import LoginScreen
from menu import UserMenu
from new_survey import NewSurvey
from survey_questions import SurveyQuestions
from sync import SyncScreen
from kivy.properties import NumericProperty
from kivy.metrics import sp, dp

class SurveyApp(App):
    def build(self):
        scaled_font_size = sp(18)

        # Labels default properties
        Label.font_size = scaled_font_size
        Label.color = (0.15, 0.6, 0.85, 1)

        # Buttons default properties
        Button.font_size = scaled_font_size
        Button.background_color = (0.65, 0.65, 0.65, 1)
        Button.size_hint_x = 0.5
        Button.pos_hint = {'center_x': 0.5}

        # Buttons default properties
        TextInput.font_size = NumericProperty(scaled_font_size)
        TextInput.size_hint_y = None

        # Spinner default properties
        Spinner.font_size = NumericProperty(scaled_font_size)
        Spinner.background_color = (0.65, 0.65, 0.65, 1)
        Spinner.size_hint_x = 0.5
        Spinner.pos_hint = {'center_x': 0.5}

        # Background
        Window.clearcolor = (1, 1, 1, 1)

        sm = ScreenManager()

        # Create screens
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(UserMenu(name='user_menu'))
        sm.add_widget(NewSurvey(name='new_survey'))
        sm.add_widget(SurveyQuestions(name='survey_questions'))
        sm.add_widget(SyncScreen(name='sync'))

        return sm

if __name__ == "__main__":
    SurveyApp().run()
