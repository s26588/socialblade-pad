import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

accounts_df = pd.read_csv('./accounts.csv', delimiter=';')

def run_classifier_experiment(model, df, column):
  X = df.copy()
  y = X[column]
  X.drop(columns=['name', 'channel_type', 'country'], inplace=True);

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  model.fit(X_train, y_train)

  y_pred = model.predict(X_test)

  print(f"Classifier test for column {column} and model {model}")
  print("Precision: %.3f:" % precision_score(y_test, y_pred, average='micro'))
  print("Recall: %.3f:" % recall_score(y_test, y_pred, average='micro'))
  print("F1: %.3f:" % f1_score(y_test, y_pred, average='micro'))
  print("Accuracy: %.3f:" % accuracy_score(y_test, y_pred))
  print();

run_classifier_experiment(KNeighborsClassifier(n_neighbors=12), accounts_df, 'channel_type')
run_classifier_experiment(KNeighborsClassifier(n_neighbors=12), accounts_df, 'country')

run_classifier_experiment(LogisticRegression(max_iter=10000), accounts_df, 'channel_type')
run_classifier_experiment(LogisticRegression(max_iter=10000), accounts_df, 'country')

run_classifier_experiment(DecisionTreeClassifier(), accounts_df, 'channel_type')
run_classifier_experiment(DecisionTreeClassifier(), accounts_df, 'country')