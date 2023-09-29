from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.widget import Widget
import requests
import keyring
import os
import json

class SyncScreen(Screen):

    def __init__(self, **kwargs):
        super(SyncScreen, self).__init__(**kwargs)

        # Layout principal
        layout = BoxLayout(orientation='vertical')
        layout.padding = [50, 50]

        # Label para mostrar el estado
        self.status_label = Label(text="Presione 'Iniciar' para comenzar la sincronización.")
        layout.add_widget(self.status_label)

        # Botón para iniciar la sincronización
        sync_button = Button(text='Iniciar', size_hint_y=None, height=50)
        sync_button.bind(on_press=self.start_sync)
        layout.add_widget(sync_button)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        # Botón para volver al menu
        sync_button = Button(text='Regresar al menu principal', size_hint_y=None, height=50)
        sync_button.bind(on_press=self.back_to_menu)
        layout.add_widget(sync_button)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        self.add_widget(layout)

    def read_all_surveys_from_file(self):
        file_path = 'completed_surveys.json'

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return []

    def start_sync(self, instance):
        # Actualizar el estado
        self.status_label.text = "Sincronización en curso, por favor espere..."

        # Recuperar el token
        token = keyring.get_password("relevamientos_app", "usuario_token")
        # URL de la API
        url = "https://api-encuestas-mds.unaj.edu.ar/create"
        # Headers
        headers = {'Authorization': 'Bearer ' + token}

        # Iterate over each completed survey
        for survey in self.read_all_surveys_from_file():
            # Realiza la solicitud POST utilizando requests
            survey_send = {"type": 1, "answers": survey}
            response = requests.post(url, json=survey_send, headers=headers)
            # Verifica el código de estado de la respuesta
            if response.status_code == 201:
                self.status_label.text = "Sincronización completada"
            else:
                json_response = json.loads(response.text)
                self.status_label.text = "Error response " + str(response.status_code) + ":\n" + json_response["error"]

    def back_to_menu(self, instance):
        app = App.get_running_app()
        app.root.current = 'user_menu'