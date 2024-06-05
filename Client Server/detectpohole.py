# Importing all necessary libraries 

import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np
import matplotlib.pyplot as plt

PATH = os.path.join(os.getcwd(), 'PotholeDataset_Updated\PotholeDataset')
print(PATH)

train_dir = os.path.join(PATH, 'Train')
validation_dir = os.path.join(PATH, 'Validation')

train_Pothole_dir = os.path.join(train_dir, 'Pothole')  # directory with our training Pothole pictures
train_Road_dir = os.path.join(train_dir, 'Road')  # directory with our training Road pictures

validation_Pothole_dir = os.path.join(validation_dir, 'Pothole')  # directory with our validation Pothole pictures
validation_Road_dir = os.path.join(validation_dir, 'Road') # directory with our validation Road pictures

num_Pothole_tr = len(os.listdir(train_Pothole_dir))
num_Road_tr = len(os.listdir(train_Road_dir))

num_Pothole_val = len(os.listdir(validation_Pothole_dir))
num_Road_val = len(os.listdir(validation_Road_dir))

total_train = num_Pothole_tr + num_Road_tr
total_val = num_Pothole_val + num_Road_val

batch_size = 22
epochs = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150

# Training
train_image_generator = ImageDataGenerator(rescale=1. / 255,
                                           rotation_range=45,
                                           width_shift_range=.15,
                                           height_shift_range=.15,
                                           horizontal_flip=True,
                                           zoom_range=0.5)  # Generator for our training data

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary')
# Validation
validation_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our validation data

val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=validation_dir,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='binary')

model = Sequential([
    Conv2D(16, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    MaxPooling2D(),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(
    train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size
)

model.save("trained.h5")
