import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox 

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

ventana = tk.Tk()
ventana.title("DETECCION DE SPAM")
ventana.minsize(width=300, height=400)
ventana.config(padx=35, pady=35)

emisor = tk.Label(text="Emisor:",font=("courier",14))
emisor.grid(column =0, row=1,sticky = "w")

emisor_texto = tk.Entry(width=50,font=("courier",14))
emisor_texto.grid(column =0, row=2)

receptor = tk.Label(text="Receptor:",font=("courier",14))
receptor.grid(column =0, row=3,sticky = "w")

receptor_texto = tk.Entry(width=50,font=("courier",14))
receptor_texto.grid(column =0, row=4)

asunto = tk.Label(text="Asunto:" ,font=("courier",14))
asunto.grid(column =0, row=5,sticky = "w")

asunto_texto = tk.Entry(width=50,font=("courier",14))
asunto_texto.grid(column =0, row=6)

mensaje = tk.Label(text="Mensaje:",font=("courier",14))
mensaje.grid(column =0, row=7,sticky = "w")

mensaje_texto = tk.Text(width=50, height=5, font=("courier",14))
mensaje_texto.grid(column =0, row=8)
def analizar_correo():
    emisor = emisor_texto.get()
    receptor = receptor_texto.get()
    asunto = asunto_texto.get()
    mensaje = mensaje_texto.get("1.0", "end-1c")

    if not emisor or not receptor or not mensaje or not asunto:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")
        return
    
    correo = f"From: {emisor}, To: {receptor}, Subject: {asunto}, Message: {mensaje}"
    correo = correo.lower()  
    correo = correo.replace("[^a-zA-Z0-9 ]", " ")
    correo_vectorizado = vectorizer.transform([correo])
    prediccion = model.predict(correo_vectorizado)[0]   
  
    if prediccion == 1:
         messagebox.showinfo("Resultado", "El correo analizado es spam")
    else:
         messagebox.showinfo("Resultado", "El correo analizado no es spam")
boton =tk.Button(
    ventana,
    text= "Analizar",
    font=("courier", 14),
    
    command=analizar_correo,
)
boton.grid(column=0,row =10)

ventana.mainloop()