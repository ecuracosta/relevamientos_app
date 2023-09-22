from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
import time
from kivy.uix.widget import Widget

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

        self.add_widget(layout)

    def start_sync(self, instance):
        # Actualizar el estado
        self.status_label.text = "Sincronización en curso..."

        # Recuperar el token
        token = keyring.get_password("relevamientos_app", "usuario_token")
        # URL de la API
        url = "https://api-encuestas-mds.unaj.edu.ar/create"
        # ACA VA UN for
        # Datos que deseas enviar en el cuerpo de la solicitud POST
        data = {'type': 1, "answers": {"A2": "1"}}
        headers = {'Authorization': 'Bearer ' + token}
        # Realiza la solicitud POST utilizando requests
        response = requests.post(url, json=data, headers=headers)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            print('Solicitud POST exitosa')
            # Establecer y guardar el token
            keyring.set_password("relevamientos_app", "usuario_token", response.text["token"])
        elif response.status_code == 401:
            pass  # TOKEN VENCIDO
        else:
            print('Error en la solicitud POST:', response.status_code)
        print(response.text)

        # Actualizar el estado
        self.status_label.text = "Sincronización completada."

        # Simulación de una operación de 3 segundos
        time.sleep(3)

        app = App.get_running_app()
        app.root.current = 'user_menu'