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
import datetime

class SyncScreen(Screen):

    def __init__(self, **kwargs):
        super(SyncScreen, self).__init__(**kwargs)

        # Main layout
        layout = BoxLayout(orientation='vertical')
        layout.padding = [50, 50]

        # Status label
        self.status_label = Label(text="Presione 'Iniciar' para comenzar la sincronización.")
        layout.add_widget(self.status_label)

        # Start sync button
        sync_button = Button(text='Iniciar', size_hint_y=None, height=50)
        sync_button.bind(on_press=self.start_sync)
        layout.add_widget(sync_button)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        # Back to menu button
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

    def check_internet_connection(self) -> bool:
        try:
            response = requests.get("https://www.google.com/", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def start_sync(self, instance):
        if not self.check_internet_connection():
            self.status_label.text = "Sin conexión a internet. \nPor favor, conecte y vuelva a intentarlo."
            return

        self.status_label.text = "Sincronización en curso, por favor espere..."
        token = keyring.get_password("relevamientos_app", "usuario_token")
        url = "https://api-encuestas-mds.unaj.edu.ar/create"
        headers = {'Authorization': 'Bearer ' + token}
        all_synced = True  # Flag to check if all surveys were synced successfully

        # Iterate over each completed survey
        for survey in self.read_all_surveys_from_file():
            survey_send = {"type": 1, "answers": survey}
            response = requests.post(url, json=survey_send, headers=headers)
            # Verify status
            if response.status_code != 201:
                all_synced = False  # Set the flag to False if there was an error
                self.status_label.text = "Error response " + str(response.status_code) + ":\n" + response.text
                break

        # If all surveys were synced successfully, rename the json
        if all_synced:
            self.status_label.text = "Sincronización completada"
            file_path = 'completed_surveys.json'
            backup_file_path = 'backup_' + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.json'
            os.rename(file_path, backup_file_path)

    def back_to_menu(self, instance):
        app = App.get_running_app()
        app.root.current = 'user_menu'