# Import required libraries
import csv
import cv2
import numpy as np
import os

# Initialize variables for the model
images       = []
measurements = []
correction   = 0.2
corrections  = [0, correction, -correction]
dropoutProb  = 0.5

print('---------------------------------------------------')
print('Staring Given Data')
print('---------------------------------------------------')

# Load given data
with open('data/driving_log.csv', 'r', newline='') as drivingLog:
    reader = csv.reader(drivingLog, delimiter=',', skipinitialspace=True)
    next(drivingLog, None)
    for line in reader:
        for i in range(3):
            imageFileName = 'data/' + line[i]
            bgrImage = cv2.imread(imageFileName)
            rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)
            croppedImage = rgbImage[50:137, :, :]
            image = cv2.resize(croppedImage, (200, 66))
            images.append(image)
            measurement = float(line[3]) + corrections[i]
            measurements.append(measurement)

            flippedImage = cv2.flip(image, 1)
            images.append(flippedImage)
            measurements.append(-measurement)

print('---------------------------------------------------')
print('Staring Forward Driving Data')
print('---------------------------------------------------')

# Load forward driving data
with open('ForwardDriving/driving_log.csv', 'r', newline='') as drivingLog:
    reader = csv.reader(drivingLog, delimiter=',', skipinitialspace=True)
    next(drivingLog, None)
    for line in reader:
        for i in range(3):
            (dirName, filename) = os.path.split(line[i])

            imageFileName = 'ForwardDriving/IMG/' + filename
            bgrImage = cv2.imread(imageFileName)
            rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)
            croppedImage = rgbImage[50:137, :, :]
            image = cv2.resize(croppedImage, (200, 66))
            images.append(image)
            measurement = float(line[3]) + corrections[i]
            measurements.append(measurement)

print('---------------------------------------------------')
print('Staring Reverse Driving Data')
print('---------------------------------------------------')

# Load reverse driving data
with open('ReverseDriving/driving_log.csv', 'r', newline='') as drivingLog:
    reader = csv.reader(drivingLog, delimiter=',', skipinitialspace=True)
    next(drivingLog, None)
    for line in reader:
        for i in range(3):
            (dirName, filename) = os.path.split(line[i])

            imageFileName = 'ReverseDriving/IMG/' + filename
            bgrImage = cv2.imread(imageFileName)
            rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)
            croppedImage = rgbImage[50:137, :, :]
            image = cv2.resize(croppedImage, (200, 66))
            images.append(image)
            measurement = float(line[3]) + corrections[i]
            measurements.append(measurement)

# TRAIN THE MODEL
X_train = np.array(images)
y_train = np.array(measurements)

print(X_train.shape)
print(y_train.shape)

print('---------------------------------------------------')
print('Starting training')
print('---------------------------------------------------')

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Dropout
from keras.layers.convolutional import Conv2D

model = Sequential()
model.add(Lambda(lambda x: (x / 255.0) - 0.5, input_shape=(66, 200, 3)))
model.add(Conv2D(filters=24, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
model.add(Conv2D(filters=36, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
model.add(Conv2D(filters=48, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu'))
model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu'))
model.add(Flatten())
model.add(Dense(1164, activation='relu'))
model.add(Dropout(dropoutProb))
model.add(Dense(100, activation='relu'))
model.add(Dropout(dropoutProb))
model.add(Dense(50, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, validation_split = 0.2, shuffle = True, epochs = 5)
model.save('model.h5')