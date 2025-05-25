import cv2
import tensorflow as tf
import numpy as np

# Cargar el modelo entrenado
model = tf.keras.models.load_model("modelo_clasificacion_imagenes.keras")

# Nombres de las clases
class_names = ["anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]

# Configuración de la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error al abrir la cámara")
    exit()

# Crear la ventana una sola vez
cv2.namedWindow("Detección de Emociones", cv2.WINDOW_AUTOSIZE)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el cuadro")
            break

        # Preprocesar el cuadro
        resized_frame = cv2.resize(frame, (80, 80))
        normalized_frame = resized_frame / 255.0
        input_frame = np.expand_dims(normalized_frame, axis=0)

        # Realizar la predicción
        predictions = model.predict(input_frame, verbose=0)
        predicted_class = np.argmax(predictions[0])
        print(predicted_class)
        if predicted_class < len(class_names):
            emotion = class_names[predicted_class]
        else:
            emotion = "Desconocido"

        # Mostrar la emoción en el cuadro
        cv2.putText(frame, f"Emoción: {emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostrar el cuadro en la ventana existente
        cv2.imshow("Detección de Emociones", frame)

        # Salir si se presiona la tecla 'q' (aumentar tiempo de espera)
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == 27:  # 'q' o ESC
            break

except KeyboardInterrupt:
    print("Interrumpido por el usuario")

finally:
    # Liberar recursos y cerrar ventanas
    cap.release()
    cv2.destroyAllWindows()
    # Asegurar que todas las ventanas se cierren
    cv2.waitKey(1)