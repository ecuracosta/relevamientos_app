from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.widget import Widget
import keyring
import requests
import json


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Main Layout
        layout = BoxLayout(orientation='vertical')
        layout.padding = [50, 50]

        # Logo
        img = Image(
            source='logo.png',
            size_hint_y=None,
            height=100,  # Establece la altura que consideres apropiada
            keep_ratio=True,
            allow_stretch=True
        )
        layout.add_widget(img)
        layout.add_widget(Widget(size_hint_y=None, height=150))

        # Label
        self.welcome_label = Label(
            text='Aplicación de relevamientos',
            size_hint_y=None,
            height=50  # Establece la altura que consideres apropiada
        )
        layout.add_widget(self.welcome_label)
        layout.add_widget(Widget(size_hint_y=None, height=50))


        # User and Password Input
        self.username = TextInput(
            hint_text='Nombre de usuario',
            size_hint_y=None,
            height=30  # Establece la altura que consideres apropiada
        )

        self.password = TextInput(
            hint_text='Contraseña',
            password=True,
            size_hint_y=None,
            height=30  # Establece la altura que consideres apropiada
        )

        layout.add_widget(self.username)
        layout.add_widget(self.password)

        # Login Button
        btn_login = Button(
            text='Iniciar sesión',
            size_hint_y=None,
            height=50  # Establece la altura que consideres apropiada
        )
        btn_login.bind(on_press=self.comprobando_usuario)
        layout.add_widget(btn_login)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        self.add_widget(layout)






    def comprobando_usuario(self, instance):
        print("comprobando")
        username = self.username.text
        password = self.password.text
        self.welcome_label.text = 'Comprobando usuario y contraseña...'

        # URL de la API
        url = "https://api-encuestas-mds.unaj.edu.ar/login"

        # Datos que deseas enviar en el cuerpo de la solicitud POST
        data = {'username': username, 'password': password}

        # Realiza la solicitud POST utilizando requests
        response = requests.post(url, json=data)

        # Verifica el código de estado de la respuesta
        print(response.text)
        if response.status_code == 200:
            self.welcome_label.text = 'Solicitud POST exitosa'
            json_token = json.loads(response.text)
            if "token" in json_token:
                keyring.set_password("relevamientos_app", "usuario_token", json_token["token"])
                app = App.get_running_app()
                app.root.current = 'user_menu'
            else:
                self.welcome_label.text = json_token["error"]
        elif response.status_code == 401:
            self.welcome_label.text = 'Token vencido'
        elif response.status_code == 400:
            self.welcome_label.text = 'Constraseña incorrecta'
        else:
            self.welcome_label.text = 'Error en la solicitud POST: ' + str(response.status_code)
