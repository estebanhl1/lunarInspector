
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

cancer_model = tf.keras.models.load_model("BENMAL.h5")
disease_type = tf.keras.models.load_model("disease_type.h5")

def predict_benmal(image):
    global cancer_model
    Classes = ["benigno","maligno"]
    frame = cv2.imread(image)
    if frame is None:
        return "Error al leer imagen"
    final_image = cv2.resize(frame, (224, 224))
    final_image = np.expand_dims(final_image, axis=0)
    final_image = final_image/255.0
    predictions = cancer_model.predict(final_image)
    #print(predictions)
    result = Classes[np.argmax(predictions)]
    return result
    
def predict_disease_type(image):
    global disease_type
    Classes = ['MEL', 'NV', 'Carcinoma basocelular', 'Keratosis actinica', 'BKL', 'DF', 'VASC', 'SCC']
    frame = cv2.imread(image)
    if frame is None:
        return "Error al leer imagen"
    final_image = cv2.resize(frame, (224, 224))
    final_image = np.expand_dims(final_image, axis=0)
    final_image = final_image/255.0
    predictions = disease_type.predict(final_image)

    indices = np.argsort(predictions[0,:])
    top_indices = indices[-3:]  # Los 3 
    predicciones = {}
    x = 1
    for i in reversed(top_indices):
        class_label = Classes[i]
        #predicciones[class_label] = predictions[0, i] * 100
        predicciones[int(x)] = {"name":class_label, "percent": float(predictions[0, i] * 100)}
        x+=1

    return predicciones    
#print(predict_benmal("images\qNKOC1At8amnLfQU.png"))
#print(predict_benmal("images\melanoma.png"))

#print(predict_disease_type("images\melanoma.png"))