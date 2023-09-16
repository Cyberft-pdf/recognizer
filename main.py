import tensorflow as tf
import cv2
import joblib
import numpy as np

model = tf.keras.models.load_model('model2.h5')  

cap = cv2.VideoCapture(0)


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")



while True:
    ret, frame = cap.read()  


    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


        face = frame[y:y+h, x:x+w]


        face = cv2.resize(face, (200, 200))

        face = face / 255.0

        face = np.expand_dims(face, axis=0)

        predictions = model.predict(face)

        gender_label = np.argmax(predictions, axis=1)[0]

        if gender_label == 0:
            gender = "Female"
        else:
            gender = "Male"

        cv2.putText(frame, f'Pohlavi: {gender}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("recognizer", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
