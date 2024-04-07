from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.widget import Widget


class UserMenu(Screen):

    def __init__(self, **kwargs):
        super(UserMenu, self).__init__(**kwargs)
        self.completed_surveys = []
        # Create a main BoxLayout
        layout = BoxLayout(orientation='vertical')
        layout.padding = [50, 50]

        # Label
        self.label = Label(text=f'Seleccione una tarea')
        layout.add_widget(self.label)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        # Button to start survey
        btn_start_survey = Button(text='Realizar encuesta')
        btn_start_survey.bind(on_press=self.realizar_encuesta)
        layout.add_widget(btn_start_survey)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        # Button to sync database
        btn_sync_db = Button(text='Sincronizar con la base de datos')
        btn_sync_db.bind(on_press=self.sincronizar_bd)
        layout.add_widget(btn_sync_db)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        self.add_widget(layout)

    def realizar_encuesta(self, instance):
        app = App.get_running_app()
        app.root.current = 'new_survey'

    def sincronizar_bd(self, instance):
        app = App.get_running_app()
        app.root.current = 'sync'
