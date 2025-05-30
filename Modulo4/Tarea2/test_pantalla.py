import cv2
import tensorflow as tf
import numpy as np
from collections import deque
import time

# Cargar el modelo entrenado
model_loaded = False
model_name = "desconocido"

# Intentar cargar modelos en orden de preferencia
model_paths = [
    ("mejor_modelo_simple.keras", "Modelo simple mejorado"),
    ("modelo_simple_emociones.keras", "Modelo simple final"),
    ("modelo_clasificacion_imagenes.keras", "Modelo original")
]

for model_path, description in model_paths:
    try:
        model = tf.keras.models.load_model(model_path)
        print(f"{description} cargado exitosamente: {model_path}")
        model_name = description
        model_loaded = True
        break
    except Exception as e:
        print(f"No se pudo cargar {model_path}: {e}")
        continue

if not model_loaded:
    print("ERROR: No se pudo cargar ningún modelo")
    exit(1)

# Nombres de las clases
class_names = ["anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]

def preprocess_frame(frame):
    """Preprocesamiento simple del frame"""
    # Redimensionar
    resized_frame = cv2.resize(frame, (80, 80))
    
    # Convertir a RGB
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    
    # Normalización
    normalized_frame = (rgb_frame.astype(np.float32) / 127.5) - 1.0
    
    # Expandir dimensiones
    input_frame = np.expand_dims(normalized_frame, axis=0)
    
    return input_frame

def draw_simple_info(frame, emotion, confidence):
    """Dibuja información de manera muy simple y visible"""
    height, width = frame.shape[:2]
    
    # Fondo negro para el texto en la parte superior
    cv2.rectangle(frame, (0, 0), (width, 150), (0, 0, 0), -1)
    
    # Texto muy grande y visible
    cv2.putText(frame, f"EMOCION: {emotion.upper()}", (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 4)
    
    cv2.putText(frame, f"CONFIANZA: {confidence:.2f} ({confidence*100:.0f}%)", (10, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
    
    # Modelo usado
    cv2.putText(frame, f"Modelo: {model_name}", (10, 130), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

def main():
    # Configuración de la cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error al abrir la cámara")
        return
    
    print("="*60)
    print("DETECTOR DE EMOCIONES - VERSION DE PRUEBA")
    print("="*60)
    print("Presiona 'q' para salir")
    print("="*60)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el cuadro")
            break
        
        try:
            # Preprocesar el frame completo
            input_frame = preprocess_frame(frame)
            
            # Realizar predicción
            predictions = model.predict(input_frame, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = predictions[0][predicted_class]
            
            # Obtener nombre de la emoción
            if predicted_class < len(class_names):
                emotion = class_names[predicted_class]
            else:
                emotion = "Desconocido"
            
            # Mostrar en consola también
            print(f"Emoción detectada: {emotion} - Confianza: {confidence:.3f}")
            
            # Dibujar información en el frame
            draw_simple_info(frame, emotion, confidence)
            
        except Exception as e:
            print(f"Error en predicción: {e}")
            draw_simple_info(frame, "ERROR", 0.0)
        
        # Mostrar el frame
        cv2.imshow("Test Detector Emociones", frame)
        
        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
    print("Test completado")

if __name__ == "__main__":
    main()
