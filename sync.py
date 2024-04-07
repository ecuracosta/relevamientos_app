from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
import requests
import os
import json
import datetime
from jnius import autoclass

SharedPreferences = autoclass('android.content.SharedPreferences')
Context = autoclass('android.content.Context')

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
        sync_button = Button(text='Iniciar')
        sync_button.bind(on_press=self.start_sync)
        layout.add_widget(sync_button)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        # Delete surveys button
        delete_button = Button(text='Borrar relevamientos')
        delete_button.bind(on_press=self.confirm_delete)
        layout.add_widget(delete_button)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        # Back to menu button
        back_button = Button(text='Regresar al menu principal')
        back_button.bind(on_press=self.back_to_menu)
        layout.add_widget(back_button)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        self.add_widget(layout)

    def confirm_delete(self, instance):
        # Create a confirmation popup
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='¿Está seguro de que desea borrar los relevamientos?'))
        yes_button = Button(text='Sí', size_hint_y=None, height=50)
        yes_button.bind(on_press=self.delete_surveys)
        no_button = Button(text='No', size_hint_y=None, height=50)
        no_button.bind(on_press=lambda x: self.popup.dismiss())
        button_layout = BoxLayout(size_hint_y=None, height=50)
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content.add_widget(button_layout)

        self.popup = Popup(title='Confirmación', content=content, size_hint=(0.8, 0.4))
        self.popup.open()

    def delete_surveys(self, instance):
        # Delete the surveys and close the popup
        file_path = 'completed_surveys.json'
        if os.path.exists(file_path):
            os.remove(file_path)
            self.status_label.text = 'Relevamientos borrados.'
        else:
            self.status_label.text = 'No hay relevamientos para borrar.'
        self.popup.dismiss()

    def get_preferences(self):
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        return activity.getSharedPreferences("relevamientos_app", Context.MODE_PRIVATE)

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
        prefs = self.get_preferences()
        token = prefs.getString("usuario_token", None)
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
