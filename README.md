# Fruit Video Recognition

This project is a WIP designed to recognize certain types of fruits in video frames using OpenCV and some other Computer Vision/Machine Learning API.
The API and the dataset used to train the Machine Learning model have yet to be chosen.

## main.py

Main function. Assembles the other files together.

## user_interface.py

Contains all the functions that manipulate the GUI directly.

## video_capture.py

Contains the basic functions for video file and frames manipulation, discounting the machine learning model

## fruit_cv_model.py

Handles the creation (training, validation and testing) and deployment of the machine learning model to be used by the other files.
Will most likely be using PyTorch/TorchVision but the decision is not final.

-------------------------------------------------------------------------------------

Further details will be announced soon.

CURRENT COMMIT CRASHING ON LAUNCH BECAUSE OF NUMPY ON PYTHON 3.14.2! Currently working on that.