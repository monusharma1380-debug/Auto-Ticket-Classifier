import kagglehub
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

path = kagglehub.dataset_download("tobiasbueck/multilingual-customer-support-tickets")

df = pd.read_csv(os.path.join(path, "dataset-tickets-multi-lang-4-20k.csv"))

df = df[df['language'] == 'en']
df["text"] = df["subject"].fillna("") + ". " + df["body"].fillna("")

df = df[["text", "queue", "priority"]]
df.columns = ["query", "category", "priority"]


texts = df["query"]
labels = df["category"]

X_train, X_test, Y_train, Y_test = train_test_split(
    texts, labels, test_size =0.25, random_state=42
)


#vectorizing part
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

#model training
model = ComplementNB()
model.fit(X_train_vec, Y_train)

predictions = model.predict(X_test_vec)

print("Predictions :", predictions)
print("Acutal : ", Y_test)

#acccuracy testing
accuracy = accuracy_score(Y_test, predictions)
print("Accuracy: ",accuracy)
print(classification_report(Y_test, predictions, zero_division=0))

#priority training 
labels_p = df["priority"]

x_train, x_test, y_train, y_test = train_test_split(
    texts, labels_p, test_size = .20, random_state = 42
)

#verterization for priority 
vectorizer_priority = TfidfVectorizer()
x_train_vec = vectorizer_priority.fit_transform(x_train)
x_test_vec = vectorizer_priority.transform(x_test)

#model train
model_pri = ComplementNB()
model_pri.fit(x_train_vec, y_train)

predictions_priority = model_pri.predict(x_test_vec)

print("Predictions :", predictions_priority)
print("Acutal : ", y_test)

#acccuracy testing
accuracy = accuracy_score(y_test, predictions_priority)
print("Accuracy: ",accuracy)
print(classification_report(y_test, predictions_priority, zero_division=0))
print(df["priority"].value_counts())

joblib.dump(model, "Category_model.pkl")
joblib.dump(vectorizer, "Category_vectorizer.pkl")
joblib.dump(model_pri, "Priority_model.pkl")
joblib.dump(vectorizer_priority, "Priority_vectorizer.pkl")

print("ALL files are save")



