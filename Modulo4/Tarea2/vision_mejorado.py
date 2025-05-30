import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import os
import numpy as np
from pycocotools.coco import COCO
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import warnings

# Configurar TensorFlow para usar solo CPU si hay problemas con GPU
warnings.filterwarnings('ignore')
tf.config.set_visible_devices([], 'GPU')  # Forzar uso de CPU
print("Configurado para usar CPU")

# Configuración de parámetros mejorados
img_height = 80
img_width = 80
batch_size = 8  # Reducido para CPU
epochs = 50  # Reducido para pruebas más rápidas
learning_rate = 0.001  # Aumentado ligeramente para CPU

# Rutas a los conjuntos de datos y anotaciones COCO
train_dir = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/train"
val_dir = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/valid"
test_dir = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/test"

train_annotations = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/train/_annotations.coco.json"
val_annotations = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/valid/_annotations.coco.json"
test_annotations = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/test/_annotations.coco.json"

# Data augmentation para mejorar la generalización
def augment_image(image, label):
    """Aplica data augmentation a las imágenes de entrenamiento"""
    # Flip horizontal aleatorio
    if tf.random.uniform([]) > 0.5:
        image = tf.image.flip_left_right(image)
    
    # Ajuste de brillo aleatorio
    image = tf.image.random_brightness(image, 0.1)
    
    # Ajuste de contraste aleatorio
    image = tf.image.random_contrast(image, 0.9, 1.1)
    
    # Ajuste de saturación aleatoria
    image = tf.image.random_saturation(image, 0.9, 1.1)
    
    # Rotación pequeña (usando tf.image.rot90 para compatibilidad)
    if tf.random.uniform([]) > 0.7:
        k = tf.random.uniform([], 0, 4, dtype=tf.int32)
        image = tf.image.rot90(image, k=1)  # Rotación de 90 grados ocasional
    
    # Ruido gaussiano ligero
    if tf.random.uniform([]) > 0.5:
        noise = tf.random.normal(shape=tf.shape(image), mean=0.0, stddev=0.01, dtype=tf.float32)
        image = tf.add(image, noise)
    
    # Asegurar que los valores estén en el rango correcto
    image = tf.clip_by_value(image, -1.0, 1.0)
    
    return image, label

# Función mejorada para cargar imágenes y etiquetas desde COCO
def load_coco_dataset(images_dir, annotations_path, is_training=False):
    print(f"Cargando dataset desde: {images_dir}")
    print(f"Anotaciones desde: {annotations_path}")
    
    try:
        coco = COCO(annotations_path)
        categories = coco.loadCats(coco.getCatIds())
        category_id_to_label = {cat['id']: idx for idx, cat in enumerate(categories)}
        global num_classes
        num_classes = len(categories)
        
        print(f"Número de clases detectadas: {num_classes}")
        print(f"Categorías: {[cat['name'] for cat in categories]}")
        
        # Filtrar la categoría 'emotions' si existe (es solo una categoría padre)
        if 'emotions' in [cat['name'] for cat in categories]:
            print("Detectada categoría 'emotions' - será ignorada")
            filtered_categories = [cat for cat in categories if cat['name'] != 'emotions']
            category_id_to_label = {cat['id']: idx for idx, cat in enumerate(filtered_categories)}
            num_classes = len(filtered_categories)
            print(f"Clases filtradas: {num_classes}")
            print(f"Categorías finales: {[cat['name'] for cat in filtered_categories]}")

    except Exception as e:
        print(f"Error cargando anotaciones COCO: {e}")
        return None

    def generator():
        image_ids = coco.getImgIds()
        total_images = len(image_ids)
        processed = 0
        successful = 0
        
        print(f"Total de imágenes a procesar: {total_images}")
        
        for image_id in image_ids:
            try:
                # Obtener información de la imagen
                image_info = coco.loadImgs(image_id)[0]
                image_path = os.path.join(images_dir, image_info['file_name'])
                
                # Verificar que el archivo existe y no está vacío
                if not os.path.exists(image_path):
                    continue
                    
                if os.path.getsize(image_path) == 0:
                    continue
                
                # Cargar la imagen
                image = tf.io.read_file(image_path)
                
                # Decodificar imagen con mejor manejo de errores
                try:
                    image = tf.image.decode_jpeg(image, channels=3)
                except:
                    try:
                        image = tf.image.decode_png(image, channels=3)
                    except:
                        try:
                            image = tf.image.decode_image(image, channels=3)
                        except:
                            continue
                
                # Asegurar que la imagen tenga exactamente 3 canales
                image.set_shape([None, None, 3])
                image = tf.image.resize_with_pad(image, img_height, img_width)
                image = tf.cast(image, tf.float32)
                
                # Normalización mejorada (zero-centered)
                image = (image / 127.5) - 1.0  # Normalización [-1, 1]
                
                # Obtener las etiquetas (categorías)
                annotation_ids = coco.getAnnIds(imgIds=image_id)
                annotations = coco.loadAnns(annotation_ids)
                
                # Filtrar anotaciones de la categoría 'emotions' si existe
                valid_labels = []
                for ann in annotations:
                    if ann['category_id'] in category_id_to_label:
                        valid_labels.append(category_id_to_label[ann['category_id']])
                
                # Usar solo la primera etiqueta válida
                if valid_labels:
                    label = valid_labels[0]
                else:
                    continue  # Saltar imágenes sin etiquetas válidas
                
                processed += 1
                successful += 1
                
                if processed % 50 == 0:
                    print(f"Procesadas {processed}/{total_images} imágenes ({successful} exitosas)")
                
                yield image, label
                
            except Exception as e:
                processed += 1
                if processed % 100 == 0:
                    print(f"Error en imagen {processed}: {str(e)}")
                continue
        
        print(f"Dataset cargado: {successful} imágenes exitosas de {total_images} totales")

    try:
        dataset = tf.data.Dataset.from_generator(
            generator,
            output_signature=(
                tf.TensorSpec(shape=(img_height, img_width, 3), dtype=tf.float32),
                tf.TensorSpec(shape=(), dtype=tf.int32)
            )
        )
        
        # Aplicar data augmentation solo al conjunto de entrenamiento
        if is_training:
            print("Aplicando data augmentation...")
            dataset = dataset.map(augment_image, num_parallel_calls=tf.data.AUTOTUNE)
        
        # Optimizaciones del dataset
        dataset = dataset.cache()
        if is_training:
            dataset = dataset.shuffle(buffer_size=500)  # Reducido para CPU
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
        
    except Exception as e:
        print(f"Error creando dataset: {e}")
        return None

# Crear datasets para entrenamiento, validación y prueba
print("="*50)
print("CARGANDO DATASETS")
print("="*50)

print("Cargando dataset de entrenamiento...")
train_dataset = load_coco_dataset(train_dir, train_annotations, is_training=True)

if train_dataset is None:
    print("ERROR: No se pudo cargar el dataset de entrenamiento")
    exit(1)

print("\nCargando dataset de validación...")
val_dataset = load_coco_dataset(val_dir, val_annotations, is_training=False)

if val_dataset is None:
    print("ERROR: No se pudo cargar el dataset de validación")
    exit(1)

print("\nCargando dataset de prueba...")
test_dataset = load_coco_dataset(test_dir, test_annotations, is_training=False)

if test_dataset is None:
    print("ERROR: No se pudo cargar el dataset de prueba")
    exit(1)

print(f"\nDatasets cargados exitosamente!")
print(f"Número de clases para el modelo: {num_classes}")

# Verificar que tenemos datos
try:
    print("Verificando datos del dataset de entrenamiento...")
    for batch in train_dataset.take(1):
        images, labels = batch
        print(f"Batch shape: {images.shape}")
        print(f"Labels shape: {labels.shape}")
        print(f"Labels únicos en el primer batch: {tf.unique(labels)[0]}")
        break
except Exception as e:
    print(f"Error verificando datos: {e}")
    exit(1)

# Construcción del modelo mejorado con regularización
def create_improved_model():
    model = tf.keras.Sequential([
        # Primera capa convolucional con batch normalization
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Segunda capa convolucional
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Tercera capa convolucional
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Capas densas con regularización
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

# Crear el modelo
model = create_improved_model()

# Mostrar resumen del modelo
model.summary()

# Optimizador mejorado con scheduling
initial_learning_rate = learning_rate
lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate,
    decay_steps=1000,
    decay_rate=0.9,
    staircase=True
)

optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)

# Compilación del modelo
model.compile(
    optimizer=optimizer,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Callbacks para mejorar el entrenamiento
callbacks = [
    EarlyStopping(
        monitor='val_accuracy',
        patience=10,  # Reducido para entrenamientos más cortos
        restore_best_weights=True,
        verbose=1,
        min_delta=0.001
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,  # Reducido
        min_lr=1e-6,
        verbose=1
    ),
    ModelCheckpoint(
        'mejor_modelo_emociones.keras',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1,
        save_weights_only=False
    )
]

# Entrenamiento del modelo
print("="*50)
print("INICIANDO ENTRENAMIENTO")
print("="*50)

try:
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )
    print("¡Entrenamiento completado exitosamente!")
    
except Exception as e:
    print(f"Error durante el entrenamiento: {e}")
    print("Guardando modelo con el estado actual...")
    model.save("modelo_clasificacion_emociones_parcial.keras")
    exit(1)

# Evaluación en el conjunto de prueba
print("="*50)
print("EVALUANDO MODELO")
print("="*50)

try:
    test_results = model.evaluate(test_dataset, verbose=1)
    test_loss = test_results[0]
    test_acc = test_results[1]
    
    print(f"Precisión en el conjunto de prueba: {test_acc:.4f}")
    print(f"Pérdida en el conjunto de prueba: {test_loss:.4f}")
    
    # Generar predicciones para la matriz de confusión
    print("Generando predicciones para matriz de confusión...")
    y_true = []
    y_pred = []
    
    for batch in test_dataset:
        images, labels = batch
        predictions = model.predict(images, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)
        
        y_true.extend(labels.numpy())
        y_pred.extend(predicted_classes)
    
    # Crear matriz de confusión
    cm = confusion_matrix(y_true, y_pred)
    
    # Obtener nombres de las clases
    try:
        coco_test = COCO(test_annotations)
        categories = coco_test.loadCats(coco_test.getCatIds())
        # Filtrar 'emotions' si existe
        class_names = [cat['name'] for cat in categories if cat['name'] != 'emotions']
        if len(class_names) != num_classes:
            class_names = [f'Clase_{i}' for i in range(num_classes)]
    except:
        class_names = [f'Clase_{i}' for i in range(num_classes)]
    
    print(f"Clases detectadas: {class_names}")
    
    # Mostrar reporte de clasificación
    print("\n" + "="*50)
    print("REPORTE DE CLASIFICACIÓN")
    print("="*50)
    report = classification_report(y_true, y_pred, target_names=class_names, zero_division=0)
    print(report)
    
except Exception as e:
    print(f"Error durante la evaluación: {e}")
    test_acc = 0

# Guardar el modelo final
model.save("modelo_clasificacion_emociones_mejorado.keras")
print("Modelo guardado como 'modelo_clasificacion_emociones_mejorado.keras'")

# Guardar también el mejor modelo del checkpoint
print("Mejor modelo guardado como 'mejor_modelo_emociones.keras'")

# Crear gráficas del entrenamiento
def plot_training_history(history):
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Gráfica de precisión
        ax1.plot(history.history['accuracy'], label='Entrenamiento')
        ax1.plot(history.history['val_accuracy'], label='Validación')
        ax1.set_title('Precisión del Modelo')
        ax1.set_xlabel('Época')
        ax1.set_ylabel('Precisión')
        ax1.legend()
        ax1.grid(True)
        
        # Gráfica de pérdida
        ax2.plot(history.history['loss'], label='Entrenamiento')
        ax2.plot(history.history['val_loss'], label='Validación')
        ax2.set_title('Pérdida del Modelo')
        ax2.set_xlabel('Época')
        ax2.set_ylabel('Pérdida')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('entrenamiento_historia.png', dpi=300, bbox_inches='tight')
        print("Gráficas guardadas como 'entrenamiento_historia.png'")
        
        # Solo mostrar si tenemos display disponible
        try:
            plt.show()
        except:
            print("No se puede mostrar gráficas (sin display)")
            
    except Exception as e:
        print(f"Error creando gráficas: {e}")

def plot_confusion_matrix(cm, class_names):
    """Crear y guardar la matriz de confusión"""
    try:
        plt.figure(figsize=(10, 8))
        
        # Crear la matriz de confusión normalizada
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        # Crear el plot
        im = plt.imshow(cm_normalized, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Matriz de Confusión Normalizada')
        plt.colorbar(im)
        
        # Configurar etiquetas
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names, rotation=45, ha='right')
        plt.yticks(tick_marks, class_names)
        
        # Agregar texto en cada celda
        fmt = '.2f'
        thresh = cm_normalized.max() / 2.
        for i in range(cm_normalized.shape[0]):
            for j in range(cm_normalized.shape[1]):
                plt.text(j, i, format(cm_normalized[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm_normalized[i, j] > thresh else "black")
        
        plt.ylabel('Etiqueta Verdadera')
        plt.xlabel('Etiqueta Predicha')
        plt.tight_layout()
        
        # Guardar la matriz de confusión
        plt.savefig('matriz_confusion.png', dpi=300, bbox_inches='tight')
        print("Matriz de confusión guardada como 'matriz_confusion.png'")
        
        # También crear una versión con valores absolutos
        plt.figure(figsize=(10, 8))
        im = plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Matriz de Confusión (Valores Absolutos)')
        plt.colorbar(im)
        
        plt.xticks(tick_marks, class_names, rotation=45, ha='right')
        plt.yticks(tick_marks, class_names)
        
        # Agregar texto con valores absolutos
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, format(cm[i, j], 'd'),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        
        plt.ylabel('Etiqueta Verdadera')
        plt.xlabel('Etiqueta Predicha')
        plt.tight_layout()
        
        plt.savefig('matriz_confusion_absoluta.png', dpi=300, bbox_inches='tight')
        print("Matriz de confusión absoluta guardada como 'matriz_confusion_absoluta.png'")
        
        # Solo mostrar si tenemos display disponible
        try:
            plt.show()
        except:
            print("No se puede mostrar gráficas (sin display)")
            
    except Exception as e:
        print(f"Error creando matriz de confusión: {e}")

# Mostrar gráficas del entrenamiento si el entrenamiento fue exitoso
if 'history' in locals():
    plot_training_history(history)
else:
    print("No hay historial de entrenamiento para graficar")

# Mostrar matriz de confusión si tenemos las variables
if 'cm' in locals() and 'class_names' in locals():
    print("\n" + "="*50)
    print("MATRIZ DE CONFUSIÓN")
    print("="*50)
    print("Matriz de confusión:")
    print(cm)
    plot_confusion_matrix(cm, class_names)
else:
    print("No se pudo generar la matriz de confusión")

print("\n" + "="*50)
print("¡Entrenamiento completado!")
print("Para usar el modelo mejorado, carga 'mejor_modelo_emociones.keras'")
print("Archivos generados:")
print("- mejor_modelo_emociones.keras (mejor modelo)")
print("- modelo_clasificacion_emociones_mejorado.keras (modelo final)")
print("- entrenamiento_historia.png (gráficas de entrenamiento)")
print("- matriz_confusion.png (matriz de confusión normalizada)")
print("- matriz_confusion_absoluta.png (matriz de confusión con valores absolutos)")
print("="*50)
