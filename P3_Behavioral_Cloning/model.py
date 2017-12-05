# Import required libraries
import csv
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

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
            # Get current image name
            imageFileName = 'data/' + line[i]
            # Convert read image to RGB
            bgrImage = cv2.imread(imageFileName)
            rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)
            # Crop the image, resize it and append it to all existing images.
            croppedImage = rgbImage[50:137, :, :]
            image = cv2.resize(croppedImage, (200, 66))
            images.append(image)
            # Apply corrections to measurements and append to existing measurements
            measurement = float(line[3]) + corrections[i]
            measurements.append(measurement)

            # Flip the images to create additional data.
            # Correspondingly apply negated measurements.
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
            # Extract directory name and file name for each image
            (dirName, filename) = os.path.split(line[i])

            # Get current image name
            imageFileName = 'ForwardDriving/IMG/' + filename
            # Convert read image to RGB
            bgrImage = cv2.imread(imageFileName)
            rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)
            # Crop the image, resize it and append it to all existing images.
            croppedImage = rgbImage[50:137, :, :]
            image = cv2.resize(croppedImage, (200, 66))
            images.append(image)
            # Apply corrections to measurements and append to existing measurements
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
            # Extract directory name and file name for each image
            (dirName, filename) = os.path.split(line[i])

            # Get current image name
            imageFileName = 'ReverseDriving/IMG/' + filename
            # Convert read image to RGB
            bgrImage = cv2.imread(imageFileName)
            rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)
            # Crop the image, resize it and append it to all existing images.
            croppedImage = rgbImage[50:137, :, :]
            image = cv2.resize(croppedImage, (200, 66))
            images.append(image)
            # Apply corrections to measurements and append to existing measurements
            measurement = float(line[3]) + corrections[i]
            measurements.append(measurement)

# TRAIN THE MODEL
X_train = np.array(images)
y_train = np.array(measurements)

# Print the size of training images and measurements
print(X_train.shape)
print(y_train.shape)

print('---------------------------------------------------')
print('Starting training')
print('---------------------------------------------------')

# Import keras libraries.
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Dropout
from keras.layers.convolutional import Conv2D

# Create CNN Model design
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

# Compile the mode, fit the model with training data.
# Create a training-validation split of 80-20 and run for 5 epochs.
# Save the model to a H5 file.
model.compile(optimizer='adam', loss='mse')
print(model.summary())
history_object = model.fit(X_train, y_train, validation_split = 0.2, shuffle = True, epochs = 5, verbose = 1)
model.save('model.h5')

### print the keys contained in the history object
print(history_object.history.keys())

### plot the training and validation loss for each epoch
plt.plot(history_object.history['loss'])
plt.plot(history_object.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.show()