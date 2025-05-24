# Inteligencia artificial
Repositorio de tareas y proyectos para la asignatura de IA <br/>
Grupo 09-10 hrs

**Docente: Dr. Zuriel Dathan Mora Felix**

**Integrantes:**

-De La Rocha Linarez Diego Alejandro <br/>
-Rodríguez Cazarez Joaquín

## **Descripción de las tareas** <br/>

## MODULO 1

**[Tarea 1: Árbol de búsqueda binaria](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo1/Arbol)** <br/>
En esta tarea se hizo la implementación de una estructura de datos tipo árbol, especifícamente de búsqueda binaria con los métodos de inicializar, añadir, buscar e imprimir.

[**Tarea 2: Historia de la IA**](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo1/Tarea%202%20Historia%20de%20la%20IA) <br/>
En esta tarea se realizó un resumen y una presentación de los temas mencionados en el libro "Artificial Intelligence A guide to Intelligent Systems" de la página 5-20.

[**Tarea 3: Sistemas de recomendación**](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo1/Tarea%203%20Sistemas%20de%20recomendacion) <br/>
En esta tarea se realizó una investigación sobre las tecnologías que hacen posible el funcionamiento de los sistemas de recomendación, tanto frameworks, lenguajes y bibliotecas. 

[**Tarea 4: Agentes deliberativos**](https://githubhttps://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo1/Tarea%204%20Agentes%20deliberativos) <br/>
En esta tarea se realizó una investigación sobre los agentes deliberativos, incluyendo definición, características y ejemplos reales de empresas con este tipo de agentes.

[**Tarea 5: Puzzle 8**](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo1/Tarea%205%20Puzzle%208) <br/>
En esta tarea se realizó un ejemplo en python de la resolución del juego Puzzle 8 con el uso de BFS

## MODULO 2

[**Tarea 1: Paradigmas de la IA**](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo2/Tarea%201) <br/>
En esta tarea se realizó una investigación sobre los paradigmas de la IA, incluyendo ejemplos practicos, descripción, relación con el paradigma al que pertenece y una tabla comparativa del modelo cognitivo con el modelo de adquisición de conocimiento.

[**Tarea 2: Red semantica**](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo2/Tarea%202) <br/>
En este trabajo se presenta una red semántica para el negocio de un banco

[**Tarea 3: Clasificador de Spam**](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo2/Tarea%203) <br/>
En este trabajo se crea un clasificador de correos de spam y no spam usando el metodo de clasificación por probabilidad con multinomial Naive Bayes, Las primeras lineas se tratan de la división de los datos, se estandariza el texto en minusculas, se eliminan caracteres especiales, se eliminan espacios multiples y spacios en el inicio y final del codigo. Se usan distintas funciones y clases de sklearn, como el tdfiVectorizer para obtener las palabras en tokens, traintestsplit para separar nuestro dataset en una parte de pruebas y otra de tes y accuracy_score para medir la precisión de predicción de correo.<br>
```
data = pd.read_csv("Modulo2/Tarea 3/spam_assassin.csv")

# Preprocesamiento
data["text"] = data["text"].str.lower()
data["text"] = data["text"].str.replace("[^a-zA-Z0-9]", " ", regex=True)  
data["text"] = data["text"].str.replace("\s+", " ", regex=True) 
data["text"] = data["text"].str.strip()

# Vectorización
vectorizer = TfidfVectorizer(stop_words="english")  
features = vectorizer.fit_transform(data["text"])  
results = data["target"]

features_train, features_test, results_train, results_test = train_test_split(
    features, results, test_size=0.25
)
```
<br>
El modelo de clasificación por probabilidad Multinomial Naive Bayes
consiste en calcular la probabilidad de que un documento sea spam, multiplicando la probabilidad de que los archivos pasados que contenian cierta palabra y que eran spam, exponenciado a la cantidad de veces que aparece esa palabra por la probabilidad de que un documento sea spam dado por el bloque de entrenamiento
<br>

```
model = MultinomialNB(alpha=0.01)
model.fit (features_train, results_train)
```

## MODULO 3

[**Tarea 1: Definición del sistema experto**](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/blob/main/Modulo3/Tarea1/Definición%20del%20sistema%20experto.pdf) <br/>
En este documento se define el problema a resolver con un sistema experto, así como sus objetivos y fuentes de información.

[**Tarea 2: Diagrama de inferencia y reglas del sistema experto**](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo3/Tarea%202%20Diagrama%20y%20reglas%20del%20Sistema%20experto) <br/>
En este documento se definen las reglas y el diagrama de inferencia que se utilizarán para la construcción del sistema experto para el apoyo de tramites del tecnológico de culiacán

## MODULO 4

[**Tarea 1: Preprocesamiento del dataset para vision artificial**](https://github.com/diegodelarochalinarez/tareas-inteligencia-artificial/tree/main/Modulo3/Tarea%202%20Diagrama%20y%20reglas%20del%20Sistema%20experto) <br/>
En este documento se añade un link donde se encuentra el dataset de imagenes y se detallan formas de como realizar el preprocesamiento de imagenes.
