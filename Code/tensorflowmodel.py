from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import utils
from tensorflow.keras.preprocessing import image
import numpy as np
from cv2 import cv2
import os

def uploadImage(path):
    f = open(path, "rb")
    chunk = f.read()
    chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
    image = cv2.imdecode(chunk_arr, 0)
    image = cv2.resize(image, (100, 170))

    return False if image is None else image

path = os.path.dirname(os.path.realpath(__file__)) + "\\numbersDataSet"
os.chdir(path)
x_train = []
y_train = []
for i in range(10):
    os.chdir(path + f'\\images_of_{i}')
    for img in os.listdir():
        x_train.append(uploadImage(img))
        y_train.append(i)
        
x_train = np.array(x_train).reshape(1000, 17000)
os.chdir(path + f'\\images_of_{4}')
x_test = uploadImage('64.jpg').reshape(1, 17000) / 255

x_train = x_train / 255

print(y_train[0])

y_train = utils.to_categorical(y_train, 10)

print(y_train[0])

model = Sequential()
model.add(Dense(17000, input_dim=17000, activation="relu"))
model.add(Dense(10, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="SGD", metrics=["accuracy"])

print(model.summary())

history = model.fit(x_train, y_train, 
                    batch_size=200, 
                    epochs=40,  
                    verbose=1)

os.chdir(os.path.dirname(os.path.realpath(__file__)))
model.save('number_model.h5')

predictions = model.predict(x_test)
n = 0
print(predictions[n])

print(np.argmax(predictions[n]))
