from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.widget import Widget

class NewSurvey(Screen):
    menu_usuario = None

    def __init__(self, **kwargs):
        super(NewSurvey, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.padding = [50, 50]

        self.add_widget(layout)

        layout.add_widget(Label(text='Ingrese el domicilio'))
        layout.add_widget(Widget(size_hint_y=None, height=50))

        self.address_input = TextInput(hint_text='Dirección', multiline=False)
        layout.add_widget(self.address_input)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        btn = Button(text='Iniciar encuesta', size_hint_y=None, height=50)
        btn.bind(on_press=self.abrir_encuesta)
        layout.add_widget(btn)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        # Botón para usar el mismo domicilio que la encuesta anterior
        back_to_menu_btn = Button(text='Regresar al menu principal', size_hint_y=None, height=50)
        back_to_menu_btn.bind(on_press=self.back_to_menu)
        layout.add_widget(back_to_menu_btn)
        layout.add_widget(Widget(size_hint_y=None, height=50))

    def abrir_encuesta(self, instance):
        address = self.address_input.text
        app = App.get_running_app()
        survey_screen = app.root.get_screen('survey_questions')
        if not hasattr(survey_screen, 'responses'):
            survey_screen.responses = {}
        survey_screen.responses["0.0"] = address

        app.root.current = 'survey_questions'

    def back_to_menu(self, instance):
        app = App.get_running_app()
        app.root.current = 'user_menu'

