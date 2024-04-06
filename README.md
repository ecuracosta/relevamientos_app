# Relevamientos App

Relevamientos App is a survey application built using the Kivy framework. It allows users to perform surveys by selecting different domiciles and answering a set of predefined questions and answers.

<img src="https://github.com/ecuracosta/relevamientos_app/assets/47532757/90326d9e-6e37-44f2-89a2-dd5502878816" height="300" />

## Description

The Relevamientos App is designed to simplify the process of conducting surveys by providing an intuitive user interface. Users can log in with their username and password, enter a domicile and answer a series of survey questions. The app then can synchronize with a database to upload the survey results.

- `login.py`: Handles the user authentication process and token management for the application.
- `main.py`: Initializes the application and sets up the screen manager to switch between different screens.
- `menu.py`: Manages the main menu options, allowing the user to choose between starting a new survey or synchronize.
- `new_survey.py`: Handles the input of the domicile information and starts a new survey.
- `survey_questions.py`: Presents survey questions to the user and saves the responses to `completed_surveys.json`.
- `sync.py`: Synchronizes the completed surveys (`completed_surveys.json`) with a remote database.
- `questions.json`: Contains the survey questions to be presented to the user.
- `answers.json`: Contains the possible answers for each survey question.
- `conditions.json`: Defines the conditions under which certain questions should be shown based on previous answers.
- `completed_surveys.json`: Stores the completed surveys with the user's responses.

**Please note that this project is currently under development and may contain incomplete features and bugs.**

## Features

- User authentication: Users can log in with their username and password.
- Menu navigation: Users can easily navigate between the survey and the sync.
- Domicile: Users can enter a domicile to perform the survey.
- Survey questions and answers: The app presents a set of predefined survey questions and ansers for users to answer.

# Building the APK using Buildozer

*Prerequisites:* Cython (0.29.3), Java (OpenJDK 17), Python and Buildozer (`.spec` file is provided)

*Run Buildozer:*
```
buildozer android debug deploy run
```


## License

This project is licensed under the [MIT License](LICENSE).

Emanuel Cura Costa
ecuracosta@gmail.com
