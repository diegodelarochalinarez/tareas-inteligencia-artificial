import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Cargar datos
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

from sklearn.naive_bayes import MultinomialNB

model = MultinomialNB(alpha=0.01)
model.fit (features_train, results_train)

results_pred = model.predict(features_test)

print("Predicciones: ",accuracy_score(results_test, results_pred))

print(model.get_params())