from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
import json
import os
from kivy.uix.widget import Widget

class SurveyQuestions(Screen):
    def __init__(self, **kwargs):
        super(SurveyQuestions, self).__init__(**kwargs)
        self.responses = {}

        # Create a main BoxLayout to add to the Screen
        self.main_layout = BoxLayout(orientation='vertical')
        self.main_layout.padding = [50, 50]

        self.add_widget(self.main_layout)

        # Cargamos las preguntas y respuestas
        with open('questions.json', 'r') as f:
            self.questions = json.load(f)

        with open('answers.json', 'r') as f:
            self.answers = json.load(f)

        with open('conditions.json', 'r') as f:
            self.conditions = json.load(f)

        self.current_question_key = None
        self.question_keys = list(self.questions.keys())
        self.current_index = 0

        self.show_question(self.current_index)

    def show_question(self, index):
        self.main_layout.clear_widgets()

        if index < 0 or index >= len(self.question_keys):
            return

        # Check if the current question has any conditions
        question_key = self.question_keys[index]
        if question_key in self.conditions:
            condition = self.conditions[question_key]
            dependent_question_key = condition["depends_on"]
            if dependent_question_key in self.responses:
                dependent_answer = self.responses[dependent_question_key]
                if self.answers[dependent_question_key][dependent_answer] not in condition["value"]:
                    # Skip this question and move to the next one
                    self.current_index += 1
                    if self.current_index < len(self.question_keys):
                        self.show_question(self.current_index)
                    return

        self.current_question_key = self.question_keys[index]
        self.current_index = index

        question_layout = BoxLayout(orientation='vertical')
        question_layout.add_widget(Label(text=self.questions[self.current_question_key]))
        self.main_layout.add_widget(Widget(size_hint_y=None, height=50))

        if self.answers[self.current_question_key]:
            self.spinner_values_keys = list(self.answers[self.current_question_key].keys())
            self.spinner_values = [str(val) for val in self.answers[self.current_question_key].values()]
            self.spinner = Spinner(text='Seleccione una opción', values=self.spinner_values)
            question_layout.add_widget(self.spinner)
        else:
            self.text_input = TextInput(hint_text='Ingrese su respuesta', multiline=False)
            question_layout.add_widget(self.text_input)
        self.main_layout.add_widget(Widget(size_hint_y=None, height=50))

        self.main_layout.add_widget(question_layout)

        button_layout = BoxLayout()

        prev_button = Button(text='Anterior', size_hint_y=None, height=50)
        prev_button.bind(on_press=self.prev_question)
        button_layout.add_widget(prev_button)
        self.main_layout.add_widget(Widget(size_hint_x=None, width=50))

        next_button = Button(text='Siguiente', size_hint_y=None, height=50)
        next_button.bind(on_press=self.next_question)
        button_layout.add_widget(next_button)
        self.main_layout.add_widget(Widget(size_hint_x=None, width=50))

        finish_button = Button(text='Finalizar', size_hint_y=None, height=50)
        finish_button.bind(on_press=self.finish_survey)
        button_layout.add_widget(finish_button)

        self.main_layout.add_widget(button_layout)
        self.main_layout.add_widget(Widget(size_hint_x=None, width=50))

    def next_question(self, instance):
        self.store_response()
        if self.responses[self.current_question_key]:
            self.current_index += 1
            if self.current_index >= len(self.question_keys):
                self.finish_survey(instance)
            else:
                self.show_question(self.current_index)

    def prev_question(self, instance):
        self.store_response()
        self.current_index -= 1
        self.show_question(self.current_index)

    def store_response(self):
        if self.answers[self.current_question_key]:
            try:
                selected_index = self.spinner_values.index(self.spinner.text)
                selected_key = self.spinner_values_keys[selected_index]
                self.responses[self.current_question_key] = selected_key
            except ValueError:
                self.responses[self.current_question_key] = None
        else:
            self.responses[self.current_question_key] = self.text_input.text

    def append_survey_to_file(self, data):
        file_path = 'completed_surveys.json'
        all_surveys = []

        # Check if the file already exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                all_surveys = json.load(file)

        all_surveys.append(data)

        # Always write the updated data back to the file
        with open(file_path, 'w') as file:
            json.dump(all_surveys, file, indent=4)

    def finish_survey(self, instance):
        self.store_response()
        self.append_survey_to_file(self.responses)
        app = App.get_running_app()
        user_menu_screen = app.root.get_screen('user_menu')
        user_menu_screen.completed_surveys.append(self.responses)
        self.responses.clear()
        app.root.current = 'new_survey'

    def on_enter(self):
        self.current_index = 0
        self.show_question(self.current_index)
