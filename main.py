from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock  # Importa Clock

class InicioPantalla(BoxLayout):
    def comprobando_usuario(self, username, password):
        self.ids.welcome_label.text = 'Comprobando usuario y contraseña...'
        Clock.schedule_once(lambda dt: self.login(username, password), 2)

    def login(self, username, password):
        if username in usuarios and password == usuarios[username]['password']:
            self.clear_widgets()
            self.add_widget(MenuUsuario(username=username))
        else:
            self.ids.username.text = ''
            self.ids.password.text = ''

class MenuUsuario(BoxLayout):
    username = StringProperty('')
    encuestas_realizadas = NumericProperty(0)
    encuestas_restantes = NumericProperty(3)

    def __init__(self, username, **kwargs):
        super(MenuUsuario, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.username = username

    def mostrar_pantalla_sincronizacion(self):
        sync_screen = SyncScreen()
        self.clear_widgets()
        self.add_widget(sync_screen)
        Clock.schedule_once(lambda dt: self.ocultar_pantalla_sincronizacion(), 2)

    def ocultar_pantalla_sincronizacion(self):
        self.clear_widgets()
        self.add_widget(MenuUsuario(username=self.username))

    def realizar_encuesta(self):
        seleccion_domicilio = SeleccionDomicilio(username=self.username)
        seleccion_domicilio.menu_usuario = self
        self.clear_widgets()
        self.add_widget(seleccion_domicilio)

    def sincronizar_bd(self):
        # lógica para sincronizar con la base de datos.
        pass

class EncuestaApp(App):
    def build(self):
        inicio_pantalla = InicioPantalla()
        return inicio_pantalla

class Encuesta:
    preguntas = [
        '¿Pregunta 1?',
        '¿Pregunta 2?',
        '¿Pregunta 3?'
    ]

class SeleccionDomicilio(BoxLayout):
    menu_usuario = None

    def __init__(self, username, **kwargs):

        super(SeleccionDomicilio, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.username = username
        self.add_widget(Label(text=f'Bienvenido {username}'))
        
        for domicilio in usuarios[username]['domicilios']:
            btn = Button(text=domicilio)
            btn.bind(on_press=self.abrir_encuesta)
            self.add_widget(btn)

    def abrir_encuesta(self, instance):
        domicilio = instance.text
        self.clear_widgets()
        self.add_widget(PreguntasEncuesta(preguntas=Encuesta.preguntas, domicilio=domicilio))

class PreguntasEncuesta(BoxLayout):
    preguntas = ListProperty([])
    domicilio = StringProperty('')
    pregunta_actual = NumericProperty(0)

    def on_pregunta_actual(self, instance, value):
        self.ids.pregunta_label.text = self.preguntas[value]

    def avanzar_pregunta(self):
        if self.pregunta_actual < len(self.preguntas) - 1:
            self.pregunta_actual += 1
        else:
            seleccion_domicilio = self.parent
            seleccion_domicilio.clear_widgets()
            seleccion_domicilio.add_widget(FinEncuesta(username=seleccion_domicilio.username))


    def finalizar_encuesta(self):
        seleccion_domicilio = self.parent
        seleccion_domicilio.clear_widgets()
        seleccion_domicilio.add_widget(FinEncuesta(username=seleccion_domicilio.username))


    def seleccionar_opcion(self, opcion):
        # lógica para manejar la respuesta seleccionada.
        pass

class FinEncuesta(BoxLayout):
    username = StringProperty('')

    def __init__(self, username, **kwargs):
        super(FinEncuesta, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.username = username
        self.add_widget(Label(text=f'Encuesta finalizada para el usuario {username}'))
        btn = Button(text='Volver al menú')
        btn.bind(on_press=self.volver_al_menu)
        self.add_widget(btn)

    def volver_al_menu(self, *args):
        seleccion_domicilio = self.parent
        seleccion_domicilio.clear_widgets()
        seleccion_domicilio.add_widget(MenuUsuario(username=self.username))

usuarios = {
    'admin': {
        'password': 'admin',
        'domicilios': [
            'Domicilio 1',
            'Domicilio 2',
            'Domicilio 3',
        ]
    },
    'usuario': {
        'password': '1234',
        'domicilios': [
            'Domicilio 4',
            'Domicilio 5',
            'Domicilio 6',
        ]
    }
}

class SyncScreen(BoxLayout):
    pass

Builder.load_file('estilo.kv')

if __name__ == '__main__':
    EncuestaApp().run()
