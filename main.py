from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from login import LoginScreen
from menu import UserMenu
from new_survey import NewSurvey
from survey_questions import SurveyQuestions
from sync import SyncScreen

class SurveyApp(App):
    def build(self):

        # Establecer propiedades por defecto para todos los Labels
        Label.font_size = '24'
        Label.color = (0.15, 0.6, 0.85, 1)

        # Establecer propiedades por defecto para todos los Buttons
        Button.font_size = '20'
        Button.background_color = (0.65, 0.65, 0.65, 1)

        # Background
        Window.clearcolor = (1, 1, 1, 1)

        sm = ScreenManager()

        # Agrega las pantallas al ScreenManager sin pasar el argumento 'name'
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(UserMenu(name='user_menu'))
        sm.add_widget(NewSurvey(name='new_survey'))
        sm.add_widget(SurveyQuestions(name='survey_questions'))
        sm.add_widget(SyncScreen(name='sync'))

        return sm

if __name__ == "__main__":
    SurveyApp().run()
