# Relevamientos App

Relevamientos App is a survey application built using the Kivy framework. It allows users to perform surveys by selecting different domiciles and answering a set of predefined questions and answers.

<img src="https://github.com/ecuracosta/relevamientos_app/assets/47532757/90326d9e-6e37-44f2-89a2-dd5502878816" width="400" height="300" />

## Description

The Relevamientos App is designed to simplify the process of conducting surveys by providing an intuitive user interface. Users can log in with their username and password, enter a domicile and answer a series of survey questions. The app then can synchronize with a database to upload the survey results.

**Please note that this project is currently under development and may contain incomplete features and bugs.**

## Features

- User authentication: Users can log in with their username and password.
- Menu navigation: Users can easily navigate between the survey and the sync.
- Domicile: Users can enter a domicile to perform the survey.
- Survey questions and answers: The app presents a set of predefined survey questions and ansers for users to answer.

# Building the APK using Buildozer

*Prerequisites:* Cython, Java (OpenJDK 11 recommended), Python and Buildozer (`.spec` file is provided)

*Run Buildozer:*
```
buildozer android debug deploy run
```


## License

This project is licensed under the [MIT License](LICENSE).

Emanuel Cura Costa
ecuracosta@gmail.com
