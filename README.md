# Siesta

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

*Version built with Love*

This project was developed as a submission for the Microsoft Engage'22.

## Resources
- [Demo Video](https://drive.google.com/file/d/1lnF16wDXn3xtUGHcfgtMHfMtqr_EV61V/view?usp=sharing)

## Getting Started
- Clone the repository. Create a virtual env using the command `python3 -m venv /path/to/new/virtual/environment`.
- Refer to the [documentation](https://docs.python.org/3/library/venv.html) for more details.
- Install the requirements using the command `pip install -r requirements.txt`.
- Install dlib using the command `pip install .\flaskapp\models_dlib\dlib-19.19.0-cp38-cp38-win_amd64.whl`.
- Download *shape_predictor_68_face_landmarks.dat* from the [link](https://github.com/tzutalin/dlib-android/blob/master/data/shape_predictor_68_face_landmarks.dat) and add it to the models_dlib directory.

## Working
Siesta is a webapp which optimizes your working hours by preventing you from drowsing off. You are constantly monitored during you screen-time, and you're sent an alert email if you're caught yawning or closing your eyes for some-time. If this continues for than 30 seconds(the duration has been kept short in the video for demonstration purposes), an alarm goes off and after some-time your system will go into hibernate mode and you can take your power nap. Isn't it helpful?

## Why I Built This
We all feel sleepy during long working hours staring continuously at the screen. You can use this application to make optimize your working time. ​

## Future Scope
An automatic switch on and off system based on Pomodoro technique can be implemented.
