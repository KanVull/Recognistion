from tensorflow import keras
import numpy as np

model = keras.models.load_model('number_model.h5')

def recognize(image):
    image = image.reshape(1, 17000) / 255
    prediction = model.predict(image)
    return str(np.argmax(prediction[0]))




