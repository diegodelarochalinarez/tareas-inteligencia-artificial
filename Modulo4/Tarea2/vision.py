import tensorflow as tf
import tensorflow.keras.layers as layers
import os
from pycocotools.coco import COCO

# Configuración de parámetros
img_height = 80
img_width = 80
batch_size = 32
epochs = 10

# Rutas a los conjuntos de datos y anotaciones COCO
train_dir = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/train"
val_dir = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/valid"
test_dir = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/test"

train_annotations = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/train/_annotations.coco.json"
val_annotations = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/valid/_annotations.coco.json"
test_annotations = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/test/_annotations.coco.json"

# Función para cargar imágenes y etiquetas desde COCO
def load_coco_dataset(images_dir, annotations_path):
    coco = COCO(annotations_path)
    categories = coco.loadCats(coco.getCatIds())
    category_id_to_label = {cat['id']: idx for idx, cat in enumerate(categories)}
    global num_classes
    num_classes = len(categories)

    def generator():
        for image_id in coco.getImgIds():
            # Obtener información de la imagen
            image_info = coco.loadImgs(image_id)[0]
            image_path = os.path.join(images_dir, image_info['file_name'])
            
            # Cargar la imagen
            image = tf.io.read_file(image_path)
            image = tf.image.decode_jpeg(image, channels=3)
            image = tf.image.resize(image, [img_height, img_width])
            image = image / 255.0  # Normalización
            
            # Obtener las etiquetas (categorías)
            annotation_ids = coco.getAnnIds(imgIds=image_id)
            annotations = coco.loadAnns(annotation_ids)
            labels = [category_id_to_label[ann['category_id']] for ann in annotations]
            
            # Usar solo la primera etiqueta si hay múltiples (para clasificación simple)
            label = labels[0] if labels else 0
            yield image, label

    dataset = tf.data.Dataset.from_generator(
        generator,
        output_signature=(
            tf.TensorSpec(shape=(img_height, img_width, 3), dtype=tf.float32),
            tf.TensorSpec(shape=(), dtype=tf.int32)
        )
    )
    return dataset

# Crear datasets para entrenamiento, validación y prueba
train_dataset = load_coco_dataset(train_dir, train_annotations).batch(batch_size)
val_dataset = load_coco_dataset(val_dir, val_annotations).batch(batch_size)
test_dataset = load_coco_dataset(test_dir, test_annotations).batch(batch_size)

# Construcción del modelo
model = tf.keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, activation='softmax')  # Salida para clasificación
])

# Compilación del modelo
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenamiento del modelo
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=epochs
)

# Evaluación en el conjunto de prueba
test_loss, test_acc = model.evaluate(test_dataset)
print(f"Precisión en el conjunto de prueba: {test_acc:.2f}")

# Guardar el modelo entrenado
model.save("modelo_clasificacion_imagenes.keras")
print("Modelo guardado como 'modelo_clasificacion_imagenes.keras'")