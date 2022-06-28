import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split

accounts_df = pd.read_csv('./accounts.csv', delimiter=';')

def run_regression_experiment(model, df, column):
  X = df.copy()
  y = X[column]
  X.drop(columns=['earnings_min', 'earnings_max', 'name', 'channel_type', 'country'], inplace=True);

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  model.fit(X_train, y_train)

  y_pred = model.predict(X_test)

  print(f"Regression test for column {column} and model {model}")
  print(f"R^2: {r2_score(y_test, y_pred)}")
  print(f"MAE: {mean_absolute_error(y_test, y_pred)}")
  print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred))}")
  print()

run_regression_experiment(LinearRegression(), accounts_df, 'earnings_min');
run_regression_experiment(LinearRegression(), accounts_df, 'earnings_max');

run_regression_experiment(DecisionTreeRegressor(max_depth=10), accounts_df, 'earnings_min');
run_regression_experiment(DecisionTreeRegressor(max_depth=10), accounts_df, 'earnings_max');