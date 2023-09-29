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
import hashlib

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
            height=100,
            keep_ratio=True,
            allow_stretch=True
        )
        layout.add_widget(img)
        layout.add_widget(Widget(size_hint_y=None, height=150))

        # Label
        self.welcome_label = Label(
            text='Aplicación de relevamientos',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.welcome_label)
        layout.add_widget(Widget(size_hint_y=None, height=50))


        # User and Password Input
        self.username = TextInput(
            hint_text='Nombre de usuario',
            size_hint_y=None,
            height=30
        )

        self.password = TextInput(
            hint_text='Contraseña',
            password=True,
            size_hint_y=None,
            height=30
        )

        layout.add_widget(self.username)
        layout.add_widget(self.password)

        # Login Button
        btn_login = Button(
            text='Iniciar sesión',
            size_hint_y=None,
            height=50
        )
        btn_login.bind(on_press=self.comprobando_usuario)
        layout.add_widget(btn_login)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        self.add_widget(layout)


    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def check_internet_connection(self) -> bool:
        try:
            response = requests.get("https://www.google.com/", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def comprobando_usuario(self, instance):
        username = self.username.text
        password = self.password.text
        self.welcome_label.text = 'Comprobando usuario y contraseña...'

        has_internet = self.check_internet_connection()
        if has_internet:
            # Online logic

            url = "https://api-encuestas-mds.unaj.edu.ar/login"
            data = {'username': username, 'password': password}
            response = requests.post(url, json=data)

            # Verify status
            if response.status_code == 200:
                self.welcome_label.text = 'Login online exitoso'
                # Save hashed credentials locally after successful online login
                hashed_username = self.hash_password(username)
                hashed_password = self.hash_password(password)
                keyring.set_password("relevamientos_app", "hashed_username", hashed_username)
                keyring.set_password("relevamientos_app", "hashed_password", hashed_password)
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
        else:
            # Offline login logic
            self.welcome_label.text = 'Login offline exitoso'
            saved_hashed_username = keyring.get_password("relevamientos_app", "hashed_username")
            saved_hashed_password = keyring.get_password("relevamientos_app", "hashed_password")

            if saved_hashed_username == self.hash_password(username) and saved_hashed_password == self.hash_password(
                    password):
                app = App.get_running_app()
                app.root.current = 'user_menu'
            else:
                self.welcome_label.text = 'Usuario o contraseña incorrectos en modo offline'
